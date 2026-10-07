# Klimt Adele Bloch-Bauer I

## Artwork and image

Gustav Klimt, *Portrait of Adele Bloch-Bauer I* (the "Golden Adele"), 1907, oil, silver and gold on canvas, 140 × 140 cm, Neue Galerie, New York. Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Gustav_Klimt_-_Portr%C3%A4t_der_Adele_Bloch-Bauer_I_(1907).jpg), from GalleriX. `klimt-adele` is the later *Adele Bloch-Bauer II*.

Commons tags the file PD-Art with `PD-old-auto-1923`: the painting is public domain (Klimt died in 1918) and the faithful two-dimensional reproduction adds no new copyright. These are recorded source assertions; the painting's publication history has not been independently reconstructed. Credit: Gustav Klimt, *Portrait of Adele Bloch-Bauer I*, Neue Galerie New York / Wikimedia Commons.

The crop below was cut from the unchanged Commons JPEG, 2801 × 2801 pixels, 3,368,013 bytes, retrieved 2026-10-06 (SHA-1 `de0bdf8b2bf00a3334b2aaa378923918b2119140`, matching Commons). The full image is not shipped.

The default wallpaper, `wallpapers/01-adele-gold-crop.jpg`, is a 3:2 crop of that file: its top 2801 × 1867 pixels (her face, hands and the upper dress against the gold ground), re-encoded as JPEG. SHA-256: `8d4237f821a258524e96df42af329396bed3adbb11eca8a7042fa52a68cb0e3f`.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The dark brown background (`#19130c`) comes from her hair. Gold leaf (`#e8bc4c`) is the primary accent, the lapis inlays of the dress (`#93a8ec`) the secondary and the green floor at the lower left (`#a6c47a`) the tertiary; the red squares (`#ec8a62`), the rose of the collar (`#d8a0c4`) and a silver-green (`#9cc8b8`) fill the other terminal roles. Cream text (`#f2e7cf`) echoes her skin. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

`theme.yaml` is the source. Besides `mode: dark` and the palette, it sets the same consumer color roles as the other Klimt themes: selection colors in the terminals, Qt and Neovim, btop's main text and highlight, opaque Qt placeholder and disabled text, dark text on Yazi's error progress, Neovim's terminal color 8, and primary-accent GTK links. Surface layers mix 3, 6, 9.5 and 13.5% of the text color into the background; muted and dim text mix 12% and 25% of the background into the text. `overrides/starship.toml` is the Starship palette template. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Hyprkarl's theme compiler builds the theme from `theme.yaml` (`hk-theme set klimt-adele-gold`).

Starship includes only the palette and leaves the user's prompt layout intact. The prompt opens on deep lapis (`#263a8a`) with cream text, set through `color_fg_host`. The colored segments that follow use dark text on gold leaf, the lapis inlays, silver and pale skin; green, coral and brown were left out because they looked foreign beside the painting. The trailing segments are deep lapis and, under the time, the dark crimson of the squares beside her, which stays crimson only at a depth that needs light text.

## Validation

`python -m theme_generator build klimt-adele-gold`, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **15.01:1**; muted and dim text on the lightest surface are **8.36:1** and **6.22:1**; selection is **10.29:1**. Every terminal color except ANSI black is at least **5.21:1** on every surface. The opening segment's cream text is **8.33:1**. Dark text on the other colored segments is at least **7.94:1**, and those segments are at least **7.94:1** against the background; on the trailing segments, main text is at least **8.33:1** and the accent text **6.82:1**. Prompt glyphs, including the Vim visual-mode glyph, are at least **7.35:1**. No desktop theme was activated.
