# Klimt Danaë

## Artwork and image

Gustav Klimt, *Danaë*, 1907–08, oil on canvas, private collection. Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Klimt_-_Danae_-_1907-08.jpeg), a reproduction from an art book.

Commons tags the file PD-Art: the painting is public domain (Klimt died in 1918) and the faithful two-dimensional reproduction adds no new copyright. Credit: Gustav Klimt, *Danaë* / Wikimedia Commons.

The crop below was cut from the unchanged Commons JPEG, 2694 × 2502 pixels, 4,634,008 bytes, retrieved 2026-10-06 (SHA-1 `91c35726311237c9ce1623f45c4a48dacdfe87b3`, matching Commons). The full image is not shipped.

The default wallpaper, `wallpapers/01-danae-crop.jpg`, is a 3:2 landscape crop of that file: its top 2694 × 1796 pixels (her face, hair and the gold rain), re-encoded as JPEG. SHA-256: `c80733f2bc510a3220feb73b88d23b055e46b9805cdbfecdae033a53e39b9ed2`. The painting is a nude, and every landscape crop of it includes nudity.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The violet-black background (`#19151f`) comes from the dark corner and the veil. Gold (`#ecc04a`) from the falling coins is the primary accent, copper (`#eb9a5c`) from her hair the secondary, and violet (`#bd96ee`) from the veil the tertiary. Cream text (`#f1e8dc`) echoes her skin. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are lightened from the painting where needed for readable text, not pigment measurements.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6). `palette.yaml` and `templates/` are the regeneration inputs; see "Regenerate the painting themes" in `docs/themes.md`. The templates are copied from `klimt-hope`, so the bar layout, GTK installation name `hyprkarl`, Foot color sections, Qt paths (`/home/earmand/.config/qt{5,6}ct/`) and other overrides match the other Klimt themes. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are copper hair, the violet veil, the gold coins, the sage at the top edge and pale skin, with dark text; the trailing segments are the veil's deep violet and a dark bronze.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.82:1**; muted and dim text on the lightest surface are **7.94:1** and **5.98:1**; selection is **10.45:1**. Every terminal color except ANSI black is at least **5.25:1** on every surface. Starship segment text is at least **7.50:1**, every colored segment is at least **7.50:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.50:1**. No desktop theme was activated.
