# Bonnard Le Cannet

## Artwork and image

Pierre Bonnard, *Le Cannet*, 1930, oil on canvas, Fondation Bemberg, Toulouse, inventory 2109. Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Bemberg_Fondation_Toulouse_-_Le_Cannet_1930_-_Pierre_Bonnard_Inv.2109.jpg).

The painting is public domain: Bonnard died in 1947, and Commons tags the artwork `PD-old-auto-expired`. The photograph is a separate work by [Didier Descouens](https://commons.wikimedia.org/wiki/User:Archaeodontosaurus), licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Credit: Pierre Bonnard, *Le Cannet* (1930), Fondation Bemberg; photograph by Didier Descouens, CC BY-SA 4.0, via Wikimedia Commons. The full license text is in `ARTWORK-LICENSE.txt`. The crop below is an adaptation of the photograph and is shared under the same license.

The Commons original is 4134 × 3382 pixels (18,867,210 bytes, SHA-1 `50e3cc57eb88bc8d9a3d260a4c91d97548aa0bb8`). The shipped full painting, `wallpapers/02-cannet.jpg`, is the 3840 × 3141 rendering that Commons serves of that file, retrieved 2026-10-06. SHA-256: `cfbc4057398a6c4c7d642ca802c149ccedb2b85cc5b50c6dc260de83ef8cd405`.

The default wallpaper, `wallpapers/01-cannet-crop.jpg`, is a 3:2 crop of that rendering: 3840 × 2560 pixels starting 290 pixels from the top, scaled to 2880 × 1920 and re-encoded as JPEG. Changes from the original: cropped, scaled and re-encoded. SHA-256: `d943c8495c9f5f33412529da865f6c9ef4fa388774be12427ca90d527be5f36f`.

The matching plain background is `wallpapers/03-default.png`.

## Palette

The deep blue background (`#1a1c26`) comes from the shadowed foliage. The orange of the sunlit ground (`#f4a83c`) is the primary accent; the agave's blue (`#8ab4f0`), the leaf green (`#a6d06a`), the oleander pink (`#ef9ac4`) and the violet hills (`#b7a2e6`) fill the other roles. Cream text (`#f4ecdc`) echoes the pale sky. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6). `palette.yaml` and `templates/` are the regeneration inputs; see "Regenerate the painting themes" in `docs/themes.md`. The templates are copied from `klimt-hope`, so the bar layout, GTK installation name `hyprkarl`, Foot color sections, Qt paths (`/home/earmand/.config/qt{5,6}ct/`) and other overrides match the Klimt themes. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/03-default.png`.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are agave blue, orange ground, leaf green, oleander pink and violet hills, with dark text; the trailing segments are shadowed foliage blue and trunk brown.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.44:1**; muted and dim text on the lightest surface are **6.64:1** and **5.04:1**; selection is **8.49:1**. Every terminal color except ANSI black is at least **4.58:1** on every surface. Starship segment text is at least **6.92:1**, every colored segment is at least **7.53:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.64:1**. No desktop theme was activated.
