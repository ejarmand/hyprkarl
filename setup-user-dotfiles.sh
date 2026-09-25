#!/bin/bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <dotfiles-repo-url>"
  exit 1
fi

REPO_URL="$1"
INSTALL_DIR="$HOME/.local/share/user-dotfiles"

for cmd in git stow; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Error: required command '$cmd' is not installed."
    exit 1
  fi
done

if [ -e "$INSTALL_DIR" ] && [ ! -d "$INSTALL_DIR/.git" ]; then
  echo "Error: $INSTALL_DIR exists but is not a git repository."
  exit 1
fi

if [ -d "$INSTALL_DIR/.git" ]; then
  CURRENT_REMOTE="$(git -C "$INSTALL_DIR" config --get remote.origin.url || true)"

  if [ "$CURRENT_REMOTE" != "$REPO_URL" ]; then
    echo "Error: $INSTALL_DIR is already cloned from a different remote:"
    echo "  current: $CURRENT_REMOTE"
    echo "  wanted:  $REPO_URL"
    exit 1
  fi
else
  git clone --depth=1 "$REPO_URL" "$INSTALL_DIR"
fi

stow_package() {
  local package="$1"
  local target="$2"

  if [ ! -d "$INSTALL_DIR/$package" ]; then
    return
  fi

  mkdir -p "$target"

  # Remove any existing symlinks from a prior stow run, then adopt conflicts so
  # the cloned repo can take ownership of the live files before restoring its
  # tracked versions.
  stow -D --dir="$INSTALL_DIR" --target="$target" "$package" 2>/dev/null || true
  stow --dir="$INSTALL_DIR" --target="$target" "$package" --adopt --no-folding
  git -C "$INSTALL_DIR" checkout -- "$package"
}

stow_package "config" "$HOME/.config"
stow_package "applications" "$HOME/.local/share/applications"
stow_package "bin" "$HOME/.local/bin"
stow_package "home" "$HOME"

if command -v hyprctl >/dev/null 2>&1; then
  hyprctl reload || true
fi

echo "Installed user dotfiles from $REPO_URL into $INSTALL_DIR"
