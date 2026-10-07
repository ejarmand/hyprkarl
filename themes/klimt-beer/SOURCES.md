# Klimt Friederike Maria Beer

## Artwork and image

Gustav Klimt, *Portrait of Friederike Maria Beer*, 1916, oil on canvas, 168 × 130 cm, Tel Aviv Museum of Art. Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Portrait_of_Friedericke_Maria_Beer.jpg), from Google Arts & Culture.

Commons tags the file `PD-old-70` with a PD-Art reproduction tag: the painting is public domain (Klimt died in 1918) and the faithful two-dimensional reproduction adds no new copyright. These are recorded source assertions; the painting's publication history has not been independently reconstructed. Credit: Gustav Klimt, *Portrait of Friederike Maria Beer*, Tel Aviv Museum of Art / Google Arts & Culture / Wikimedia Commons.

The crop below was cut from the unchanged Commons JPEG, 2868 × 3743 pixels, 2,826,354 bytes, retrieved 2026-10-06 (SHA-1 `e92d00ead39272b077889af2e5bd712dbdfdd243`, matching Commons). The full image is not shipped.

The default wallpaper, `wallpapers/01-beer-crop.jpg`, is a 3:2 crop of that file: 2868 × 1912 pixels starting 40 pixels from the top (her face, the fur-lined coat and the warriors behind her), re-encoded as JPEG. SHA-256: `c02b7fcee21435902e36fa6c02259ae2e86431d4be2d59b94974f5b587e4aa0d`.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The dark blue-green background (`#141b1c`) darkens the painting's outlines and the shadowed jade. The rose-magenta of her coat and the backdrop (`#e19ccb`) is the primary accent, the warriors' jade (`#8ccaa2`) the secondary and the lemon backdrop (`#e4d47a`) the tertiary; the dress blue (`#98aaf2`), orange tassels (`#f0976e`) and turquoise rug (`#86ccc4`) fill the other terminal roles. Pale text (`#eeebe3`) echoes the grey fur. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

`theme.yaml` is the source. Besides `mode: dark` and the palette, it sets the same consumer color roles as the other Klimt themes: selection colors in the terminals, Qt and Neovim, btop's main text and highlight, opaque Qt placeholder and disabled text, dark text on Yazi's error progress, Neovim's terminal color 8, and primary-accent GTK links. Surface layers mix 3, 6, 9.5 and 13.5% of the text color into the background; muted and dim text mix 12% and 25% of the background into the text. `overrides/starship.toml` is the Starship palette template. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Hyprkarl's theme compiler builds the theme from `theme.yaml` (`hk-theme set klimt-beer`).

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are the rose coat, the dress blue, the lemon backdrop, jade and grey fur, with dark text; the trailing segments are a deep magenta and a dark jade.

## Validation

`python -m theme_generator build klimt-beer`, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.65:1**; muted and dim text on the lightest surface are **8.01:1** and **6.03:1**; selection is **8.16:1**. Every terminal color except ANSI black is at least **5.40:1** on every surface. Starship segment text is at least **7.78:1** and every colored segment is at least **7.78:1** against the background; on the trailing segments, main text is at least **8.96:1** and the accent text **6.38:1**. Prompt glyphs, including the Vim visual-mode glyph, are at least **7.78:1**. No desktop theme was activated.
