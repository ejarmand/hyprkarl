# Portrait of Adele Bloch-Bauer II

The palette was chosen after downloading and visually inspecting the original reproduction of Gustav Klimt's *Portrait of Adele Bloch-Bauer II*, 1912.

Source image: [Wikimedia Commons file page](https://commons.wikimedia.org/wiki/File:Gustav_Klimt_047.jpg). The original is 1576 × 2590 pixels, from The Yorck Project's 2002 reproduction collection. The file page identifies the artwork and the individual reproduction as public domain, and distinguishes the collection's compilation copyright under the GNU Free Documentation License. This palette's plain background is generated from `base.background`.

The file page includes a US pre-1931 publication/registration statement and PD-Art for the faithful reproduction. These are recorded source assertions; the historical publication event has not been independently reconstructed. Credit: Gustav Klimt, *Portrait of Adele Bloch-Bauer II*, The Yorck Project / Wikimedia Commons.

The reproduction was retrieved 2026-10-05 (SHA-256 `8c49d204cbb2ed3955be283998cba8c7573a21cdd3a32bbac6890b84bf1d787c`); the full image is not shipped. The matching plain background is `wallpapers/02-default.png`.

The default wallpaper, `wallpapers/01-adele-portrait.jpg`, is a landscape crop of that same file: its top 1575 × 1050 pixels, a 3:2 frame of the hat, face and red wall, made by the repository owner and re-encoded as JPEG. It changes only the framing, so it remains a faithful reproduction of the public-domain painting. SHA-256: `18fce17b4dded783abccd247ab553ce7d60f3011919a6d32e246a823019d21ab`.

## Palette choices

Green from the floral backdrop, coral from the upper wall and flowers, rose and lilac from the side panels and floor, and cream from the dress. These are visual adaptations rather than exact pigment measurements. Surfaces are darkened, text is lifted toward cream, and terminal and status colours are brightened to remain readable. Some subdued cool hues are extended into blue and cyan terminal roles so commands and diagnostics retain distinct colours.

`palette.yaml` is the colour source. `templates/` preserves Vera-dark's current bar layout and application overrides, with a Starship template whose segment colors are picked from the painting. It includes no wallpaper copies. GTK uses the installed name `hyprkarl`; Qt files point to the active theme; Foot supports both colour sections; Neovim retains a dark background.

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
name = "klimt-adele"
generate.generate(name, root / "themes" / name)
PYGEN
```

This reads the preserved palette and overrides directly and leaves the wallpaper directory intact. Regenerate the plain background with ImageMagick using `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png` from this theme directory.

Generation completed successfully, including GTK 3 and GTK 4 CSS. Generated TOML files parse, generated configuration has no unresolved template expressions, and bar layout matches Vera-dark.

Contrast was calculated independently with WCAG relative luminance from linear sRGB. Across all five dark surface layers, minimum text/status contrast is 4.72:1. Selection contrast is 9.15:1. Starship segment text is at least 5.84:1. The prompt opens on the near-black indigo of the sash with near-white text, set through `color_fg_host`. Then come garden green, the ivory dress, the horses' blue-grey and the dusty rose panel with dark text, and the trailing segments are the hat's brown and the pavilion roof's brown. Prompt glyphs are at least 10.44:1 against the background.

Yazi's error-progress text uses the dark background colour on the error fill, giving 8.11:1. Btop explicitly uses the primary foreground. Qt active and inactive placeholders use the opaque secondary foreground, with at least 6.09:1 across the theme surfaces.

All listed pairs meet 4.5:1. The prompt layout reuses `color_yellow` for the directory segment and the Vim visual-mode glyph; both are readable. These checks cover opaque palette colours; wallpaper overlays and application-specific opacity can change effective contrast.

The plain background is 3840 × 2160 pixels, filled with `#17231f`. No active theme was switched.
