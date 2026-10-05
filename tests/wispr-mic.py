#!/usr/bin/env python3

# Replay fixed recordings through each Wispr Mic profile into Wispr Flow and
# score the transcripts, so profiles are compared on identical input.
#
# For each profile and clip: set the profile (hk-wispr-profile), point the
# chain's input at a private null sink instead of the mic, start hands-free
# dictation (hk-wispr-switch press), play the clip into the sink, stop, then
# read the new dictation out of Wispr's database and score its raw ASR against
# the clip's reference text (word error rate).
#
# Clips, references and results are personal data, so they live outside the
# repo, in $HK_WISPR_MIC_DIR (default ~/.local/share/hk-wispr-mic/).
#
# Usage:
#   tests/wispr-mic.py add NAME WAV "REFERENCE"     add a recording as a clip
#   tests/wispr-mic.py record NAME "REFERENCE"      record a clip from the mic
#   tests/wispr-mic.py list                         list clips
#   tests/wispr-mic.py run [-p off,whisper] [-n N] [CLIP...]
#                                                   replay and score
#   tests/wispr-mic.py report [RESULTS.jsonl]       score table (default: last run)
#   tests/wispr-mic.py restore                      reconnect the chain to the mic
#   tests/wispr-mic.py chain start|stop|status      run this checkout's chain
#                                                   in a private PipeWire process
#   tests/wispr-mic.py mine [--since YYYY-MM-DD]    find dictations sent through
#                                                   T3 Code as candidate clips
#   tests/wispr-mic.py candidates [--all]           list them (edited ones first)
#   tests/wispr-mic.py accept ID NAME ["REFERENCE"] make one a clip
#
# A reference may mark a span it is unsure of as {remove|retire}; the closer
# alternative is scored.
#
# It uses this checkout's hk-wispr-profile and profiles, not the ones on $PATH,
# so a worktree can be tested without touching the live config. `chain start`
# likewise loads this checkout's chain into its own PipeWire process, leaving
# the PipeWire daemon alone; only one Wispr Mic may exist at a time.
#
# Needs: Wispr running with "Wispr Mic (virtual)" picked as its mic,
# hk-wispr-switch running (with `press`, so restart it and then Wispr after
# updating it), and a scratch text field focused (Wispr pastes every
# transcript). Don't touch the mic's mute switch during a run.

import argparse
import contextlib
import datetime
import difflib
import itertools
import json
import math
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import wave
from array import array
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAIN_CONF = REPO / "config/pipewire/pipewire.conf.d/wispr-mic.conf"
CHAIN_DIR = Path(os.environ.get("XDG_RUNTIME_DIR", "/tmp")) / "hk-wispr-mic-chain"
DATA = Path(os.environ.get("HK_WISPR_MIC_DIR") or Path.home() / ".local/share/hk-wispr-mic")
CLIPS = DATA / "clips"
RESULTS = DATA / "results"
CANDIDATES = DATA / "candidates.jsonl"
T3_DB = Path(os.environ.get("T3_STATE_DB") or Path.home() / ".t3/userdata/statev2.sqlite")
MATCH_WINDOW = datetime.timedelta(minutes=30)
MAX_MATCH_DISTANCE = 0.5    # word edits per pasted word
WISPR_DB = Path(os.environ.get("WISPR_APP_SUPPORT_DIR") or Path.home() / ".config/Wispr Flow")
MIC = os.environ.get("HK_WISPR_SWITCH_SOURCE",
                     "alsa_input.usb-0c76_JOUNIVO_MICROPHONE-00.mono-fallback")
CHAIN_STREAM = "wispr_mic.capture"
CHAIN_SOURCE = "wispr_mic"
REPLAY_SINK = "hk_wispr_replay"

SCRATCH = "org.hyprkarl.wispr-mic-scratch"

LEAD_IN = 0.8           # s between starting dictation and playing the clip
TAIL = 1.0              # s after the clip before stopping
TRANSCRIPT_TIMEOUT = 45


def sh(*cmd, check=True):
    return subprocess.run(cmd, capture_output=True, text=True, check=check).stdout


def hk(*cmd):
    """Run one of this checkout's hk-* commands against this checkout."""
    env = {**os.environ, "HYPRKARL_PATH": str(REPO)}
    return subprocess.run([str(REPO / "bin" / cmd[0]), *cmd[1:]], capture_output=True,
                          text=True, check=True, env=env).stdout


