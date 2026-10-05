# bin/lib/app.sh
# Shared helpers for the hk-app-* commands, which install and update AppImages
# outside the package manager. Source from each script:
#   SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
#   source "$SCRIPT_DIR/lib/app.sh"
#
# Each app has a config named <id>.conf, sourced as bash. Yours live in
# ~/.config/hyprkarl/apps/, where hk-app install writes them; Hyprkarl's ship in
# defaults/config/hyprkarl/apps/, and a file of yours with the same name
# replaces one. Keys:
#   repo=owner/name          GitHub repo to install releases from (omit for a
#                            manual URL install, which hk-app update skips)
#   url=https://...          Direct AppImage URL (manual installs only)
#   sha256=HEX               Expected checksum of the url download (GitHub
#                            releases use the asset's published digest)
#   tag_pattern='-nightly\.' Regex a release tag must match; this also admits
#                            prereleases. Unset: newest non-prerelease.
#   asset_pattern='...'      Regex for the AppImage asset (default: <arch>.AppImage)
#   args=(--flag ...)        Extra launcher arguments, appended after the caller's
#   desktop_entry=('Key=value' ...)
#                            Set or add keys in the desktop entry's main group
#   post_install='cmd ...'   Run after extraction and on config-update, with
#                            APP_ID, APP_DIR (the release dir) and APP_TAG set.
#                            A failure aborts the install.
#
# Layout per app:
#   ~/.local/opt/<id>/<tag>/        extracted AppImage (tag made a single path
#                                   component by app_dir_tag)
#   ~/.local/opt/<id>/current       symlink to the active release
#   ~/.local/opt/<id>/previous      symlink to the one before it (rollback)
#   ~/.local/bin/<id>               launcher: runs current/AppRun
#   ~/.local/share/applications/<id>.desktop
#
# Functions:
#   app_ids                          Print the id of every app config
#   app_conf_path ID                 Print the config ID uses, yours first
#   app_load ID                      Source ID's config into repo/url/args/...
#   app_dir_tag TAG                  Print TAG as a release dir name
#   app_current_tag ID               Print the active release tag
#   app_previous_tag ID              Print the rollback release tag
#   app_valid_regex RE               Return 0 if RE is a valid jq regex
#   app_latest                       Resolve the newest matching release; sets
#                                    release_tag asset_name asset_url asset_sha256
#   app_download URL NAME SHA256     Download into the cache; prints the file path
#   app_stage IMAGE                  Extract and delete IMAGE; prints the extracted dir
#   app_commit ID TAG [STAGED]       Move a staged release into place (or reuse
#                                    an extracted one), run the post-install
#                                    hook, activate, integrate, prune; on a
#                                    failure, leave the installed version as it was
#   app_integrate ID                 Write the launcher and desktop entry
#   app_run_hook ID DIR TAG          Run the app's post_install command
#   app_running ID                   Return 0 if any process runs from the app dir
#   app_lock                         Take the hk-app lock or exit

# Release and config globals here are read by the hk-app-* commands.
# shellcheck shell=bash disable=SC2034
APP_CONF_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/hyprkarl/apps"
APP_DEFAULT_CONF_DIR="$HYPRKARL_PATH/defaults/config/hyprkarl/apps"
APP_OPT_DIR="$HOME/.local/opt"
APP_BIN_DIR="$HOME/.local/bin"
APP_DESKTOP_DIR="$HOME/.local/share/applications"
APP_CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/hk-app"

info()  { gum log --level info  "$*"; }
warn()  { gum log --level warn  "$*"; }
error() { gum log --level error "$*"; exit 1; }

# --- config ---

