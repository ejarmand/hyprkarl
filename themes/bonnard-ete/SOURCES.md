# Bonnard L'Été

## Artwork and image

Pierre Bonnard, *L'Été* (*Summer*), 1917, oil on canvas, 260 × 340 cm, Fondation Marguerite et Aimé Maeght, Saint-Paul-de-Vence. Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Pierre_Bonnard_-_L%27%C3%89t%C3%A9,_1917.jpg), taken from a [Sotheby's article](https://www.sothebys.com/en/articles/pierre-bonnard-painting-paradise).

Commons tags the file PD-Art with `PD-old-auto-expired` (Bonnard died in 1947): the painting is public domain and the faithful two-dimensional reproduction adds no new copyright. In the US, a work first published before 1931 is public domain, and an unpublished work's term (life plus 70 years) ended in 2017; the painting's publication history has not been independently reconstructed. Credit: Pierre Bonnard, *L'Été*, Fondation Maeght / Wikimedia Commons.

The crop below was cut from the Commons original, 4465 × 3406 pixels, 3,081,107 bytes, retrieved 2026-10-06 (SHA-1 `f52bea3291cd523a0bc3f0f9b217b00d6509f1fd`, matching Commons). The full image is not shipped.

The default wallpaper, `wallpapers/01-ete-crop.jpg`, is a 3:2 crop of that file: 4465 × 2977 pixels starting 300 pixels from the top (the meadow and the figures on the grass), scaled to 2880 × 1920 and re-encoded as JPEG. SHA-256: `659fcab435ab7bd0874abe3ac8e8b751d4675fd06e083431550150acfee59933`. It includes small nude bathers in the middle distance.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The deep blue-green background (`#121c1e`) comes from the shaded foliage. The lime green of the sunlit grass (`#88d84e`) is the primary accent and the flame orange of the meadow's edge (`#f4983c`) the secondary; the blue of the dresses (`#8aa6f2`), the foliage teal (`#6cc4b0`), the pale meadow (`#e8d88a`) and the lilac sky (`#bcaaf0`) fill the other roles. Cream text (`#f0ecdf`) echoes the pale figures. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements. Leading with green keeps it distinct from `bonnard-cannet`, which leads with orange.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6). `palette.yaml` and `templates/` are the regeneration inputs; see "Regenerate the painting themes" in `docs/themes.md`. The templates are copied from `klimt-hope`, so the bar layout, GTK installation name `hyprkarl`, Foot color sections, Qt paths (`/home/earmand/.config/qt{5,6}ct/`) and other overrides match the Klimt themes. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are lime grass, blue dress, flame orange, foliage teal and pale meadow, with dark text; the trailing segments are deep shade blue and olive tree.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.68:1**; muted and dim text on the lightest surface are **7.30:1** and **5.49:1**; selection is **9.90:1**. Every terminal color except ANSI black is at least **4.73:1** on every surface. Starship segment text is at least **7.09:1**, every colored segment is at least **7.28:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.77:1**. No desktop theme was activated.