# --- Clips ---

def load_clips():
    path = CLIPS / "clips.json"
    return json.loads(path.read_text()) if path.exists() else {}


def save_clips(clips):
    CLIPS.mkdir(parents=True, exist_ok=True)
    (CLIPS / "clips.json").write_text(json.dumps(clips, indent=2, ensure_ascii=False) + "\n")


def add(name, wav, reference):
    CLIPS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(wav, CLIPS / f"{name}.wav")
    clips = load_clips()
    clips[name] = reference
    save_clips(clips)
    print(f"{name}: {clip_info(CLIPS / f'{name}.wav')}")


def record(name, reference):
    CLIPS.mkdir(parents=True, exist_ok=True)
    out = CLIPS / f"{name}.wav"
    print(f'Say: "{reference}"\nRecording from {MIC}; press Enter to stop.')
    rec = subprocess.Popen(["pw-record", f"--target={MIC}", "--channels=1", "--format=s16",
                            "--rate=48000", str(out)])
    input()
    rec.terminate()
    rec.wait()
    clips = load_clips()
    clips[name] = reference
    save_clips(clips)
    print(f"{name}: {clip_info(out)}")


def clip_info(path):
    """Duration, peak and clipped-sample count of a 16-bit WAV."""
    with wave.open(str(path)) as w:
        rate, frames = w.getframerate(), w.readframes(w.getnframes())
    samples = array("h", frames)
    peak = max((abs(s) for s in samples), default=0)
    clipped = sum(1 for s in samples if abs(s) >= 32767)
    peak_db = 20 * math.log10(peak / 32768) if peak else float("-inf")
    return f"{len(samples) / rate:.1f} s, peak {peak_db:.1f} dBFS, {clipped} clipped samples"


# --- Scoring ---

def words(text):
    # Wispr formats some dictations as HTML lists (<ul><li>...): drop the tags
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"[^a-z0-9' ]", " ", text.lower().replace("-", " ")).split()


def edit_distance(ref, hyp):
    row = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        prev, row[0] = row[0], i
        for j, h in enumerate(hyp, 1):
            prev, row[j] = row[j], min(row[j] + 1, row[j - 1] + 1, prev + (r != h))
    return row[-1]


def wer(reference, hypothesis):
    """Word error rate, taking the closest choice at each {a|b} span."""
    parts = re.split(r"\{([^}]*)\}", reference)
    choices = [[p] if i % 2 == 0 else p.split("|") for i, p in enumerate(parts)]
    hyp = words(hypothesis)
    best = None
    for combo in itertools.product(*choices):
        ref = words(" ".join(combo))
        rate = edit_distance(ref, hyp) / max(len(ref), 1)
        best = rate if best is None else min(best, rate)
    return best


# --- Audio routing ---

def source_outputs():
    return json.loads(sh("pactl", "-f", "json", "list", "source-outputs") or "[]")


def chain_stream():
    return next((s for s in source_outputs()
                 if s["properties"].get("node.name") == CHAIN_STREAM), None)


def source_index(name):
    for line in sh("pactl", "list", "sources", "short").splitlines():
        fields = line.split()
        if fields[1:2] == [name]:
            return fields[0]
    return None


def wispr_source():
    """Name of the source Wispr is recording from, or None."""
    names = {line.split()[0]: line.split()[1]
             for line in sh("pactl", "list", "sources", "short").splitlines()}
    for s in source_outputs():
        pid = s["properties"].get("application.process.id") or ""
        try:
            exe = os.readlink(f"/proc/{pid}/exe") if pid.isdigit() else ""
        except OSError:
            exe = ""
        if "/wispr-flow/" in exe:
            return names.get(str(s["source"]))
    return None