app_ids() {
  local conf
  for conf in "$APP_CONF_DIR"/*.conf "$APP_DEFAULT_CONF_DIR"/*.conf; do
    [[ -f "$conf" ]] && basename "$conf" .conf
  done | sort -u
}

# Prints nothing when ID has no config.
app_conf_path() {
  local conf
  for conf in "$APP_CONF_DIR/$1.conf" "$APP_DEFAULT_CONF_DIR/$1.conf"; do
    if [[ -f "$conf" ]]; then
      printf '%s\n' "$conf"
      return 0
    fi
  done
}

app_load() {
  local id="$1"
  app_conf=$(app_conf_path "$id")
  repo="" url="" tag_pattern="" asset_pattern="" post_install="" sha256=""
  args=() desktop_entry=()
  if [[ -z "$app_conf" ]]; then
    error "No config for $id (expected $APP_CONF_DIR/$id.conf)"
  fi
  # shellcheck source=/dev/null
  source "$app_conf"
  asset_pattern="${asset_pattern:-$(uname -m)\\.AppImage\$}"
}

# Release tags become dir names under ~/.local/opt/<id>/, so make each a
# single path component: "/" becomes "_", and a leading "." or "-" (which
# covers . and ..) or a clash with the current/previous links gets a "_"
# prefix.
app_dir_tag() {
  local tag="${1//\//_}"
  if [[ "$tag" == [.-]* || "$tag" == current || "$tag" == previous ]]; then
    tag="_$tag"
  fi
  printf '%s\n' "$tag"
}

app_current_tag() {
  local link
  link=$(readlink "$APP_OPT_DIR/$1/current" 2>/dev/null)
  [[ -n "$link" ]] && basename "$link"
}

app_previous_tag() {
  local link
  link=$(readlink "$APP_OPT_DIR/$1/previous" 2>/dev/null)
  [[ -n "$link" ]] && basename "$link"
}

# --- releases ---

# Print one page (100 releases, newest first) of REPO's releases.
app_github_releases() {
  local path="repos/$1/releases?per_page=100&page=$2"
  # gh is authenticated (5000 req/h); anonymous curl gets 60.
  if gh auth token &>/dev/null; then
    gh api "$path"
  else
    curl -fsSL "https://api.github.com/$path"
  fi
}

app_valid_regex() {
  jq -n --arg re "$1" '"" | test($re)' &>/dev/null
}

app_latest() {
  local json page max_pages=5
  release_tag="" asset_name="" asset_url="" asset_sha256=""
  # A bad pattern would fail jq on every page and read as "no match".
  if [[ -n "$tag_pattern" ]] && ! app_valid_regex "$tag_pattern"; then
    warn "Invalid tag_pattern regex for $repo: $tag_pattern"
    return 1
  fi
  if ! app_valid_regex "$asset_pattern"; then
    warn "Invalid asset_pattern regex for $repo: $asset_pattern"
    return 1
  fi
  # Pages run newest first, so stop at the first page with a match. Capped
  # to spare the anonymous rate limit.
  for ((page = 1; page <= max_pages; page++)); do
    json=$(app_github_releases "$repo" "$page")
    if [[ -z "$json" ]]; then
      warn "Cannot reach GitHub releases for $repo"
      return 1
    fi
    # Newest non-draft release whose tag matches (or newest stable if no
    # pattern), then its first asset matching asset_pattern.
    IFS=$'\t' read -r release_tag asset_name asset_url asset_sha256 < <(
      jq -r --arg tp "$tag_pattern" --arg ap "$asset_pattern" '
        [ .[] | select(.draft | not)
              | select(if $tp == "" then (.prerelease | not) else (.tag_name | test($tp)) end)
              | . as $r | .assets[] | select(.name | test($ap))
              | [$r.tag_name, .name, .browser_download_url, ((.digest // "") | sub("^sha256:"; ""))] ]
        | first // empty | @tsv' <<<"$json")
    [[ -n "$release_tag" ]] && return 0
    # A short page is the last one.
    [[ "$(jq length <<<"$json")" -lt 100 ]] && break
  done
  if [[ "$page" -gt "$max_pages" ]]; then
    warn "No release in the newest $((max_pages * 100)) of $repo matches tag '${tag_pattern:-<stable>}' and asset '$asset_pattern'"
  else
    warn "No release in $repo matches tag '${tag_pattern:-<stable>}' and asset '$asset_pattern'"
  fi
  return 1
}

# --- install steps ---

app_download() {
  local url="$1" name="$2" sha="$3" file
  mkdir -p "$APP_CACHE_DIR"
  file="$APP_CACHE_DIR/$name"
  info "Downloading $name" >&2
  if ! curl -fL --retry 3 --connect-timeout 30 --progress-bar -o "$file.part" "$url"; then
    rm -f "$file.part"
    warn "Download failed: $url" >&2
    return 1
  fi
  mv "$file.part" "$file"
  if [[ -n "$sha" ]]; then
    if ! sha256sum --status -c <<<"$sha  $file"; then
      rm -f "$file"
      warn "SHA-256 mismatch for $name; not installing it" >&2
      return 1
    fi
  else
    warn "No checksum published for $name; installing unverified" >&2
  fi
  printf '%s\n' "$file"
}

app_stage() {
  local image="$1" work
  mkdir -p "$APP_OPT_DIR"
  # Stage on the same filesystem as the install so the final move is a rename.
  work=$(mktemp -d "$APP_OPT_DIR/.hk-app.XXXXXX")
  chmod +x "$image"
  info "Extracting $(basename "$image")" >&2
  if ! (cd "$work" && "$image" --appimage-extract >/dev/null); then
    rm -rf "$work" "$image"
    warn "Extraction failed; is $(basename "$image") a type-2 AppImage?" >&2
    return 1
  fi
  if [[ ! -x "$work/squashfs-root/AppRun" ]]; then
    rm -rf "$work"
    warn "No AppRun in $(basename "$image")" >&2
    return 1
  fi
  rm -f "$image"
  printf '%s\n' "$work/squashfs-root"
}

app_relink() {
  local target="$1" link="$2"
  ln -sfn "$target" "$link.new" && mv -T "$link.new" "$link"
}

app_run_hook() {
  local id="$1" dir="$2" tag="$3"
  [[ -z "$post_install" ]] && return 0
  info "Running post-install: $post_install"
  APP_ID="$id" APP_DIR="$dir" APP_TAG="$tag" bash -c "$post_install"
}

app_commit() {
  local id="$1" tag staged="$3" root="$APP_OPT_DIR/$1" dest fresh=0 old_cur old_prev
  tag=$(app_dir_tag "$2")
  dest="$root/$tag"
  mkdir -p "$root"
  if [[ -d "$dest" ]]; then
    info "$id $tag is already extracted; reusing it"
    [[ -n "$staged" ]] && rm -rf "$(dirname "$staged")"
  else
    mv -T "$staged" "$dest" || error "Cannot create $dest"
    rm -rf "$(dirname "$staged")"
    fresh=1
  fi

  if ! app_run_hook "$id" "$dest" "$tag"; then
    [[ "$fresh" -eq 1 ]] && rm -rf "$dest"
    error "Post-install for $id failed; the installed version is unchanged"
  fi

  # Raw link targets (relative or absolute), to put back if activation fails.
  old_cur=$(readlink "$root/current" 2>/dev/null)
  old_prev=$(readlink "$root/previous" 2>/dev/null)
  if ! app_activate "$id" "$tag"; then
    if ! app_restore "$id" "$old_cur" "$old_prev"; then
      error "Cannot activate $id $tag, nor restore the current and previous links in $root"
    fi
    [[ "$fresh" -eq 1 ]] && rm -rf "$dest"
    error "Cannot activate $id $tag; the installed version is unchanged"
  fi
  app_prune "$id"
  info "Installed $id $tag"
}

# Point current at TAG and previous at the release it replaces, then integrate.
app_activate() {
  local id="$1" tag="$2" root="$APP_OPT_DIR/$1" old
  old=$(app_current_tag "$id")
  if [[ -n "$old" && "$old" != "$tag" ]]; then
    app_relink "$old" "$root/previous" || return 1
  fi
  app_relink "$tag" "$root/current" || return 1
  app_integrate "$id"
}

# Undo app_activate given the old current and previous link targets (empty if
# the link did not exist), then re-integrate the old release, best effort.
app_restore() {
  local id="$1" cur="$2" prev="$3" root="$APP_OPT_DIR/$1"
  app_restore_link "$cur" "$root/current" || return 1
  app_restore_link "$prev" "$root/previous" || return 1
  if [[ -n "$cur" ]]; then
    app_integrate "$id" || warn "Cannot restore the launcher and desktop entry for $id"
  elif grep -qs '^# Generated by hk-app' "$APP_BIN_DIR/$id"; then
    # First install: the launcher would run a release that is not current.
    rm -f "$APP_BIN_DIR/$id"
  fi
  return 0
}

app_restore_link() {
  local target="$1" link="$2"
  if [[ -n "$target" ]]; then
    app_relink "$target" "$link"
  else
    rm -f "$link"
  fi
}

app_prune() {
  local root="$APP_OPT_DIR/$1" keep_cur keep_prev dir
  keep_cur=$(app_current_tag "$1")
  keep_prev=$(app_previous_tag "$1")
  for dir in "$root"/*/; do
    dir="${dir%/}"
    [[ -L "$dir" ]] && continue
    [[ "$(basename "$dir")" == "$keep_cur" || "$(basename "$dir")" == "$keep_prev" ]] && continue
    info "Removing old release $(basename "$dir")"
    rm -rf "$dir"
  done
}

