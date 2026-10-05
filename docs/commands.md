# Command Reference

This page lists the `hk-*` commands you would normally run directly. These
names and arguments stay stable across updates; commands not listed here are
internal and can change. See [What updates keep
stable](updating.md#what-updates-keep-stable).

## Update

- `hk-version`
  Print the installed version: the release tag, or `vX.Y.Z-N-g<commit>`
  between releases, with `-dirty` when tracked files have local changes. See
  [Versions](updating.md#versions).
- `hk-update-available`
  Fetch the update source and print bar-widget JSON that is visible when new
  commits are waiting. The shipped bar polls it hourly; offline it reuses the
  last fetched state.
- `hk-update check`
  Report the staged revision, the last applied revision, package changes,
  pending migrations, and which `hk-app` AppImages have a newer release (this
  part queries GitHub) without changing anything.
- `hk-update all`
  Run `sync`, then `apply`, then `hk-app update`, then personal `post-update`
  hooks. The update menu launches this command in a terminal.
- `hk-update apps [--dry-run] [id...]`
  Update AppImages installed with `hk-app` (the same as `hk-app update`).
- `hk-update sync`
  Fetch the configured remote and branch, show the new changelog entries and
  incoming commits, and pin one confirmed commit in XDG state. It does not move
  the live checkout.
- `hk-update apply`
  Fast-forward to the staged revision, then install and review packages, run
  pending migrations, copy new starting configs, restow, rebuild the theme,
  and reload. Quickshell is stopped meanwhile and started again however apply
  ends. With nothing staged, reapply the current checkout, which also repairs
  links and generated output.
- `hk-update remove-stale`
  Remove Hyprkarl links in `~/.config` whose target no longer exists.
- `hk-update packages`
  Install newly required packages and review retired ones; `apply` runs it.
- `hk-config-seed`
  Create missing personal files and starting configs, never overwriting one;
  `apply` runs it.

## Lifecycle Hooks

- `hk-autostart`
  Start Hyprkarl's session services at login: the shell, the idle daemon, the
  wallpaper, the cursor, and `login` hooks. Hyprland runs it once; a personal
  version in `~/.local/bin` replaces it.
- `hk-hook-run <event>`
  Run the hooks in `~/.config/hyprkarl/hooks/<event>.d/` in name order. Events
  are `login`, `post-update`, `theme-set`, and `wallpaper-set`; Hyprkarl runs
  each at that moment.

## Menus and Launching

- `hk-shell menu [toggle|open] [menu-id]` / `hk-shell menu close`
  Open, toggle, or close a menu, such as `hk-shell menu toggle main`. It opens
  on the focused monitor, or on the clicked bar's monitor from a bar widget.
- `hk-shell launcher [toggle|open|close]`
  Control the application launcher.
- `hk-shell calculator [toggle|open|close]`
  Control the Quickshell calculator. Results come from `qalc`; choosing one
  copies it to the clipboard and stores up to five recent calculations in XDG
  state.
- `hk-shell wallpaper <set|remove|close>`
  Open the Quickshell thumbnail picker to set or remove a wallpaper.
- `hk-keybindings-list`
  Print the live Hyprland keybindings shown by the searchable `keybindings`
  shell menu.
- `hk-icon-data-update`
  Refresh the `icons` menu's Nerd Font glyph list from upstream.

### Launching apps

- `hk-audio-launch`
  Launch the audio controls TUI (`wiremix`).
- `hk-bluetooth-launch`
  Launch the bluetooth controls TUI (`bluetui`). Unblocks bluetooth via
  `rfkill` first.
- `hk-wifi-launch`
  Launch the Wi-Fi controls TUI (`wifitui`). Unblocks Wi-Fi via `rfkill`
  first.
- `hk-browser-launch [--private] [args...]`
  Launch the default browser as defined by `xdg-settings`. `--private` is
  translated to the right private-browsing flag for the detected browser
  (Firefox, Edge, Chromium, etc.).
- `hk-editor-launch [args...]`
  Launch the editor set in `$EDITOR` (with `nvim` as a fallback). Known TUI
  editors run inside the hyprkarl terminal; everything else runs detached.
- `hk-tui-launch <command> [args...]`
  Run a terminal program in a floating Hyprkarl terminal window, as the menus
  do for updates and package pickers.
- `hk-terminal-open [args...]`
  Open a terminal window with the hyprkarl terminal app-id, waiting for it
  to close before returning. Arguments are forwarded to `xdg-terminal-exec`.
  Use `hk-tui-launch` instead when you don't need to wait for the result.
- `hk-open-with <file>`
  Show the shared Quickshell application picker for opening a file. Its custom
  switch optionally makes the selected application the default for the file's
  MIME type before launching it.
- `hk-lock`
  Lock the session.

### Power

- `hk-suspend`
  Suspend. Hypridle locks the session first.
- `hk-reboot`
  Reboot through `hyprshutdown` with the standard countdown overlay.
- `hk-shutdown`
  Shut down through `hyprshutdown` with the standard countdown overlay.

### Screenshots

- `hk-screenshot <window|output|region> [hyprshot options]`
  Capture with Hyprshot while preserving an open Quickshell feature panel.
  Additional options pass through to Hyprshot. The default `Print` bindings
  use this command for window, display, and region capture.

## Themes and Wallpapers

- `hk-theme set <theme>`
  Build a built-in source, personal source, or built-in plus same-name
  personal overlay; make it the active theme; copy its GTK theme; then update
  the wallpaper and application settings and reload affected programs.
- `hk-theme list`
  List installed themes.
- `hk-theme current`
  Print the current theme name.
- `hk-wallpaper set <filename>`
  Set the current wallpaper for the active theme.
- `hk-wallpaper cycle`
  Switch to the next wallpaper in the active theme.
- `hk-wallpaper add <path>`
  Copy an image into the active theme's wallpaper directory and set it as the
  current wallpaper.
- `hk-wallpaper remove <filename>`
  Remove a wallpaper and its cached preview.
- `hk-wallpaper cache [--regenerate|--single <filename>]`
  Sync or rebuild wallpaper previews for the active theme.
- `hk-wallpaper init`
  Reapply the current wallpaper through `hyprpaper`.

## Fingerprint

- `hk-shell menu open fingerprint`
  Open the setup-aware fingerprint workflow. Enrollment uses a dynamic picker
  containing only available fingers; removal uses a dynamic picker containing
  only enrolled fingers. Every fingerprint menu is rendered by Quickshell.
- `hk-fingerprint setup [--remove]`
  Configure fingerprint authentication for sudo and polkit, or remove it with
  `--remove`.
- `hk-fingerprint enroll <finger-name>`
  Enroll the specified fingerprint. The shell menu owns finger selection.
- `hk-fingerprint remove <finger-name>`
  Delete an enrolled fingerprint.
- `hk-fingerprint list`
  Print enrolled fingers, one per line.

## Defaults and Session Behavior

- `hk-default-terminal <terminal>`
  Install a terminal and make it the default by writing
  `~/.config/xdg-terminals.list`.
- `hk-default-editor <editor>`
  Install an editor and record it as `$EDITOR` in `~/.config/uwsm/default`.
- `hk-default-shell <shell>`
  Install a shell and make it the login shell.
- `hk-timezone-setup`
  Set the system timezone.

## Packages

- `hk-pkg-upgrade`
  Upgrade all installed packages (pacman + AUR) non-interactively, then prompt
  to reboot. Intended to be launched via `hk-tui-launch hk-pkg-upgrade` so it
  opens in a floating terminal.
- `hk-pkg-install-tui`
  Open an `fzf` package picker to install pacman packages.
- `hk-pkg-install-tui --aur`
  Open an `fzf` package picker to install AUR packages.
- `hk-pkg-install-tui --flatpak`
  Open an `fzf` package picker to install Flatpak apps.
- `hk-pkg-remove-tui`
  Open an `fzf` package picker to uninstall pacman packages.
- `hk-pkg-remove-tui --flatpak`
  Open an `fzf` package picker to uninstall Flatpak apps.
- `hk-pkg install <package>...`
  Install named pacman packages.
- `hk-pkg install --aur <package>...`
  Install named AUR packages.
- `hk-pkg install --flatpak <app-id>...`
  Install named Flatpak app ids.
- `hk-pkg remove <package>...`
  Remove named packages if they are installed.
- `hk-pkg remove --flatpak <app-id>...`
  Remove named Flatpak app ids if they are installed.
- `hk-pkg missing <package>...`
  Return success if any named package is missing.
- `hk-pkg missing --flatpak <app-id>...`
  Return success if any named Flatpak is missing.
- `hk-pkg present <package>...`
  Return success if all named packages are installed.
- `hk-pkg present --flatpak <app-id>...`
  Return success if all named Flatpaks are installed.

## Apps (AppImages)

AppImages installed outside the package manager. Each app has a config,
`<id>.conf` (key reference at the top of `bin/lib/app.sh`). `hk-app install`
writes yours to `~/.config/hyprkarl/apps/`; Hyprkarl ships a few in
`defaults/config/hyprkarl/apps/`, and one of yours with the same name replaces
it. An app installs to `~/.local/opt/<id>/<tag>/`, with `current` and
`previous` links, a launcher at `~/.local/bin/<id>`, and a desktop entry.

- `hk-app install <owner/repo> [--channel REGEX] [--asset REGEX] [--id ID] [-- args...]`
  Install the newest GitHub release and write its config. `--channel` tracks
  tags matching a regex (e.g. `nightly`) and admits prereleases; the default is
  the newest stable release. Arguments after `--` are added to the launcher.
  The download is checked against GitHub's SHA-256 digest when the release
  publishes one.
- `hk-app install <url> [--sha256 HEX] [--id ID] [-- args...]`
  Install a direct AppImage URL. Manual installs are not updated; run
  `hk-app install <id>` to fetch the URL again. Each release is named
  `<version>-<hash>` after its bundled version and content, so a changed image
  gets its own release (and `hk-app rollback` works) even if the version did not.
- `hk-app install <id>`
  Install from an existing config, such as a shipped one or one copied from
  another machine. Takes no options: edit the config instead.
- `hk-app update [--dry-run] [id...]`
  Update installed apps to their newest matching release. Keeps the previous
  release and lists running apps that need a restart.
- `hk-app config-update [id...]`
  Re-apply configs to the installed release without downloading: rewrite the
  launcher and desktop entry and re-run the `post_install` command. Run it
  after editing a config or whatever `post_install` builds.
- `hk-app status [id...]`
  Show the installed and latest release of each app.
- `hk-app rollback <id>`
  Swap to the previous release.
- `hk-app restart <process-name>`
  Kill and relaunch a running app (`hk-app-restart`).

The menu's Install > AppImage entry asks for an `owner/repo` or URL
(`hk-app-install-tui`), and Update > Update Apps runs `hk-app update`.

## Docker

- `hk-shell menu open docker-install`
  Open the shell-native Docker install menu, populated with services that are
  not installed.
- `hk-shell menu open docker-uninstall`
  Open the shell-native Docker uninstall menu, populated with installed
  services.
- `hk-docker install <service>`
  Install a local Docker service.
- `hk-docker uninstall <service>`
  Uninstall a local Docker service.
- `hk-docker list`
  Print the supported Docker service ids.

## Quickshell Shell

These commands manage and communicate with the session-started production
shell.

- `hk-shell start`, `stop`, `restart`
  Start, stop, or restart the shell. `start` reports QML load errors.
- `hk-shell status`
  Print JSON with `running` and the running instances; exits nonzero when
  stopped.
- `hk-shell logs [qs log options]`
  Show the shell's log, the last 200 lines by default; options such as
  `--follow` pass through to `qs log`.
- `hk-shell notifications <dismiss|dismiss-all|toggle-silenced|restore>`
  Dismiss notifications, silence them, or bring back the last one dismissed.
- `hk-shell osd <kind> ...`
  Show an OSD popup on the focused monitor, for your own keybindings. A media
  percentage of `-1` leaves out the progress bar:

  ```text
  hk-shell osd volume <percent> [muted]
  hk-shell osd audio-output <percent> <muted> <description>
  hk-shell osd microphone <muted>
  hk-shell osd display-brightness <percent>
  hk-shell osd keyboard-brightness <percent>
  hk-shell osd media <playing|paused|next|previous> <percent|-1> <title> [artist]
  ```

## UI Helpers

- `hk-terminal-reload`
  Reload terminal configs for supported terminals.
- `hk-workspace-swap <target_num>`
  Swap all windows between the active workspace and the target workspace, then
  focus the target. Tiled windows will be retiled on arrival.

## Media, Hardware, and Utilities

- `hk-screen-record`
  Start or stop screen recording. Supports desktop audio, microphone audio,
  webcam overlays, and explicit resolution arguments.
- `hk-video-compress [input] [target_size] [options]`
  Two-pass compression of a video file to a target file size. Prompts via
  `gum` for missing arguments unless `--non-interactive` is set.
- `hk-picture-select [directory]`
  Open `yazi` as an image picker and print the chosen path. Defaults to
  `~/Pictures`.
- `hk-video-select [directory]`
  Open `yazi` as a video picker and print the chosen path. Defaults to
  `~/Videos`.
- `hk-nightlight [on|off|toggle]`
  Enable, disable, or toggle hyprsunset nightlight (warm color temperature +
  gamma dimming).
- `hk-caffeine [on|off|toggle|status]`
  Pause idle locking and sleep with a systemd idle inhibitor. Hypridle keeps
  running, so manual suspend and lid close still lock first.
- `hk-display <state|scale|toggle|brightness> [arguments]`
  The display panel's backend. `state [output]` prints JSON,
  `scale <output> <factor>` and `toggle <output>` change a monitor and save
  the layout, and `brightness <output> <percent>` sets a built-in screen's
  backlight. The panel also uses internal `arrange`, `preview`, `confirm`,
  and `revert` actions.
- `hk-playerctl`
  Control media playback and show track state in the shell OSD.
- `hk-volume`
  Adjust audio volume and show the current level.
- `hk-mic`
  Toggle microphone mute and show the current state.
- `hk-webcam`
  Open a webcam preview window.
- `hk-dictionary`
  Dictionary TUI powered by `fzf` and the FreeDict DICT server.
- `hk-wifi-restart`
  Unblock Wi-Fi.
- `hk-audio-restart`
  Restart the PipeWire audio service.
- `hk-btop-reload`
  Reload the running `btop` so it picks up theme changes.
- `hk-starship-reload`
  Rebuild the Starship prompt config from `~/.config/starship.toml` and the
  active theme's palette. `hk-theme set`, `hk-update apply`, and login run it;
  run it yourself after editing `~/.config/starship.toml`. See
  [Themes](themes.md#starship-prompt).

## Voice Commands (Wispr Flow)

Wispr Flow installs as an `hk-app` AppImage (`hk-app install wispr-flow`) with
a locally built helper swapped in. Login starts it in the tray, after
`hk-wispr-switch`.

- `hk-voice-command [--dry-run] <transcript>` / `--list` / `--join-mode MODE`
  Wispr Flow's transcript hook (`WISPR_TRANSCRIPT_HOOK` in `config/uwsm/env`).
  A transcript matching a phrase in the voice command file runs its command
  instead of being pasted; anything else is pasted, joined to the previous
  dictation in the same window. The file is
  `~/.config/hyprkarl/voice-commands.conf` if you have one, which replaces
  Hyprkarl's `defaults/config/hyprkarl/voice-commands.conf`; its header
  documents the syntax. `--list` prints the phrases for the focused app and
  everywhere, which the Utilities > Voice Commands menu shows (say "cheat
  sheet" to open it).
- `hk-voice-keys <step>...`
  Send keys (`CTRL+L`, `Return`) and text (`type:TEXT`) to the focused window.
- `hk-voice-launch <name>`
  Start the application whose name is, or starts with, the spoken words; with
  no single match, open the launcher. The "launch" and "open" phrases run it.
- `hk-wispr-word-add [--correction]`
  Open Wispr's "Add to vocabulary" dialog through AT-SPI, cursor in the word
  field; `--correction` sets it up as misspelling -> correct word.
- `hk-wispr-dictionary [output.csv|-]`
  Back up Wispr's personal dictionary as a CSV in Wispr's import format
  (default: `~/.config/hyprkarl/wispr-dictionary.csv`, outside the checkout so
  personal words stay out of the repo).
- `hk-wispr-helper-install [release-dir]`
  The `post_install` command in the `wispr-flow` app recipe: builds
  `wispr-flow-linux-helper` from the `vendor/wispr-flow-helper` submodule
  (the `local` branch of
  [ejarmand/wisprflow-linux-helper](https://github.com/ejarmand/wisprflow-linux-helper),
  fetched on first use; set `WISPR_HELPER_SRC` to build another checkout) and
  swaps it into the release, keeping the shipped helper as `.orig`. Rebuild
  and reinstall it with `hk-app config-update wispr-flow`; to pick up new
  helper commits, run `git submodule update --remote vendor/wispr-flow-helper`
  and commit the new pin. `hk-update apply` keeps a fetched submodule at the
  pinned commit.
- `hk-wispr-transcripts [--no-audio] [--since YYYY-MM-DD] [DIR]`
  Export Wispr's dictation history (raw speech recognition, cleaned and pasted
  text, audio) to `~/Documents/wispr-exports/` for review.
- `hk-wispr-switch [run|on|off|toggle|status]`
  Make a USB mic's hardware mute switch drive Wispr hands-free: unmuting starts
  it, muting stops it (by pressing Ctrl+Super+Space on a virtual keyboard, which
  is why that shortcut is left unbound). It hears the switch as exact digital
  silence, stays out of the way while another app records from the mic, and
  ignores software mutes. Login starts it before Wispr, whose helper only finds
  keyboards at launch; restart Wispr after restarting it. `off` and `toggle`
  (`Super+Alt+D`) pause it until the next login. The mic is
  `$HK_WISPR_SWITCH_SOURCE` (default: the Jounivo JV601); it logs to
  `journalctl --user -t hk-wispr-switch`.

## Internal Helpers

Other scripts, keybindings, and bar widgets call these; they can change in
any release:

- Launching glue: `hk-app-restart`
- Hardware actions bound to function keys: `hk-brightness-display`,
  `hk-brightness-keyboard`, `hk-audio-switch`, `hk-battery-monitor`; display
  dispatcher actions: `hk-display-state`, `hk-display-arrange`,
  `hk-display-preview`, `hk-display-confirm`, `hk-display-revert`,
  `hk-display-scale`, `hk-display-toggle`, `hk-display-brightness`; internal
  timeout helper: `hk-display-watch`
- Menu row providers: `hk-voice-command-menu-entries` (the voice command cheat
  sheet)
- Notification helpers: `hk-battery-notify`, `hk-notify-window-class`,
  `hk-show-done`, `hk-suggest-reboot`
- Lookup helpers: `hk-battery-find`, `hk-icon-find`, `hk-cmd-present`,
  `hk-terminal-cwd`

## Notes

For editing conventions, see [Repo Conventions](repo-conventions.md) and
[Command Script Style](shell-style.md).
