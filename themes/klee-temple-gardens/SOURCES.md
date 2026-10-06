# Klee Temple Gardens

## Artwork and image

Paul Klee, *Temple Gardens*, 1920, gouache and ink on paper, 18.4 × 26.7 cm, The Metropolitan Museum of Art, 1987.455.2, The Berggruen Klee Collection, 1987. Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Temple_Gardens,_1920_-_Paul_Klee,_MET_ma1987.455.2.R.jpg).

Commons tags the file PD-Art (Klee died in 1940; tagged `PD-old-auto-1923`): the work is public domain and the faithful two-dimensional reproduction adds no new copyright. Credit: Paul Klee, *Temple Gardens*, The Metropolitan Museum of Art / Wikimedia Commons.

The crop below was cut from the unchanged Commons JPEG, 1519 × 1233 pixels, 636,084 bytes, retrieved 2026-10-06 (SHA-1 `ad64bb856b91cd368cfee7bc2267e6dfab254993`, matching Commons). The full image is not shipped.

The default wallpaper, `wallpapers/01-temple-gardens-crop.jpg`, is a 3:2 crop of that file inside the paper border: 1440 × 960 pixels starting 40 pixels from the left and top, re-encoded as JPEG. SHA-256: `963c2cfefb871f97c621872e4c110294f4075b53b36a097092bb343652d96688`. The source is small, so this wallpaper is upscaled on most screens.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The dark red-brown background (`#1f1714`) deepens the painting's shadows. Temple orange (`#f3a64a`) is the primary accent; the teal arches (`#6fc8b8`), red (`#f28462`), slate blue (`#93a8d4`) and green (`#a6cf7a`) fill the other roles. Cream text (`#f3e8d8`) echoes the paper. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

`theme.yaml` is the source. Besides `mode: dark` and the palette, it sets the same consumer color roles as the other Klimt themes: selection colors in the terminals, Qt and Neovim, btop's main text and highlight, opaque Qt placeholder and disabled text, dark text on Yazi's error progress, Neovim's terminal color 8, and primary-accent GTK links. `overrides/starship.toml` is the Starship palette template. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Hyprkarl's theme compiler builds the theme from `theme.yaml` (`hk-theme set klee-temple-gardens`). It was first generated for the AGS-era layout with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6), using the Klimt templates. The 1.x port renders the same terminal, btop, wifitui, Yazi, Qt, GTK and Starship colors as that build, so the checks below, made on that build, still describe it.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are temple orange, slate blue, red, teal arches and ochre, with dark text; the trailing segments are deep slate and burnt red-brown.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.56:1**; muted and dim text on the lightest surface are **7.69:1** and **5.71:1**; selection is **8.70:1**. Every terminal color except ANSI black is at least **4.78:1** on every surface. Starship segment text is at least **5.80:1**, every colored segment is at least **6.93:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **6.93:1**. No desktop theme was activated.
