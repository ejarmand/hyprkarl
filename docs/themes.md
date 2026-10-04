# Themes

Hyprkarl themes are directories under `themes/`. The active theme is selected
by updating symlinks under `config/hyprkarl/current/`.

## How Theme Selection Works

The active theme state lives in `config/hyprkarl/current/`:

- `theme`
  relative symlink to `../../../themes/<name>`
- `theme.name`
  active theme name
- `wallpaper`
  symlink to the current wallpaper inside the active theme

When you run:

```bash
hk-theme set <theme-name>
```

Hyprkarl:

- updates `config/hyprkarl/current/theme`
- writes `config/hyprkarl/current/theme.name`
- updates the wallpaper state
- updates GNOME and QT themes
- reloads Hyprland, mako, terminals, and `btop`
- rebuilds the Starship prompt config (`hk-starship-reload`)
- restarts AGS (picks up the new `bar.scss`)

## Switch the Active Theme

The usual way to switch themes is `Hyprkarl Menu -> Config -> Theme`, but you
can also run:

```bash
hk-theme set <theme-name>
```

To list installed themes, run:

```bash
hk-theme list
```

## Vera light and dark

`vera-light` and `vera-dark` take their colors from a private painting.
The artwork stays local. Both ship a plain background matching their palette
as `wallpapers/01-default.png`. The light theme uses cream paper and dark blue text;
the dark theme uses a deep blue background and cream text. Cobalt marks active
windows, teal marks success, raspberry marks errors, and lavender adds a
second accent. Yellow becomes darker ochre in light mode so it stays readable.

| Color | `vera-light` | `vera-dark` |
| --- | --- | --- |
| Background | `#f6f3e9` | `#141e2a` |
| Foreground | `#253b4b` | `#edeade` |
| Blue | `#275f89` | `#86b6db` |
| Teal | `#1e6558` | `#82bfaa` |
| Lavender | `#6e4a82` | `#b4a0d4` |
| Raspberry | `#a12b51` | `#ef7c9c` |
| Ochre / yellow | `#805c21` | `#e6cf8d` |

```bash
hk-theme set vera-light
hk-theme set vera-dark
```

To use your own wallpaper, select the theme first, then run
`hk-wallpaper add /path/to/your/image.jpg`. Repeat for the other variant if
you want the same wallpaper in both. Locally added wallpapers are ignored
by Git; only the plain default backgrounds ship with these themes.

They cover the same applications as the existing themes, including GTK 3/4,
Qt 5/6, Neovim, and all four terminals. Their bar layout matches `hyprkarl`.
Only `vera-light` has `light.mode`; its GTK settings and Neovim background also
select light mode. Foot supplies matching `[colors-dark]` and `[colors-light]`
sections so terminal color-scheme detection preserves the selected palette.
Both keep the GTK installation name `hyprkarl`, which matches the stowed
theme bundle. Their Qt palette paths target `/home/earmand/.config/`; update
those paths when installing on a different account.

### Regenerate the Vera themes

Each theme keeps its source palette in `palette.yaml` and template overrides
in `templates/`. The original generation used companion generator commit
`2645fecd819980f7f1c4482cc52deaeb5fc4ee6e`. Use its dependencies and `sassc`
as described in that project's README. Run the following from the generator
checkout, with `HYPRKARL_PATH` pointing to this repository:

```bash
for name in vera-light vera-dark; do
  mkdir -p "palettes/$name/templates/wallpapers"
  cp "$HYPRKARL_PATH/themes/$name/palette.yaml" "palettes/$name/"
  cp -a "$HYPRKARL_PATH/themes/$name/templates/." "palettes/$name/templates/"
  cp "$HYPRKARL_PATH/themes/$name/wallpapers/01-default.png" \
    "palettes/$name/templates/wallpapers/"
done
python generate.py vera-dark
python - <<'PY'
import colloid
from generate import generate

compile_sass = colloid._run_sassc

def compile_light(source, destination):
    source = source.with_name(source.name.replace("-Dark", "-Light"))
    compile_sass(source, destination)

colloid._run_sassc = compile_light
generate("vera-light")
PY
for name in vera-light vera-dark; do
  cp -a "output/$name/." "$HYPRKARL_PATH/themes/$name/"
done
```

The light build selects Colloid's Light SCSS entrypoints because this version
of the generator hardcodes Dark entrypoints. The light theme's internal
palette override supplies the light-to-dark GTK grey scale. Keep both when
regenerating. The commands above preserve `palette.yaml` and `templates/` in
the installed theme directories.

## Theme Contents

The simplest way to create a theme is to copy an existing one and keep the same
layout.

A full theme in this repo includes:

