# Lady with a Hat and Feather Boa

The palette was chosen after downloading and visually inspecting the original reproduction of Gustav Klimt's *Lady with a Hat and Feather Boa*, 1909.

Source image: [Wikimedia Commons file page](https://commons.wikimedia.org/wiki/File:Gustav_Klimt_009.jpg). The original is 2024 × 2501 pixels, from The Yorck Project's 2002 reproduction collection. The file page identifies the artwork and the individual reproduction as public domain, and distinguishes the collection's compilation copyright under the GNU Free Documentation License. This palette's plain background is generated from `base.background`.

The same file page requests a US public-domain tag. Its existing life-term and Yorck PD-Art statements do not resolve that gap. The reproduction was used locally as a palette reference and is not bundled. The only shipped wallpaper is `wallpapers/01-default.png`.

## Palette choices

Violet from the hat, copper rose from the hair and background, ivory from the glove and face, and warm near-black from the feather boa. These are visual adaptations rather than exact pigment measurements. Surfaces are darkened, text is lifted toward cream, and terminal and status colours are brightened to remain readable. Some subdued cool hues are extended into blue and cyan terminal roles so commands and diagnostics retain distinct colours.

`palette.yaml` is the colour source. `templates/` preserves Vera-dark's current bar layout and application overrides, with a palette-driven Starship template. It includes no wallpaper copies. GTK uses the installed name `hyprkarl`; Qt files point to the active theme; Foot supports both colour sections; Neovim retains a dark background.

## Generation and checks

Generator: [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator), revision `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e`.

Run from the pinned generator checkout, with `HYPRKARL_PATH` set to the Hyprkarl checkout and the generator's dependencies and `sassc` installed:

```bash
python - <<'PYGEN'
import os
from pathlib import Path
import generate

root = Path(os.environ["HYPRKARL_PATH"])
generate.PALETTES_DIR = root / "themes"
name = "klimt-boa"
generate.generate(name, root / "themes" / name)
PYGEN
```

This reads the preserved palette and overrides directly and leaves the wallpaper directory intact. Regenerate the plain background with ImageMagick using `magick -size 3840x2160 xc:<base.background> wallpapers/01-default.png` from this theme directory.

Generation completed successfully, including GTK 3 and GTK 4 CSS. Generated TOML files parse, generated configuration has no unresolved template expressions, and bar layout matches Vera-dark.

Contrast was calculated independently with WCAG relative luminance from linear sRGB. Across all five dark surface layers, minimum text/status contrast is 4.56:1. Selection contrast is 8.05:1. The actual prompt's hardcoded purple OS/hostname segment has 4.98:1 contrast; the four palette-controlled segment fills have at least 7.12:1. Python/Kubernetes text has 6.19:1. Green, red and purple character glyphs remain bright, with at least 10.07:1.

Yazi's error-progress text uses the dark background colour on the error fill, giving 7.26:1. Btop explicitly uses the primary foreground. Qt active and inactive placeholders use the opaque secondary foreground, with at least 6.04:1 across the theme surfaces.

All listed pairs meet 4.5:1. The existing prompt also uses `color_yellow` for both a directory-segment background and a Vim visual-mode glyph. This palette keeps the segment readable; the shared yellow glyph role remains a limitation of that prompt layout. These checks cover opaque palette colours; wallpaper overlays and application-specific opacity can change effective contrast.

The plain background is 3840 × 2160 pixels, filled with `#191418`. No active theme was switched.
