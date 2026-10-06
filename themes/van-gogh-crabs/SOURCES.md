# Van Gogh Two Crabs

## Artwork and image

Vincent van Gogh, *Two Crabs*, January 1889, oil on canvas, 47 × 61 cm, private collection, on loan to the National Gallery, London, L995 ([gallery record](https://www.nationalgallery.org.uk/paintings/vincent-van-gogh-two-crabs)). Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Vincent_van_Gogh_-_Two_Crabs_(1889).jpg).

Commons tags the file PD-Art (Van Gogh died in 1890; tagged `PD-old-auto-1923`): the painting is public domain and the faithful two-dimensional reproduction adds no new copyright. Credit: Vincent van Gogh, *Two Crabs*, National Gallery, London / Wikimedia Commons.

The Commons original is 6000 × 4226 pixels (8,959,921 bytes, SHA-1 `6b8a9b25d2cbf71f709ff20c7303c931e8104daa`). The crop below was cut from the 3840 × 2705 rendering that Commons serves of that file, retrieved 2026-10-06. The full image is not shipped.

The default wallpaper, `wallpapers/01-crabs-crop.jpg`, is a 3:2 crop of that rendering: 3840 × 2560 pixels starting 72 pixels from the top, scaled to 2880 × 1920 and re-encoded as JPEG. SHA-256: `44ee865b03967e94d87b17b36ee63f9ff8b0a89e09681155264a5cabf4124398`.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The dark green background (`#10201c`) deepens the ground. The crabs' orange (`#f2a85a`) is the primary accent; the sea-green ground (`#66c6b0`), the red shells (`#fa9478`), green (`#9ad488`) and the blue shadows (`#92aef2`) fill the other roles. Cream text (`#f1ebdf`) echoes the pale claws. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6). `palette.yaml` and `templates/` are the regeneration inputs; see "Regenerate the painting themes" in `docs/themes.md`. The templates are copied from `klimt-hope`, so the bar layout, GTK installation name `hyprkarl`, Foot color sections, Qt paths (`/home/earmand/.config/qt{5,6}ct/`) and other overrides match the Klimt themes. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are crab orange, sea-green ground, red shell, pale claw and blue shadow, with dark text; the trailing segments are deep green and dark shell red.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.20:1**; muted and dim text on the lightest surface are **6.77:1** and **5.08:1**; selection is **8.45:1**. Every terminal color except ANSI black is at least **4.78:1** on every surface. Starship segment text is at least **5.17:1**, every colored segment is at least **7.18:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.18:1**. No desktop theme was activated.