- `hyprland.lua`
  Theme-specific Hyprland styling (Lua — Hyprland's config is Lua since 0.55).
  The main Hyprland config loads it last via `loadfile`, so it overrides earlier
  settings. Typically just the active border color, e.g.
  `hl.config({ general = { col = { active_border = "rgb(63005A)" } } })`.
- `hyprlock.conf`
  Lock screen styling
- `hyprtoolkit.conf`
  Hyprtoolkit styling
- `bar.scss`
  AGS bar colors, spacing, radii, and typography
- `rofi.rasi`
  Rofi styling
- `mako.ini`
  Notification styling
- `alacritty.toml`, `foot.ini`, `ghostty.conf`, `kitty.conf`
  Terminal colors
- `btop.theme`
  `btop` colors
- `wifitui.toml`
  `wifitui` colors
- `yazi.toml`
  Yazi theme settings
- `qt5ct/qt5ct.conf`, `qt5ct/style-colors.conf`
  Qt5 color palette and widget style settings
- `qt6ct/qt6ct.conf`, `qt6ct/style-colors.conf`
  Qt6 color palette and widget style settings
- `gtk-3.0/settings.ini`, `gtk-4.0/settings.ini`
  GTK settings files (stowed to `~/.config/gtk-{3,4}.0/`); point GTK apps to
  the theme name and set the dark/light preference
- `gtk-theme/`
  The GTK theme bundle stowed to `~/.local/share/themes/hyprkarl/`.
  Contains `index.theme` (theme metadata) and the GTK3/4 stylesheets under
  `gtk-3.0/` and `gtk-4.0/` (`gtk.css`, `gtk-dark.css`, and assets).
  GTK apps read their colors from here.
- `nvim/colorscheme.lua`, `nvim/custom-colors.lua`
  Neovim colors
- `wallpapers/`
  Wallpapers available to `hk-wallpaper`

Optional theme files:

- `light.mode`
  Switches GNOME to `prefer-light`. Without it, Hyprkarl uses `prefer-dark`.
- `icons.theme`
  Single-line file naming the icon theme. Applied via `gsettings` on theme
  switch and embedded in `gtk-theme/index.theme`.
- `icons/`
  Theme-local icons used by Hyprkarl helpers and notifications.
- `starship.toml`
  A `[palettes.hyprkarl]` table for the Starship prompt. See
  [Starship Prompt](#starship-prompt).

## Starship Prompt

Starship has no include mechanism, so Hyprkarl builds the prompt config.
`hk-starship-reload` reads your layout from `~/.config/starship.toml`. If the
active theme has a `starship.toml`, the command appends that file's
`[palettes.hyprkarl]` table and selects it with `palette = 'hyprkarl'`, in
place of the layout's own top-level `palette` line. Otherwise it copies the
layout unchanged. The result goes to `~/.local/state/hyprkarl/starship.toml`,
and `config/uwsm/env` points `STARSHIP_CONFIG` there. Open shells pick up the
new colors at their next prompt.

`hk-theme set` and login run the command. Run `hk-starship-reload` yourself
after you edit `~/.config/starship.toml`. Edits to the generated file are lost.

A layout uses the palette by referring to color names instead of hex values,
for example `bg:color_blue fg:color_fg0`. The theme palettes define these
keys:

| Key | Use |
| --- | --- |
| `color_fg0` | Text on the colored segments |
| `color_fg1` | Text on the `color_bg1` and `color_bg3` segments |
| `color_bg1`, `color_bg3` | Surface segments at the end of the line |
| `color_purple`, `color_orange`, `color_yellow`, `color_aqua`, `color_blue` | Segment backgrounds, in order along the prompt |
| `color_green`, `color_red` | Success and error prompt characters |

Keep the layout's own palette, such as `[palettes.gruvbox_dark]`, so the
layout still works under themes without a `starship.toml` and on machines
without Hyprkarl. Don't define `[palettes.hyprkarl]` in the layout, because the
merged file would then contain the table twice. Only `vera-light` and
`vera-dark` ship a Starship palette.

## Create a New Theme

There are two ways to make a theme.

### Generate one from a color palette (recommended)

The themes shipped with Hyprkarl are produced by a companion tool,
[hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator).
It renders an entire theme — every file listed under
[Theme Contents](#theme-contents) — from a single YAML color palette, so the
colors stay consistent across Hyprland, the bar, terminals, GTK, Qt, and the
rest. It's the easiest path if you're building a new look, and it pairs well
with an LLM: hand it a terminal colorscheme (or describe the mood you want) and
have it write the palette.

```bash
git clone https://github.com/KarlJussila/hyprkarl-theme-generator.git
cd hyprkarl-theme-generator
# create palettes/my-theme/palette.yaml (see that repo's AGENTS.md), then:
python generate.py my-theme
export HYPRKARL_PATH=~/.local/share/hyprkarl
./sync_theme.sh my-theme          # installs it into themes/my-theme/
hk-theme set my-theme
```

### Copy an existing theme

For quick tweaks to an existing look, copy a theme directory and edit it in place:

```bash
cd ~/.local/share/hyprkarl
cp -a themes/hyprkarl themes/my-theme
```

Then edit the copied files and activate it:

```bash
hk-theme set my-theme
```

Starting from an existing theme is easier than building one from scratch,
because the repo already expects a specific file layout.

## Wallpapers in Themes

Wallpapers are stored in each theme's `wallpapers/` directory.

To add a wallpaper to the current theme, you can run:

```bash
hk-wallpaper add /path/to/image.png
```

That copies the file into the current theme's `wallpapers/` directory, rebuilds
its thumbnail, and sets it as the current wallpaper.

You can also add wallpapers manually by copying image files into:

```text
themes/<theme>/wallpapers/
```

Then rebuild that theme's thumbnail cache:

```bash
hk-wallpaper cache
```

Wallpaper commands always operate on the active theme:

```bash
hk-wallpaper set <filename>
hk-wallpaper cycle
hk-wallpaper remove <filename>
hk-wallpaper cache [--regenerate|--single <filename>]
```

## Sharp Edges

- Missing theme files do not always fail loudly.
- To restore wallpaper state, use:

```bash
hk-wallpaper init || hk-wallpaper cycle
```

## Related Docs

- [Using Hyprkarl](using-hyprkarl.md)
- [Command Reference](commands.md)
- [Extending Hyprkarl](extending-hyprkarl.md)
