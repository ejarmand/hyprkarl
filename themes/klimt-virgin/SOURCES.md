# Klimt The Virgin

## Artwork and image

Gustav Klimt, *The Virgin* (*Die Jungfrau*, also *The Maiden*), 1913, oil on canvas, National Gallery Prague, inventory O 4152. Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:KlimtDieJungfrau.jpg), credited to the [National Gallery Prague collection record](http://sbirky.ngprague.cz/dielo/CZE:NG.O_4152).

Commons tags the file PD-Art: the painting is public domain (Klimt died in 1918) and the faithful two-dimensional reproduction adds no new copyright. Credit: Gustav Klimt, *The Virgin*, National Gallery Prague / Wikimedia Commons.

The Commons original is 24943 × 23842 pixels (230,335,418 bytes, SHA-1 `b50bf79a6ce31c9a86623175c93afe046dba1b80`). The shipped full painting, `wallpapers/02-virgin.jpg`, is the 3840 × 3670 rendering that Commons serves of that file, retrieved 2026-10-06. SHA-256: `bbdba5fa1b6bf316c79902891e5bee060c40f6c9e95824a0c9aaec3f6d185b63`.

The default wallpaper, `wallpapers/01-virgin-crop.jpg`, is a 3:2 landscape crop of that rendering: its top 3840 × 2560 pixels (the sleeping faces and the violet swirls), scaled to 2880 × 1920 and re-encoded as JPEG. SHA-256: `9eaadc161e15a01688c018298a2f5372a68b20f281518cdf10555d1d5a6a9c32`.

The matching plain background is `wallpapers/03-default.png`.

## Palette

The warm near-black background (`#1b1714`) comes from the painting's dark field. Violet (`#c78cf4`) and cobalt (`#8a9cfa`) come from the swirling robe, orange (`#f48a5c`) from the flower clusters, emerald (`#6fd0a8`) from the green drapery, and the pale text (`#eee6da`) from the sleeping figures. The violet is the primary accent. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are lightened from the painting where needed for readable text, not pigment measurements.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6). `palette.yaml` and `templates/` are the regeneration inputs; see "Regenerate the Klimt themes" in `docs/themes.md`. The templates are copied from `klimt-hope`, so the bar layout, GTK installation name `hyprkarl`, Foot color sections, Qt paths (`/home/earmand/.config/qt{5,6}ct/`) and other overrides match the other Klimt themes. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/03-default.png`.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are the violet swirl, the orange flowers, the emerald drapery, cobalt and the pink cushion, with dark text; the trailing segments are the deep blue of the swirls and the background's brown.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.39:1**; muted and dim text on the lightest surface are **7.54:1** and **5.85:1**; selection is **7.20:1**. Every terminal color except ANSI black is at least **4.77:1** on every surface. Starship segment text is at least **6.64:1**, every colored segment is at least **6.85:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.20:1**. No desktop theme was activated.