# --- desktop integration ---

app_icon_path() {
  local dir="$1" desktop="$2" name ext
  # .DirIcon is usually a relative symlink into usr/share/icons.
  if [[ -L "$dir/.DirIcon" ]]; then
    printf '%s/%s\n' "$dir" "$(readlink "$dir/.DirIcon")"
    return
  fi
  name=$(sed -n 's/^Icon=//p' "$desktop" | head -n1)
  for ext in png svg; do
    if [[ -f "$dir/$name.$ext" ]]; then
      printf '%s/%s.%s\n' "$dir" "$name" "$ext"
      return
    fi
  done
  printf '%s/.DirIcon\n' "$dir"
}

# Apply desktop_entry to the [Desktop Entry] group on stdin: replace keys it
# already has, append the rest at the end of the group.
app_desktop_override() {
  awk -v extra="$(printf '%s\n' "${desktop_entry[@]}")" '
    function flush(   i) {
      for (i = 1; i <= m; i++) if (!(order[i] in seen)) print want[order[i]]
      flushed = 1
    }
    BEGIN {
      n = split(extra, lines, "\n")
      for (i = 1; i <= n; i++) {
        if (lines[i] == "") continue
        k = lines[i]; sub(/=.*/, "", k)
        want[k] = lines[i]; order[++m] = k
      }
    }
    /^\[/ { if (main && !flushed) flush(); main = ($0 == "[Desktop Entry]"); print; next }
    main { k = $0; sub(/=.*/, "", k); if (k in want) { print want[k]; seen[k] = 1; next } }
    { print }
    END { if (main && !flushed) flush() }'
}

# Write stdin to FILE with MODE via a temp file and a rename, so a failure
# leaves FILE as it was.
app_write() {
  local file="$1" mode="${2:-0644}"
  if ! cat > "$file.new" || ! chmod "$mode" "$file.new" || ! mv -T "$file.new" "$file"; then
    rm -f "$file.new"
    warn "Cannot write $file"
    return 1
  fi
}

app_integrate() {
  local id="$1" dir="$APP_OPT_DIR/$1/current" launcher="$APP_BIN_DIR/$1" desktop icon entry
  mkdir -p "$APP_BIN_DIR" "$APP_DESKTOP_DIR" || return 1

  # Extra args go after the caller's so AppRun still sees its own flags
  # (e.g. wispr-flow --doctor) first; Electron parses switches anywhere.
  {
    printf '#!/bin/bash\n# Generated by hk-app from %s\n' "$app_conf"
    printf 'exec %q "$@"' "$dir/AppRun"
    if [[ ${#args[@]} -gt 0 ]]; then
      printf ' %q' "${args[@]}"
    fi
    printf '\n'
  } | app_write "$launcher" 0755 || return 1

  desktop=$(find "$dir/" -maxdepth 1 -name '*.desktop' | head -n1)
  if [[ -z "$desktop" ]]; then
    warn "$id ships no desktop entry; only the launcher was written"
    return 0
  fi
  icon=$(app_icon_path "$dir" "$desktop")
  # Replace the first word of every Exec (main entry and actions), keeping
  # bundled flags and field codes like %U. Rendered in checked steps before
  # writing, so a failed read cannot replace the entry with an empty one.
  if ! entry=$(sed -E \
      -e "s#^Exec=(\"[^\"]*\"|[^ ]+)#Exec=$launcher#" \
      -e "s#^TryExec=.*#TryExec=$launcher#" \
      -e "s#^Icon=.*#Icon=$icon#" \
      "$desktop") || ! entry=$(app_desktop_override <<<"$entry") || [[ -z "$entry" ]]; then
    warn "Cannot read the desktop entry $desktop"
    return 1
  fi
  printf '%s\n' "$entry" | app_write "$APP_DESKTOP_DIR/$id.desktop" || return 1
  update-desktop-database "$APP_DESKTOP_DIR" &>/dev/null
  return 0
}

# --- misc ---

app_running() {
  pgrep -f "$APP_OPT_DIR/$1/" &>/dev/null
}

app_lock() {
  mkdir -p "$APP_OPT_DIR"
  exec 9>"$APP_OPT_DIR/.hk-app.lock"
  flock -n 9 || error "Another hk-app install or update is running"
  # Holding the lock, any staging dir left behind is from an interrupted run.
  rm -rf "$APP_OPT_DIR"/.hk-app.??????
}
