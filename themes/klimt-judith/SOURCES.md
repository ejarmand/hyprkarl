# Klimt Judith II

## Artwork and image

Gustav Klimt, *Judith II (Salome)*, 1909, oil on canvas, 178 × 46 cm, Ca' Pesaro – Galleria Internazionale d'Arte Moderna, Venice, bought at the 1910 Venice Biennale. Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:(Venice)_Gustav_Klimt_-_Giuditta_II_(Judith_II)_with_original_frame_-_Museo_d%27arte_moderna.jpg), a photograph of the painting in its original gilded frame, taken 2024-05-07.

The painting is public domain: Klimt died in 1918. The photograph is a separate work by [Didier Descouens](https://commons.wikimedia.org/wiki/User:Archaeodontosaurus), licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Credit: Gustav Klimt, *Judith II* (1909), Ca' Pesaro, Venice; photograph by Didier Descouens, CC BY-SA 4.0, via Wikimedia Commons. The full license text is in `ARTWORK-LICENSE.txt`. The crop below is an adaptation of the photograph and is shared under the same license.

The theme was requested from [`File:Gustav_Klimt,_Judith_II.jpg`](https://commons.wikimedia.org/wiki/File:Gustav_Klimt,_Judith_II.jpg) (1629 × 3508 pixels, SHA-1 `1220ff087917473a4f91d5e7a075902c343c8a8b`, tagged `PD-old`, from Flickr). That file is too small for a wallpaper that reaches her shoulders, so the crop comes from the larger Descouens photograph, whose frame supplies the width a 3:2 landscape crop needs. The palette was picked from his [unframed photograph](https://commons.wikimedia.org/wiki/File:(Venice)_Gustav_Klimt_-_Giuditta_II_(Judith_II)_-_Museo_d%27arte_moderna.jpg) of the same painting, also CC BY-SA 4.0, which is not shipped.

The Commons original is 3034 × 6238 pixels (17,128,095 bytes, SHA-1 `914e205e484685fcc234b8071fdcd609feb6290f`), retrieved 2026-10-07. The full image is not shipped.

The default wallpaper, `wallpapers/01-judith-crop.jpg`, is a 3:2 crop of that file: 2826 × 1884 pixels starting 102 pixels from the left and 360 from the top, between the outer edges of the frame's gilded pillars and below the frame's top bar and the shadow it casts on the canvas. It shows her face, neck and shoulders, the poppies, the chequered shawl and her bare chest. Re-encoded as JPEG. Changes from the original: cropped and re-encoded. SHA-256: `73d10ff71994293fc216cdb00ce5d958e6180fa42f03045b0ce68feb18574abd`.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The warm black background (`#14100f`) comes from her hair. The vermilion ground behind her (`#ec8c62`) is the primary accent, the gold leaf (`#e3be52`) the secondary and the poppies' pink (`#e59cba`) the tertiary; the shawl's cobalt (`#92a6ec`), green (`#9cc49a`) and teal (`#88c4c0`) fill the other terminal roles. Ivory text (`#f0e6d8`) echoes her skin. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are lightened from the painting where needed for readable text, not pigment measurements.

## Generation and compatibility

`theme.yaml` is the source. Besides `mode: dark` and the palette, it sets the same consumer color roles as the other Klimt themes: selection colors in the terminals, Qt and Neovim, btop's main text and highlight, opaque Qt placeholder and disabled text, dark text on Yazi's error progress, Neovim's terminal color 8, and primary-accent GTK links. Surface layers mix 3, 6, 9.5 and 13.5% of the text color into the background; muted and dim text mix 12% and 25% of the background into the text. `overrides/starship.toml` is the Starship palette template. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Hyprkarl's theme compiler builds the theme from `theme.yaml` (`hk-theme set klimt-judith`).

Starship includes only the palette and leaves the user's prompt layout intact. The prompt opens on the painting's deep vermilion (`#a8381a`) with cream text, set through `color_fg_host`, because the red stays red only when it is too dark for dark text. The colored segments that follow alternate cool and warm, with dark text: the shawl's cobalt, gold leaf, the silver-grey robe and ivory skin. Coral, pink and gold side by side blurred together, so no two warm segments touch, and pastel teal and pink were dropped as foreign to the painting. The trailing segments are the poppies' crimson and, under the time, the shawl's deep blue.

## Validation

`python -m theme_generator build klimt-judith`, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **15.32:1**; muted and dim text on the lightest surface are **8.58:1** and **6.36:1**; selection is **7.65:1**. Every terminal color except ANSI black is at least **5.50:1** on every surface. The opening segment's cream text is **5.24:1**. Dark text on the other colored segments is at least **8.00:1**, and those segments are at least **8.00:1** against the background; on the trailing segments, main text is at least **8.29:1** and the accent text **5.48:1**. Prompt glyphs, including the Vim visual-mode glyph, are at least **7.65:1**. No desktop theme was activated.
