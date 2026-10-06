# Van Gogh Wheatfield with Crows

## Artwork and image

Vincent van Gogh, *Wheatfield with Crows*, 1890, oil on canvas, Van Gogh Museum, Amsterdam, s0149V1962 ([museum record](http://www.vangoghmuseum.nl/nl/collectie/s0149V1962)). Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Korenveld_met_kraaien_-_s0149V1962_-_Van_Gogh_Museum.jpg).

Commons tags the file PD-Art with `PD-old-100-expired` (Van Gogh died in 1890): the painting is public domain and the faithful two-dimensional reproduction adds no new copyright. Credit: Vincent van Gogh, *Wheatfield with Crows*, Van Gogh Museum / Wikimedia Commons.

The Commons original is 7762 × 3718 pixels (27,469,225 bytes, SHA-1 `4feead4b36e5c141a6f32acae26d3e653c0b1613`). The shipped full painting, `wallpapers/02-crows.jpg`, is the 3840 × 1839 rendering that Commons serves of that file, retrieved 2026-10-06. SHA-256: `fe423e074e50ced0aca93960ffd799e8330a466190bfb043a7bd90878ca591f3`.

The default wallpaper, `wallpapers/01-crows-crop.jpg`, is a 3:2 crop from the middle of that rendering: 2758 × 1839 pixels starting 541 pixels from the left, re-encoded as JPEG. SHA-256: `dd6a5b18faf289bc477f64dde5ecf41836a651fe5b69db2f56952d71a6448841`.

The matching plain background is `wallpapers/03-default.png`.

## Palette

The deep blue background (`#121a2e`) darkens the stormy sky. The wheat's yellow (`#f0d050`) is the primary accent; the sky blue (`#86a8f4`), the red-brown path (`#ef8e62`), the green verges (`#8fcf6a`) and the pale clouds (`#9fd8e0`) fill the other roles. Cream text (`#f2ede0`) echoes the clouds. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6). `palette.yaml` and `templates/` are the regeneration inputs; see "Regenerate the painting themes" in `docs/themes.md`. The templates are copied from `klimt-hope`, so the bar layout, GTK installation name `hyprkarl`, Foot color sections, Qt paths (`/home/earmand/.config/qt{5,6}ct/`) and other overrides match the Klimt themes. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/03-default.png`.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are sky blue, wheat, path, grass and cloud, with dark text; the trailing segments are deep sky and path shadow.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.81:1**; muted and dim text on the lightest surface are **7.37:1** and **5.55:1**; selection is **11.41:1**. Every terminal color except ANSI black is at least **4.66:1** on every surface. Starship segment text is at least **7.19:1**, every colored segment is at least **7.19:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.19:1**. No desktop theme was activated.
