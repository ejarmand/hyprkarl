# Van Gogh Irises

## Artwork and image

Vincent van Gogh, *Irises*, 1889, oil on canvas, 74.3 × 94.3 cm, J. Paul Getty Museum, 90.PA.20. Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Vincent_van_Gogh_-_Irises_(1889).jpg), from the Getty's open-content images.

Commons tags the file PD-Art with `PD-old-auto-expired` (Van Gogh died in 1890): the painting is public domain and the faithful two-dimensional reproduction adds no new copyright. Credit: Vincent van Gogh, *Irises*, J. Paul Getty Museum / Wikimedia Commons.

The Commons original is 9600 × 7413 pixels (29,674,196 bytes, SHA-1 `a9a4abf694de994b39d8e4a441c89b027582adf2`). The shipped full painting, `wallpapers/02-irises.jpg`, is the 3840 × 2965 rendering that Commons serves of that file, retrieved 2026-10-06. SHA-256: `97d421fbfc16f70fe39263c63f2d716e4ae03cf49c8e05506fd989222fd9898c`.

The default wallpaper, `wallpapers/01-irises-crop.jpg`, is a 3:2 crop of that rendering: 3840 × 2560 pixels starting 200 pixels from the top, scaled to 2880 × 1920 and re-encoded as JPEG. SHA-256: `aa222c47e72a1c5730fa80a8324510a1099424619ec2e3cd3e1355813d2360c8`.

The matching plain background is `wallpapers/03-default.png`.

## Palette

The deep green background (`#141c1b`) darkens the leaves. The irises' violet-blue (`#98a6f6`) is the primary accent; the teal-green leaves (`#88c4aa`), the orange marigolds (`#f2a65a`), the earth (`#ee9670`) and violet (`#b89af0`) fill the other roles. Cream text (`#efeadc`) echoes the white iris. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6). `palette.yaml` and `templates/` are the regeneration inputs; see "Regenerate the painting themes" in `docs/themes.md`. The templates are copied from `klimt-hope`, so the bar layout, GTK installation name `hyprkarl`, Foot color sections, Qt paths (`/home/earmand/.config/qt{5,6}ct/`) and other overrides match the Klimt themes. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/03-default.png`.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are iris blue, marigold, leaf green, earth and white iris, with dark text; the trailing segments are deep iris and earth brown.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.42:1**; muted and dim text on the lightest surface are **7.14:1** and **5.42:1**; selection is **7.53:1**. Every terminal color except ANSI black is at least **4.73:1** on every surface. Starship segment text is at least **5.24:1**, every colored segment is at least **7.53:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.36:1**. No desktop theme was activated.
