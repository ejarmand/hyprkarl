# Klimt Lady with a Fan

## Artwork and image

Gustav Klimt, *Lady with a Fan* (*Dame mit Fächer*), 1917–18, oil on canvas, private collection. Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Gustav_Klimt_-_Dame_mit_F%C3%A4cher.jpeg), a reproduction from an art book.

Commons tags the file PD-Art and PD-old-70-expired: Klimt died in 1918, so the painting's copyright has expired, and the faithful two-dimensional reproduction adds no new copyright. These are recorded source statements; the painting's publication history has not been independently reconstructed. Credit: Gustav Klimt, *Lady with a Fan* / Wikimedia Commons.

The crop below was cut from the unchanged Commons JPEG, 2772 × 2760 pixels, 4,722,516 bytes, retrieved 2026-10-06 (SHA-1 `040a8abb2dca3af3558aa886378c278119339f59`, matching Commons). The full image is not shipped.

The default wallpaper, `wallpapers/01-fan-crop.jpg`, is a 3:2 landscape crop of that file: 2772 × 1848 pixels starting 60 pixels from the top (her face, the birds and the top of the fan), re-encoded as JPEG. SHA-256: `ab978a89a47fc7064a676b4865ba1ab38bbaa2be27962069a82b632588883eaf`.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The dark navy background (`#171a24`) comes from the kimono. The saturated yellow field (`#f2cd4a`) is the primary accent; turquoise (`#6ec4c8`) and coral (`#f7926a`) come from the birds, pink (`#eaa0c0`) from the lotus flowers, and green (`#9fd08a`) from the leaves. Cream text (`#f3ead6`) echoes her skin. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on the dark background, not pigment measurements. The painting is light, but the theme is dark like the other Klimt themes.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6). `palette.yaml` and `templates/` are the regeneration inputs; see "Regenerate the painting themes" in `docs/themes.md`. The templates are copied from `klimt-hope`, so the bar layout, GTK installation name `hyprkarl`, Foot color sections, Qt paths (`/home/earmand/.config/qt{5,6}ct/`) and other overrides match the other Klimt themes. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are the turquoise bird, the yellow field, the coral bird, lotus pink and leaf green, with dark text; the trailing segments are the kimono's blue and brown.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.51:1**; muted and dim text on the lightest surface are **6.89:1** and **5.34:1**; selection is **11.25:1**. Every terminal color except ANSI black is at least **4.71:1** on every surface. Starship segment text is at least **7.67:1**, every colored segment is at least **7.67:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.67:1**. No desktop theme was activated.
