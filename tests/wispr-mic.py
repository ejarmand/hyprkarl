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
#
# A reference may mark a span it is unsure of as {remove|retire}; the closer
# alternative is scored.
#
# Needs: Wispr running with "Wispr Mic (virtual)" picked as its mic,
# hk-wispr-switch running, and a scratch text field focused (Wispr pastes every
# transcript). Don't touch the mic's mute switch during a run.

import argparse
import datetime
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

DATA = Path(os.environ.get("HK_WISPR_MIC_DIR") or Path.home() / ".local/share/hk-wispr-mic")
CLIPS = DATA / "clips"
RESULTS = DATA / "results"
WISPR_DB = Path(os.environ.get("WISPR_APP_SUPPORT_DIR") or Path.home() / ".config/Wispr Flow")
MIC = os.environ.get("HK_WISPR_SWITCH_SOURCE",
                     "alsa_input.usb-0c76_JOUNIVO_MICROPHONE-00.mono-fallback")
CHAIN_STREAM = "wispr_mic.capture"
CHAIN_SOURCE = "wispr_mic"
REPLAY_SINK = "hk_wispr_replay"

LEAD_IN = 0.8           # s between starting dictation and playing the clip
TAIL = 1.0              # s after the clip before stopping
TRANSCRIPT_TIMEOUT = 45


def sh(*cmd, check=True):
    return subprocess.run(cmd, capture_output=True, text=True, check=check).stdout


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
    return re.sub(r"[^a-z0-9' ]", " ", (text or "").lower().replace("-", " ")).split()


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
        sh("pactl", "move-source-output", str(stream["index"]), f"{REPLAY_SINK}.monitor")
        return self

    def play(self, wav):
        subprocess.run(["pw-play", f"--target={REPLAY_SINK}", str(wav)], check=True)

    def __exit__(self, *_):
        restore()
        sh("pactl", "unload-module", self.module, check=False)


def restore():
    stream = chain_stream()
    if stream:
        sh("pactl", "move-source-output", str(stream["index"]), MIC, check=False)


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


def last_timestamp():
    with tempfile.TemporaryDirectory() as snapshot:
        for f in WISPR_DB.glob("flow.sqlite*"):
            shutil.copy2(f, snapshot)
        con = sqlite3.connect(os.path.join(snapshot, "flow.sqlite"))
        stamp = con.execute("SELECT max(timestamp) FROM History").fetchone()[0] or ""
        con.close()
    return stamp


def press():
    sh("hk-wispr-switch", "press")


def dictate(replay, wav):
    """One hands-free dictation of `wav`; returns the new History row."""
    since = last_timestamp()
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
        return sh("hk-wispr-profile", "status").strip()
    sh("hk-wispr-profile", name)
    return name


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
    input("Focus a scratch text field (Wispr pastes every transcript), then press Enter... ")
    for s in (3, 2, 1):
        print(f"  {s}", end="\r", flush=True)
        time.sleep(1)

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
    u = sub.add_parser("run")
    u.add_argument("-p", "--profiles", default="off,whisper",
                   help="comma-separated (default: off,whisper)")
    u.add_argument("-n", "--repeat", type=int, default=1, help="passes over the clips")
    u.add_argument("clips", nargs="*")
    p = sub.add_parser("report")
    p.add_argument("results", nargs="?")
    sub.add_parser("restore")
    args = parser.parse_args()

    if args.cmd == "add":
        add(args.name, args.wav, args.reference)
    elif args.cmd == "record":
        record(args.name, args.reference)
    elif args.cmd == "list":
        for name, reference in load_clips().items():
            print(f"{name:<20} {clip_info(CLIPS / f'{name}.wav')}\n{'':<20} {reference}")
    elif args.cmd == "run":
        run(args.profiles.split(","), args.repeat, args.clips)
    elif args.cmd == "report":
        report(args.results)
    elif args.cmd == "restore":
        restore()


if __name__ == "__main__":
    main()