class Replay:
    """A null sink the chain listens to in place of the mic, for the run."""

    def __enter__(self):
        stream = chain_stream()
        if not stream:
            sys.exit("Wispr Mic's chain is not running (hk-wispr-profile status)")
        # Never the default output: priority 0 so nothing else plays into it
        self.module = sh("pactl", "load-module", "module-null-sink",
                         f"sink_name={REPLAY_SINK}", "channel_map=mono",
                         "sink_properties=device.description=hk-wispr-replay"
                         " priority.session=0 priority.driver=0").strip()
        move_chain(f"{REPLAY_SINK}.monitor")
        return self

    def play(self, wav):
        subprocess.run(["pw-play", f"--target={REPLAY_SINK}", str(wav)], check=True)

    def __exit__(self, *_):
        restore()
        sh("pactl", "unload-module", self.module, check=False)


def move_chain(source):
    """Point the chain's input at `source` and wait for the move, which
    WirePlumber makes asynchronously."""
    stream = chain_stream()
    sh("pactl", "move-source-output", str(stream["index"]), source, check=False)
    target = source_index(source)
    deadline = time.time() + 3
    while (stream := chain_stream()) and str(stream["source"]) != target:
        if time.time() > deadline:
            sys.exit(f"Wispr Mic's input did not move to {source}")
        time.sleep(0.1)


def restore():
    if chain_stream():
        move_chain(MIC)


# --- Wispr ---

def latest_dictations(since):
    """Dictations newer than `since`, read from a copy of Wispr's database."""
    with tempfile.TemporaryDirectory() as snapshot:
        for f in WISPR_DB.glob("flow.sqlite*"):
            shutil.copy2(f, snapshot)
        con = sqlite3.connect(os.path.join(snapshot, "flow.sqlite"))
        con.row_factory = sqlite3.Row
        rows = [dict(r) for r in con.execute(
            "SELECT timestamp, asrText, formattedText, averageLogProb, micDevice, audio"
            " FROM History WHERE timestamp > ? ORDER BY timestamp", (since,))]
        con.close()
    return rows


@contextlib.contextmanager
def snapshot_db(files, name):
    """Open a copy of a live SQLite database (with its -wal/-shm), deleted
    afterwards: Wispr's holds every recording."""
    with tempfile.TemporaryDirectory() as snapshot:
        for f in files:
            shutil.copy2(f, snapshot)
        con = sqlite3.connect(os.path.join(snapshot, name))
        try:
            yield con
        finally:
            con.close()


def last_timestamp():
    with tempfile.TemporaryDirectory() as snapshot:
        for f in WISPR_DB.glob("flow.sqlite*"):
            shutil.copy2(f, snapshot)
        con = sqlite3.connect(os.path.join(snapshot, "flow.sqlite"))
        stamp = con.execute("SELECT max(timestamp) FROM History").fetchone()[0] or ""
        con.close()
    return stamp


def active_class():
    return json.loads(sh("hyprctl", "activewindow", "-j") or "{}").get("class")


