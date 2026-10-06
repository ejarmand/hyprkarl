# Munch Young People on the Beach

## Artwork and image

Edvard Munch, *Young People on the Beach*, from the Linde Frieze, 1904, Munch Museum, Oslo. Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Edvard_Munch,_giovani_sulla_spiaggia_(fregio_linde),_1904.jpg).

Munch died in 1944, so the work is out of copyright in countries with a life-plus-70 term. In the US, a work first published before 1931 is public domain, and an unpublished work's term (life plus 70 years) ended in 2014; only a first publication in 1931 or later could keep it protected. Commons records it as public domain; its publication history has not been independently reconstructed. The photograph is a separate work by Francesco Bini (Wikimedia Commons user [Sailko](https://commons.wikimedia.org/wiki/User:Sailko)), dated 2024-06-15 and licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Credit: Edvard Munch, *Young People on the Beach* (1904), Munch Museum; photograph by Francesco Bini, CC BY-SA 4.0, via Wikimedia Commons. The full license text is in `ARTWORK-LICENSE.txt`. The crop below is an adaptation of the photograph and is shared under the same license.

The Commons original is 5544 × 3018 pixels (8,623,250 bytes, SHA-1 `b55b4f51b1c98ae6efd0fd93e6fc9f73e5cbb576`) and shows the painting in its frame, so no full image is shipped. The default wallpaper, `wallpapers/01-linde-beach-crop.jpg`, is a 3:2 crop of the 3840 × 2090 rendering that Commons serves, retrieved 2026-10-06: 2820 × 1880 pixels starting at x = 850, y = 95, inside the frame, re-encoded as JPEG. Changes from the original: cropped to remove the frame and re-encoded. SHA-256: `2c00e62111961fb8bfc097b7bf2e74d5842ccbea711449972c1435c90473ab95`.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The dark green background (`#141b17`) deepens the grass. The red hat (`#fa866e`) is the primary accent; the grass (`#74c97e`), the sand (`#e8c27a`), the pale sea (`#9ab4e0`) and the pink rocks (`#e6a0b0`) fill the other roles. Cream text (`#f1ebdd`) echoes the white dress. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6). `palette.yaml` and `templates/` are the regeneration inputs; see "Regenerate the painting themes" in `docs/themes.md`. The templates are copied from `klimt-hope`, so the bar layout, GTK installation name `hyprkarl`, Foot color sections, Qt paths (`/home/earmand/.config/qt{5,6}ct/`) and other overrides match the Klimt themes. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are sea, red hat, sand, grass and pink rock, with dark text; the trailing segments are dark grass and dark coats.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.74:1**; muted and dim text on the lightest surface are **7.32:1** and **5.49:1**; selection is **7.26:1**. Every terminal color except ANSI black is at least **4.70:1** on every surface. Starship segment text is at least **5.42:1**, every colored segment is at least **7.26:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.26:1**. No desktop theme was activated.
