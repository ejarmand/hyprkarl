# bin/lib/app.sh
# Shared helpers for the hk-app-* commands, which install and update AppImages
# outside the package manager. Source from each script:
#   SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
#   source "$SCRIPT_DIR/lib/app.sh"
#
# Each app has a tracked config at config/hyprkarl/apps/<id>.conf, sourced as
# bash. Keys:
#   repo=owner/name          GitHub repo to install releases from (omit for a
#                            manual URL install, which hk-app update skips)
#   url=https://...          Direct AppImage URL (manual installs only)
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
#   ~/.local/opt/<id>/<tag>/        extracted AppImage
#   ~/.local/opt/<id>/current       symlink to the active release
#   ~/.local/opt/<id>/previous      symlink to the one before it (rollback)
#   ~/.local/bin/<id>               launcher: runs current/AppRun
#   ~/.local/share/applications/<id>.desktop
#
# Functions:
#   app_ids                          Print the id of every app config
#   app_load ID                      Source ID's config into repo/url/args/...
#   app_current_tag ID               Print the active release tag
#   app_previous_tag ID              Print the rollback release tag
#   app_latest                       Resolve the newest matching release; sets
#                                    release_tag asset_name asset_url asset_sha256
#   app_download URL NAME SHA256     Download into the cache; prints the file path
#   app_stage IMAGE                  Extract and delete IMAGE; prints the extracted dir
#   app_commit ID TAG [STAGED]       Move a staged release into place (or reuse
#                                    an extracted one), run the post-install
#                                    hook, activate, integrate, prune
#   app_integrate ID                 Write the launcher and desktop entry
#   app_run_hook ID DIR TAG          Run the app's post_install command
#   app_running ID                   Return 0 if any process runs from the app dir
#   app_lock                         Take the hk-app lock or exit

APP_CONF_DIR="$HYPRKARL_PATH/config/hyprkarl/apps"
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
  for conf in "$APP_CONF_DIR"/*.conf; do
    [[ -f "$conf" ]] && basename "$conf" .conf
  done
}

app_load() {
  local id="$1"
  app_conf="$APP_CONF_DIR/$id.conf"
  repo="" url="" tag_pattern="" asset_pattern="" post_install="" sha256=""
  args=() desktop_entry=()
  if [[ ! -f "$app_conf" ]]; then
    error "No config for $id (expected $app_conf)"
  fi
  source "$app_conf"
  asset_pattern="${asset_pattern:-$(uname -m)\\.AppImage\$}"
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

app_github_releases() {
  # gh is authenticated (5000 req/h); anonymous curl gets 60.
  if gh auth token &>/dev/null; then
    gh api "repos/$1/releases?per_page=50"
  else
    curl -fsSL "https://api.github.com/repos/$1/releases?per_page=50"
  fi
}

app_latest() {
  local json
  release_tag="" asset_name="" asset_url="" asset_sha256=""
  json=$(app_github_releases "$repo")
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
  if [[ -z "$release_tag" ]]; then
    warn "No release in $repo matches tag '${tag_pattern:-<stable>}' and asset '$asset_pattern'"
    return 1
  fi
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
  local id="$1" tag="$2" staged="$3" root="$APP_OPT_DIR/$1" dest fresh=0 old
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

  old=$(app_current_tag "$id")
  if [[ -n "$old" && "$old" != "$tag" ]]; then
    app_relink "$old" "$root/previous"
  fi
  app_relink "$tag" "$root/current"
  app_integrate "$id"
  app_prune "$id"
  info "Installed $id $tag"
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

app_integrate() {
  local id="$1" dir="$APP_OPT_DIR/$1/current" launcher="$APP_BIN_DIR/$1" desktop icon
  mkdir -p "$APP_BIN_DIR" "$APP_DESKTOP_DIR"

  # Extra args go after the caller's so AppRun still sees its own flags
  # (e.g. wispr-flow --doctor) first; Electron parses switches anywhere.
  {
    printf '#!/bin/bash\n# Generated by hk-app from %s\n' "$app_conf"
    printf 'exec %q "$@"' "$dir/AppRun"
    if [[ ${#args[@]} -gt 0 ]]; then
      printf ' %q' "${args[@]}"
    fi
    printf '\n'
  } > "$launcher.new"
  chmod 0755 "$launcher.new"
  mv -T "$launcher.new" "$launcher"

  desktop=$(find "$dir/" -maxdepth 1 -name '*.desktop' | head -n1)
  if [[ -z "$desktop" ]]; then
    warn "$id ships no desktop entry; only the launcher was written"
    return 0
  fi
  icon=$(app_icon_path "$dir" "$desktop")
  # Replace the first word of every Exec (main entry and actions), keeping
  # bundled flags and field codes like %U.
  sed -E \
    -e "s#^Exec=(\"[^\"]*\"|[^ ]+)#Exec=$launcher#" \
    -e "s#^TryExec=.*#TryExec=$launcher#" \
    -e "s#^Icon=.*#Icon=$icon#" \
    "$desktop" | app_desktop_override > "$APP_DESKTOP_DIR/$id.desktop.new"
  mv -T "$APP_DESKTOP_DIR/$id.desktop.new" "$APP_DESKTOP_DIR/$id.desktop"
  update-desktop-database "$APP_DESKTOP_DIR" &>/dev/null
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