def focus_scratch():
    """Wispr pastes every transcript into the focused window, so keep that a
    terminal running `cat > /dev/null`, whatever else the user clicks."""
    if active_class() == SCRATCH:
        return
    clients = json.loads(sh("hyprctl", "clients", "-j") or "[]")
    if not any(c.get("class") == SCRATCH for c in clients):
        subprocess.Popen(["setsid", "uwsm-app", "--", "xdg-terminal-exec", f"--app-id={SCRATCH}",
                          "-e", "sh", "-c", "cat > /dev/null"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.time() + 5
    while active_class() != SCRATCH:
        if time.time() > deadline:
            sys.exit("Couldn't focus the scratch window: stopping before Wispr pastes anywhere else")
        sh("hyprctl", "dispatch", f"hl.dsp.focus({{ window = 'class:^({SCRATCH})$' }})", check=False)
        time.sleep(0.3)


def press():
    hk("hk-wispr-switch", "press")


def dictate(replay, wav):
    """One hands-free dictation of `wav`; returns the new History row."""
    since = last_timestamp()
    focus_scratch()
    press()
    deadline = time.time() + 5
    while (src := wispr_source()) is None and time.time() < deadline:
        time.sleep(0.1)
    if src != CHAIN_SOURCE:
        if src:
            press()
        sys.exit(f"Wispr is recording from {src or 'nothing'}, not Wispr Mic: pick "
                 "\"Wispr Mic (virtual)\" in Wispr's mic settings")
    time.sleep(LEAD_IN)
    replay.play(wav)
    time.sleep(TAIL)
    focus_scratch()             # Wispr pastes once dictation stops
    press()
    deadline = time.time() + TRANSCRIPT_TIMEOUT
    while time.time() < deadline:
        rows = latest_dictations(since)
        if rows:
            return rows[-1]
        time.sleep(0.5)
    return None


def profile(name=None):
    if name is None:
        return hk("hk-wispr-profile", "status").strip()
    hk("hk-wispr-profile", name)
    return name


# --- Private chain ---

def chain_pid():
    try:
        pid = int((CHAIN_DIR / "pid").read_text())
        return pid if "pipewire" in Path(f"/proc/{pid}/cmdline").read_text() else None
    except (OSError, ValueError):
        return None


def chain(action):
    """Run CHAIN_CONF in its own `pipewire -c` (a client of the PipeWire
    daemon, like filter-chain.service), so testing never restarts audio."""
    pid = chain_pid()
    if action == "status":
        print(f"private chain running (pid {pid})" if pid else "no private chain")
        return
    if action == "stop":
        if pid:
            os.kill(pid, 15)
        (CHAIN_DIR / "pid").unlink(missing_ok=True)
        return
    if pid:
        sys.exit(f"private chain already running (pid {pid})")
    if source_index(CHAIN_SOURCE):
        sys.exit("Wispr Mic already exists (the live chain?): only one at a time")
    conf_d = CHAIN_DIR / "daemon.conf.d"
    conf_d.mkdir(parents=True, exist_ok=True)
    shutil.copy("/usr/share/pipewire/filter-chain.conf", CHAIN_DIR / "daemon.conf")
    shutil.copy(CHAIN_CONF, conf_d / "wispr-mic.conf")
    log = open(CHAIN_DIR / "log.txt", "w")
    proc = subprocess.Popen(["pipewire", "-c", "daemon.conf"], stdout=log, stderr=log,
                            stdin=subprocess.DEVNULL, start_new_session=True,
                            env={**os.environ, "PIPEWIRE_CONFIG_DIR": str(CHAIN_DIR)})
    (CHAIN_DIR / "pid").write_text(str(proc.pid))
    deadline = time.time() + 5
    while not source_index(CHAIN_SOURCE) and time.time() < deadline:
        time.sleep(0.2)
    if not source_index(CHAIN_SOURCE):
        chain("stop")
        sys.exit(f"the chain did not load (lsp-plugins-ladspa installed? see {CHAIN_DIR}/log.txt)")
    print(f"Wispr Mic running from {CHAIN_CONF} (pid {proc.pid})")


# --- Mining T3 Code ---

def utc(stamp):
    """Wispr ("2026-10-03 04:04:28.918 +00:00") and T3 ("...Z") timestamps."""
    stamp = stamp.replace(" +00:00", "+00:00").replace("Z", "+00:00").replace(" ", "T", 1)
    return datetime.datetime.fromisoformat(stamp)


def best_span(pasted, message):
    """Where word list `pasted` best fits inside `message`, free to start and
    end anywhere: (edit distance, start, end)."""
    prev, start = [0] * (len(message) + 1), list(range(len(message) + 1))
    for i, p in enumerate(pasted, 1):
        cur, cur_start = [i] + [0] * len(message), [0] * (len(message) + 1)
        for j, m in enumerate(message, 1):
            cur[j], cur_start[j] = min((prev[j - 1] + (p != m), start[j - 1]),
                                       (prev[j] + 1, start[j]),
                                       (cur[j - 1] + 1, cur_start[j - 1]))
        prev, start = cur, cur_start
    dist, end = min((d, j) for j, d in enumerate(prev))
    return dist, start[end], end


def mine(since):
    """Pair each dictation with the T3 Code message it was sent in, if any:
    the matching span of the message is what the user actually sent, edits
    included. Writes CANDIDATES for review; nothing becomes a clip yet."""
    with snapshot_db(T3_DB.parent.glob(T3_DB.name + "*"), T3_DB.name) as t3:
        messages = [(utc(m["createdAt"]), words(m["text"])) for m in (
            json.loads(p) for (p,) in t3.execute(
                "SELECT payload_json FROM orchestration_v2_projection_messages"
                " WHERE role = 'user'"))]
    with snapshot_db(WISPR_DB.glob("flow.sqlite*"), "flow.sqlite") as wispr:
        rows = wispr.execute(
            "SELECT transcriptEntityId, timestamp, asrText, pastedText FROM History"
            " WHERE pastedText != '' AND audio IS NOT NULL AND timestamp >= ?"
            " ORDER BY timestamp", (since or "",)).fetchall()

    found = []
    for entity, stamp, asr, pasted in rows:
        pasted_words = words(pasted)
        if len(pasted_words) < 3:
            continue
        sent_at = utc(stamp)
        best = None
        for when, message in messages:
            if sent_at <= when <= sent_at + MATCH_WINDOW:
                dist, a, b = best_span(pasted_words, message)
                if best is None or dist < best[0]:
                    best = (dist, " ".join(message[a:b]))
        if best and best[0] / len(pasted_words) <= MAX_MATCH_DISTANCE:
            found.append({"id": entity, "time": stamp, "asr": asr, "pasted": pasted,
                          "sent": best[1], "distance": round(best[0] / len(pasted_words), 3)})
    DATA.mkdir(parents=True, exist_ok=True)
    with open(CANDIDATES, "w") as out:
        for c in found:
            out.write(json.dumps(c, ensure_ascii=False) + "\n")
    edited = sum(1 for c in found if c["distance"] > 0)
    print(f"{len(found)} of {len(rows)} dictations matched a T3 message: "
          f"{edited} edited, {len(found) - edited} sent unchanged. See `candidates`.")


def load_candidates():
    if not CANDIDATES.exists():
        sys.exit("No candidates yet: run `mine`")
    return [json.loads(line) for line in open(CANDIDATES)]


def show_candidates(show_all):
    found = sorted(load_candidates(), key=lambda c: -c["distance"])
    for c in found if show_all else [c for c in found if c["distance"] > 0]:
        pasted = words(c["pasted"])
        sent = c["sent"].split()
        changes = [f"{' '.join(pasted[i1:i2]) or '-'} -> {' '.join(sent[j1:j2]) or '-'}"
                   for tag, i1, i2, j1, j2 in
                   difflib.SequenceMatcher(None, pasted, sent).get_opcodes() if tag != "equal"]
        print(f"{c['id'][:8]}  {c['time'][:16]}  {c['distance']:.2f}  {'; '.join(changes)}")
        print(f"          sent: {c['sent']}")


def accept(prefix, name, reference):
    matches = [c for c in load_candidates() if c["id"].startswith(prefix)]
    if len(matches) != 1:
        sys.exit(f"{len(matches)} candidates match {prefix}")
    c = matches[0]
    with snapshot_db(WISPR_DB.glob("flow.sqlite*"), "flow.sqlite") as wispr:
        audio = wispr.execute("SELECT audio FROM History WHERE transcriptEntityId = ?",
                              (c["id"],)).fetchone()[0]
    with tempfile.NamedTemporaryFile(suffix=".wav") as wav:
        wav.write(audio)
        wav.flush()
        add(name, wav.name, reference or c["sent"])


# --- Commands ---

def run(profiles, repeat, names):
    clips = load_clips()
    names = names or list(clips)
    missing = [n for n in names if n not in clips]
    if missing:
        sys.exit(f"No such clip: {', '.join(missing)}")
    if not names:
        sys.exit("No clips yet: add some with `add` or `record`")

    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out_dir = RESULTS / stamp
    (out_dir / "audio").mkdir(parents=True)
    trials = [(p, n, i) for i in range(repeat) for p in profiles for n in names]
    print(f"{len(trials)} dictations, about {sum(wav_seconds(CLIPS / f'{n}.wav') + 6 for _, n, _ in trials) / 60:.0f} min.")
    if sys.stdin.isatty():
        input("Wispr pastes into a scratch window this opens; press Enter to start... ")

    before = profile()
    with Replay() as replay, open(out_dir / "results.jsonl", "w") as results:
        try:
            for p, n, i in trials:
                profile(p)
                row = dictate(replay, CLIPS / f"{n}.wav")
                record = {"profile": p, "clip": n, "trial": i, "reference": clips[n]}
                if row:
                    audio = out_dir / "audio" / f"{p}_{n}_{i}.wav"
                    if row["audio"]:
                        audio.write_bytes(row["audio"])
                    record.update(asr=row["asrText"], formatted=row["formattedText"],
                                  log_prob=row["averageLogProb"], mic=row["micDevice"],
                                  wer=wer(clips[n], row["asrText"]),
                                  wer_formatted=wer(clips[n], row["formattedText"]),
                                  received=clip_info(audio) if row["audio"] else None)
                    print(f"{p:>16} {n:<20} WER {record['wer']:.2f}  {row['asrText']}")
                else:
                    print(f"{p:>16} {n:<20} no transcript")
                results.write(json.dumps(record, ensure_ascii=False) + "\n")
                results.flush()
        finally:
            profile(before)
    print()
    report(out_dir / "results.jsonl")


def wav_seconds(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def report(path=None):
    if path is None:
        runs = sorted(RESULTS.glob("*/results.jsonl"))
        if not runs:
            sys.exit("No results yet")
        path = runs[-1]
    records = [json.loads(line) for line in open(path)]
    # Rescore from the stored text, so scoring fixes apply to old runs too
    for r in records:
        if r.get("asr") is not None:
            r["wer"] = wer(r["reference"], r["asr"])
            r["wer_formatted"] = wer(r["reference"], r["formatted"])
    profiles = list(dict.fromkeys(r["profile"] for r in records))
    clips = list(dict.fromkeys(r["clip"] for r in records))

    def mean(rs, key):
        vals = [r[key] for r in rs if r.get(key) is not None]
        return f"{sum(vals) / len(vals):.2f}" if vals else "  - "

    print(f"{path}\n")
    print(f"{'WER (raw ASR)':<20}" + "".join(f"{p:>16}" for p in profiles))
    for c in clips:
        print(f"{c:<20}" + "".join(
            f"{mean([r for r in records if r['clip'] == c and r['profile'] == p], 'wer'):>16}"
            for p in profiles))
    print(f"{'mean':<20}" + "".join(
        f"{mean([r for r in records if r['profile'] == p], 'wer'):>16}" for p in profiles))
    print(f"{'mean (formatted)':<20}" + "".join(
        f"{mean([r for r in records if r['profile'] == p], 'wer_formatted'):>16}"
        for p in profiles))


def main():
    parser = argparse.ArgumentParser(description="Score Wispr Mic profiles on fixed recordings.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("name")
    a.add_argument("wav")
    a.add_argument("reference")
    r = sub.add_parser("record")
    r.add_argument("name")
    r.add_argument("reference")
    sub.add_parser("list")
    mi = sub.add_parser("mine")
    mi.add_argument("--since", help="only dictations on or after YYYY-MM-DD (UTC)")
    ca = sub.add_parser("candidates")
    ca.add_argument("--all", action="store_true", help="include ones sent unchanged")
    ac = sub.add_parser("accept")
    ac.add_argument("id", help="a candidate id, or a unique prefix of one")
    ac.add_argument("name")
    ac.add_argument("reference", nargs="?", help="default: the text that was sent")
    u = sub.add_parser("run")
    u.add_argument("-p", "--profiles", default="off,whisper",
                   help="comma-separated (default: off,whisper)")
    u.add_argument("-n", "--repeat", type=int, default=1, help="passes over the clips")
    u.add_argument("clips", nargs="*")
    p = sub.add_parser("report")
    p.add_argument("results", nargs="?")
    sub.add_parser("restore")
    c = sub.add_parser("chain")
    c.add_argument("action", choices=["start", "stop", "status"])
    args = parser.parse_args()

    if args.cmd == "add":
        add(args.name, args.wav, args.reference)
    elif args.cmd == "record":
        record(args.name, args.reference)
    elif args.cmd == "mine":
        mine(args.since)
    elif args.cmd == "candidates":
        show_candidates(args.all)
    elif args.cmd == "accept":
        accept(args.id, args.name, args.reference)
    elif args.cmd == "list":
        for name, reference in load_clips().items():
            print(f"{name:<20} {clip_info(CLIPS / f'{name}.wav')}\n{'':<20} {reference}")
    elif args.cmd == "run":
        run(args.profiles.split(","), args.repeat, args.clips)
    elif args.cmd == "report":
        report(args.results)
    elif args.cmd == "restore":
        restore()
    elif args.cmd == "chain":
        chain(args.action)


if __name__ == "__main__":
    main()
