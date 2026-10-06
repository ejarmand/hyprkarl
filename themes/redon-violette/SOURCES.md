# Redon Violette Heymann

## Artwork and image

Odilon Redon, *Portrait of Violette Heymann*, pastel, Cleveland Museum of Art, 1976.1926 ([museum record](http://www.clevelandart.org/art/1976.1926)). Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Portrait_of_Violette_Heyman_-_Odilon_Redon_(Cleveland_Art_Museum).jpg).

Commons tags the file PD-Art with `PD-old-auto-expired` (Redon died in 1916): the work is public domain and the faithful two-dimensional reproduction adds no new copyright. Credit: Odilon Redon, *Portrait of Violette Heymann*, Cleveland Museum of Art / Wikimedia Commons.

The Commons original is 9989 × 7831 pixels (40,226,450 bytes, SHA-1 `9900dae5d5325ada980980e779416b879521c90c`). The crop below was cut from the 3840 × 3010 rendering that Commons serves of that file, retrieved 2026-10-06. The full image is not shipped.

The default wallpaper, `wallpapers/01-violette-crop.jpg`, is a 3:2 crop of that rendering: 3840 × 2560 pixels starting 225 pixels from the top, scaled to 2880 × 1920 and re-encoded as JPEG. SHA-256: `30ec063b1559d4508bfd9d23d5e3101b84ea38f3f2d5b0d016be15ed3f359a85`.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The warm dark background (`#1d1a17`) deepens the taupe ground. The violet flowers (`#c194f2`) are the primary accent; the mint of her dress (`#96dcc4`), the cobalt flowers (`#8ea4f4`), the leaf green (`#86d686`), the peach flower (`#f2a084`) and the ochre ribbon (`#e4c56a`) fill the other roles. Cream text (`#efe7da`) echoes the white blossoms. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6). `palette.yaml` and `templates/` are the regeneration inputs; see "Regenerate the painting themes" in `docs/themes.md`. The templates are copied from `klimt-hope`, so the bar layout, GTK installation name `hyprkarl`, Foot color sections, Qt paths (`/home/earmand/.config/qt{5,6}ct/`) and other overrides match the Klimt themes. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are mint dress, violet flowers, peach flower, cobalt flowers and leaf green, with dark text; the trailing segments are taupe ground and auburn hair.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.12:1**; muted and dim text on the lightest surface are **7.29:1** and **5.46:1**; selection is **7.25:1**. Every terminal color except ANSI black is at least **4.89:1** on every surface. Starship segment text is at least **5.60:1**, every colored segment is at least **7.23:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.25:1**. No desktop theme was activated.
