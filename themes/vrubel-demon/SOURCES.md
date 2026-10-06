# Vrubel Demon Seated

## Artwork and image

Mikhail Vrubel, *Demon Seated*, 1890, oil on canvas, State Tretyakov Gallery, Moscow. Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:%D0%94%D0%B5%D0%BC%D0%BE%D0%BD_%D1%81%D0%B8%D0%B4%D1%8F%D1%89%D0%B8%D0%B9.jpg).

The painting is public domain: Vrubel died in 1910. The photograph is a separate work by Wikimedia Commons user [Mikhisor](https://commons.wikimedia.org/wiki/User:Mikhisor), dated 2020-10-21 and licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Credit: Mikhail Vrubel, *Demon Seated* (1890); photograph by Mikhisor, CC BY-SA 4.0, via Wikimedia Commons. The full license text is in `ARTWORK-LICENSE.txt`. The crop below is an adaptation of the photograph and is shared under the same license.

The Commons original is 6144 × 3261 pixels (18,909,483 bytes, SHA-1 `43b22bb32293a83b84c9335f779777e60ea6dc5a`). The crop below was cut from the 3840 × 2038 rendering that Commons serves of that file, retrieved 2026-10-06. The full image is not shipped.

The default wallpaper, `wallpapers/01-demon-crop.jpg`, is a 3:2 crop of that rendering: 3057 × 2038 pixels starting 200 pixels from the left, scaled to 2880 × 1920 and re-encoded as JPEG. Changes from the original: cropped, scaled and re-encoded. SHA-256: `678e4be9ba43d4bfbd7cb9b3ec1b5e71651315b10ed496835b30b358ff3bb456`.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The blue-black background (`#18171f`) comes from the darkest shadows. The coral of the sunset sky (`#f28a72`) is the primary accent; the robe's blue (`#86a4ee`), the lilac of the crystal flowers (`#c4b2e0`), the sunset gold (`#f2b866`) and a muted leaf green (`#8cc0a0`) fill the other roles. Cream text (`#f1e8e2`) echoes the lit stone. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6). `palette.yaml` and `templates/` are the regeneration inputs; see "Regenerate the painting themes" in `docs/themes.md`. The templates are copied from `klimt-hope`, so the bar layout, GTK installation name `hyprkarl`, Foot color sections, Qt paths (`/home/earmand/.config/qt{5,6}ct/`) and other overrides match the Klimt themes. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are coral sky, robe blue, sunset gold, crystal lilac and leaf green, with dark text; the trailing segments are deep robe blue and umber.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.71:1**; muted and dim text on the lightest surface are **7.39:1** and **5.60:1**; selection is **7.33:1**. Every terminal color except ANSI black is at least **4.75:1** on every surface. Starship segment text is at least **5.87:1**, every colored segment is at least **7.25:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.33:1**. No desktop theme was activated.
