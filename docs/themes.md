# Themes

Hyprkarl keeps theme source and generated runtime output separate:

```text
themes/<name>/                                  shipped authoring source
${XDG_CONFIG_HOME:-$HOME/.config}/hyprkarl/
└── themes/<name>/                              personal source or overlay
${XDG_STATE_HOME:-$HOME/.local/state}/hyprkarl/
├── current/theme -> ../themes/<name>.<timestamp>   the active build
└── themes/<name>.<timestamp>/                     the generated build
```

Generated builds do not live in Git or the personal configuration directory.
The GTK theme is also copied to `~/.local/share/themes/hyprkarl/`, because
GTK does not reliably follow symlinked theme directories.

## Switch themes

Use `Hyprkarl Menu -> Config -> Theme` or run:

```bash
hk-theme set <theme-name>
```

List available source themes with:

```bash
hk-theme list
```

Hyprkarl ships `hyprkarl`, `everforest`, `gruvbox`, `loam`, and
`tokyo-night`; this fork adds [`vera-light` and `vera-dark`](#vera-light-and-dark). The Tokyo Night source uses the original dark Night variant.
Loam uses warm brown surfaces and a narrow olive, ochre, and bark palette. It
began as an adaptation of Melange and retains the upstream attribution in its
source directory.

Every selection rebuilds the theme. `hk-theme set`:

1. loads the built-in source, personal source, or both;
2. merges and resolves the typed value graph;
3. renders and validates every consumer into a new build directory;
4. points `current/theme` at that build and deletes older builds;
5. copies the GTK theme and sets the GTK desktop settings;
6. reloads affected consumers.

A failed build leaves the active theme unchanged. Quickshell notices the switch
and reloads without restarting.

## Vera light and dark

`vera-light` and `vera-dark` take their colors from a private painting.
The artwork stays local and out of the repository. Both ship a plain
background matching their palette as `wallpapers/01-default.png`. The light
theme uses cream paper and dark blue text; the dark theme uses a deep blue
background and cream text. Cobalt marks active windows, teal marks success,
raspberry marks errors, and lavender adds a second accent. Yellow becomes
darker ochre in light mode so it stays readable.

| Color | `vera-light` | `vera-dark` |
| --- | --- | --- |
| Background | `#f6f3e9` | `#141e2a` |
| Foreground | `#253b4b` | `#edeade` |
| Blue | `#275f89` | `#86b6db` |
| Teal | `#1e6558` | `#82bfaa` |
| Lavender | `#6e4a82` | `#b4a0d4` |
| Raspberry | `#a12b51` | `#ef7c9c` |
| Ochre / yellow | `#805c21` | `#e6cf8d` |

Each is a single `theme.yaml` plus a Starship palette in
`overrides/starship.toml`. `vera-light` sets `mode: light`, which selects
Colloid's light GTK build and the light desktop preference, Neovim's light
background, and foot's light color section. Both route selection, btop,
wifitui, Qt, Neovim search, and GTK accent colors through the [consumer
color roles](#generated-bundle) so pale soft accents never carry text. To use
your own wallpaper, select the theme, then run `hk-wallpaper add <image>`.

## Source layout

A source may contain:

```text
<name>/
├── theme.yaml
├── overrides/
├── wallpapers/
├── icons/
└── previews/
```

- `theme.yaml` contains typed values and Jinja expressions.
- `overrides/<relative-template-path>` completely replaces one compiler
  template at the same relative path.
- `wallpapers/` contains wallpaper assets. By convention, `01-*` is primary.
- `icons/` adds or replaces generated theme-local icons.
- `previews/` contains repository screenshots such as `busy.png`,
  `launcher.png`, `menu.png`, and `wallpapers.png`.

Set `desktop.icon_theme` to the installed icon family that best fits the
palette. For example, Loam uses `Yaru-olive-dark` and Tokyo Night uses
`Yaru-blue-dark`.

Set `desktop.cursor_theme` to an installed cursor theme in
`/usr/share/icons/` or `~/.local/share/icons/`; it defaults to `Adwaita`.
Activating a theme points the default cursor,
`~/.local/share/icons/default/index.theme`, at it, and sets Hyprland's own
cursor. Apps that draw their own cursor pick up a change when they restart.
Cursor size is not part of the theme: set `XCURSOR_SIZE` and `HYPRCURSOR_SIZE`
in `~/.config/hypr/hyprland.local.lua` and start a new session.

Themes may also opt into the shared Hyprkarl wallpaper:

```yaml
wallpaper:
  generate_default: true
```

The compiler writes `01-hyprkarl-wallpaper.png` using `base.background`,
`accent.primary.base`, and `accent.primary.soft`. A theme may override the
corresponding `wallpaper.background`, `wallpaper.accent`, and
`wallpaper.accent_dim` values. Generation is independent of authored assets,
so the theme may include other files under `wallpapers/` at the same time. An
authored file named `01-hyprkarl-wallpaper.png` wins over the generated one.
The default is `generate_default: false`.

A personal-only theme requires `theme.yaml`. A personal directory with the
same name as a built-in is a sparse overlay and may omit it. That makes small
changes practical. For example:

```text
~/.config/hyprkarl/themes/hyprkarl/
└── theme.yaml
```

```yaml
metrics:
  border:
    standard: 3

shell:
  bar:
    margin:
      screen: 4
```

Run `hk-theme set hyprkarl` after editing it.

## Merge and rendering order

The value graph resolves in this order:

```text
theme-generator/defaults/theme.yaml
  -> themes/<name>/theme.yaml
  -> ~/.config/hyprkarl/themes/<name>/theme.yaml
  -> recursive native Jinja resolution
```

Objects merge recursively. Arrays and scalar values replace earlier values.
Whole-value expressions retain native strings, integers, decimals, and
booleans. Theme authors may define their own structures and reference them from
consumer values. The shipped `metrics`, `motion`, and `typography` names are
defaults, not an allowlist.

Templates and assets use the same ownership order:

```text
compiler template or asset -> built-in replacement -> personal replacement
```

An override replaces a whole template. It does not introduce a second merge
language. Personal wallpaper files add to or replace built-in files.
`.wallpapers-disabled` records inherited wallpaper paths that should be absent
from the generated bundle.

## Create a personal theme

Start from a shipped source, not a generated bundle:

```bash
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/hyprkarl/themes/my-theme"
cp ~/.local/share/hyprkarl/themes/hyprkarl/theme.yaml \
  "${XDG_CONFIG_HOME:-$HOME/.config}/hyprkarl/themes/my-theme/theme.yaml"
$EDITOR "${XDG_CONFIG_HOME:-$HOME/.config}/hyprkarl/themes/my-theme/theme.yaml"
hk-theme set my-theme
```

Keys outside `shell` stay stable across updates; the detailed `shell` keys can
be renamed in a release, with a changelog note. Prefer the stable keys in a
personal theme. See [What updates keep stable](updating.md#what-updates-keep-stable).

The shared compiler defaults provide fonts, spacing, radii, border widths,
motion, and the complete Quickshell appearance shape. Most new sources only
need palette values and intentional changes.

For direct compiler work, run the module from `theme-generator/`:

```bash
cd ~/.local/share/hyprkarl/theme-generator
python -m theme_generator preview hyprkarl
python -m theme_generator preview hyprkarl -o /tmp/hyprkarl-palette.png
python -m theme_generator capture hyprkarl
python -m theme_generator build hyprkarl -o /tmp/hyprkarl-theme
python -m theme_generator build hyprkarl \
  --overlay ~/.config/hyprkarl/themes/hyprkarl \
  -o /tmp/hyprkarl-theme
python -m theme_generator validate
python -m pytest -q
```

These are authoring and test commands. `hk-theme set` remains the public
build-and-activate action. There is no sibling generator checkout, compiler
sync command, or `hk-theme build` action.

`preview` prints a terminal palette and renders a graphical palette board.
`capture` activates the theme and creates the standard palette, busy desktop,
launcher, menu, and wallpaper-picker images under the source's `previews/`
directory. It uses empty numbered workspace 4 by default and refuses to touch
one that already contains windows. Use `--workspace 9`, for example, when 4 is
occupied. The command recreates the established tiled busy layout, stages the
volume OSD and one notification, controls hover selection, then restores the
previous workspace and pointer position. Preview files are published only
after the complete capture succeeds.

## Generated bundle

The compiler renders the resolved graph into consumer files for:

- Quickshell (including the lock screen), Hyprland, and Hyprtoolkit;
- Alacritty, foot, Ghostty, Kitty, `btop`, `wifitui`, Yazi, and Neovim;
- fastfetch's whole config, logo included;
- Qt 5 and Qt 6 palettes and settings;
- GTK 3 and GTK 4, including a palette-derived Colloid theme;
- the cursor theme name, theme metadata, icons, wallpapers, and previews.

`quickshell.json` holds the shell's appearance; see [Shell
appearance](#shell-appearance).

Fastfetch belongs to the theme entirely. Its `fastfetch` keys set the logo's
`mark` and `wordmark` colors, the `labels` and `title` colors, and the
`modules` list; an `overrides/config/fastfetch/config.jsonc` template replaces
the layout or the logo art. A `~/.config/fastfetch/config.jsonc` of your own
takes precedence over every theme.

A few consumers take colors by role, and a theme can point a role at another
palette value without overriding the template:

| Key | Default | Used for |
|---|---|---|
| `terminal.selection_fg`, `terminal.selection_bg` | `base.background`, `ui.cursor` | Selected text in foot and Ghostty |
| `btop.main_fg` | empty (btop's own) | btop's text |
| `btop.highlight` | `accent.secondary.soft` | btop's highlighted keys and graph starts |
| `wifitui.subtle` | `accent.secondary.soft` | wifitui's subtle text |
| `qt.highlight` | `accent.secondary.base` | Qt's selection highlight |
| `qt.placeholder`, `qt.placeholder_disabled`, `qt.highlighted_text_disabled` | `base.foreground_muted`, `base.foreground_dim`, `base.foreground` | Qt's placeholder text and disabled selected text; each has an `_alpha` key, a two-digit hex opacity (`80`, `80`, `66`) |
| `yazi.progress_error_fg` | `status.warning` | Text on Yazi's error progress bar |
| `nvim.terminal_color_8`, `nvim.search_fg`, `nvim.search_bg` | empty: the surface color, and the background on the primary accent | Neovim's terminal color 8 and search matches |
| `gtk.accent`, `gtk.accent_bright` | `accent.secondary.base`, `accent.secondary.bright` | Colloid's accent and links |

For example, a light theme whose soft accents are pale points the btop and
wifitui roles at readable colors:

```yaml
btop:
  highlight: "{{accent.secondary.base}}"
wifitui:
  subtle: "{{base.foreground_muted}}"
```

`mode: light` also selects Neovim's light background and gives foot a matching
`[colors-light]` section.

The generated `theme.yaml` contains the fully merged and resolved graph for
inspection. It is output, not the next authoring source.

## Starship prompt

Starship has no include mechanism, so Hyprkarl builds the prompt config.
`hk-starship-reload` reads your layout from `~/.config/starship.toml`. If the
active theme renders a `starship.toml`, the command appends that file's
`[palettes.hyprkarl]` table and selects it with `palette = 'hyprkarl'`, in
place of the layout's own top-level `palette` line. Otherwise it copies the
layout unchanged. The result goes to `~/.local/state/hyprkarl/starship.toml`,
and `config/uwsm/env` points `STARSHIP_CONFIG` there. Open shells pick up the
new colors at their next prompt.

`hk-theme set`, `hk-update apply`, and login run the command. Run
`hk-starship-reload` yourself after you edit `~/.config/starship.toml`. Edits
to the generated file are lost.

A theme ships its palette as an `overrides/starship.toml` template, since no
shared template exists for it; it may use palette expressions such as
`{{base.foreground}}`. A layout uses the palette by referring to color names
instead of hex values, for example `bg:color_blue fg:color_fg0`. The theme
palettes define these keys:

| Key | Use |
| --- | --- |
| `color_fg0` | Text on the colored segments |
| `color_fg1` | Text on the time segment (`color_bg1`) |
| `color_fg2` | Text on the Docker and Conda segments (`color_bg3`) |
| `color_bg1`, `color_bg3` | Surface segments at the end of the line |
| `color_magenta`, `color_orange`, `color_yellow`, `color_aqua`, `color_blue` | Segment backgrounds, in order along the prompt |
| `color_green`, `color_red`, `color_purple` | Prompt character for success, error, and Vim replace mode |

Keep the layout's own palette, such as `[palettes.gruvbox_dark]`, so the
layout still works under themes without a Starship palette and on machines
without Hyprkarl. Don't define `[palettes.hyprkarl]` in the layout, because the
merged file would then contain the table twice.

## GTK output

The active build contains a `gtk-theme/` directory. `hk-theme set` copies it
to:

```text
~/.local/share/themes/hyprkarl/
```

This is a real copy because GTK discovery and asset loading have been
unreliable through symlinked theme directories, so do not replace it with a
symlink. Edit theme source and select the theme again instead of editing
the installed copy. Dark sources compile Colloid's dark variant; `mode: light`
compiles its light variant. Hyprkarl's linked `~/.config/gtk-3.0/settings.ini`
and `gtk-4.0/settings.ini` select the stable `hyprkarl` theme name, and its
linked `gtk.css` files import the installed copy; `hk-theme set` applies the
light/dark preference through desktop settings. Qt follows the theme too:
`hk-theme set` writes `~/.config/qt5ct/qt5ct.conf` and `qt6ct.conf` with the
theme's palette, fonts, and icon family.

## Shell appearance

Everything the shell draws comes from the theme's `shell` object, which the
build writes to `quickshell.json`; the running shell picks up a theme switch
without restarting. Its groups are `palette`, `surfaces`, `typography`,
`metrics`, `switch`, `bar`, `panel`, `tooltip`, `osd`, `notification`,
`polkit`, `lock`, `menu`, `applicationPicker`, `calculator`,
`wallpaperPicker`, and `displayArrangement`.
`theme-generator/defaults/theme.yaml` lists every value with its default.
Most defaults derive from the palette, so a palette change already reaches the
shell; set a single value under `shell.<group>` to change just that.

The bar's island shapes are relative to the bar, so one theme works for top
and bottom bars. `screen` faces the monitor edge, `content` the windows,
`outer` the monitor's side, and `inner` the neighboring island:

```yaml
shell:
  bar:
    island:
      corners:
        screenOuter: square
        screenInner: curve    # concave join; corners are otherwise square or round
        contentOuter: square
        contentInner: round
      borders:
        screen: false
        content: true
        outer: false
        inner: true
```

## Wallpapers

Built-in wallpapers live in `themes/<name>/wallpapers/` and yours in
`~/.config/hyprkarl/themes/<name>/wallpapers/`, which updates never touch.
Each theme build links both sets into its `wallpapers/` folder by filename;
your file wins over a built-in one with the same name. Built-in wallpapers
you remove are listed in that theme's `.wallpapers-disabled` file and stay
gone through updates, while new built-in ones appear on the next
`hk-update apply`.

`hk-wallpaper add` copies an image into your folder and rebuilds the theme; a
file you place there yourself appears after the next `hk-theme set`.
`hk-wallpaper remove` deletes your file or disables a built-in one, along with
its thumbnail. The picker keeps thumbnails in `~/.cache/hyprkarl/wallpapers/`
and regenerates one when its wallpaper changes.

```bash
hk-wallpaper set <filename>
hk-wallpaper cycle
hk-wallpaper add /path/to/image.png
hk-wallpaper remove <filename>
hk-wallpaper cache [--regenerate|--single <filename>]
```

The current selection lives in XDG state. To recover an invalid selection,
run:

```bash
hk-wallpaper init || hk-wallpaper cycle
```

## Related docs

- [Using Hyprkarl](using-hyprkarl.md)
- [Command reference](commands.md)
- [Extending Hyprkarl](extending-hyprkarl.md)
