# Klee Wald Bau

## Artwork and image

Paul Klee, *Wald Bau* (*Forest Construction*), 1919, Museo del Novecento, Milan. Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Wald_Bau,_1919_-_Paul_Klee.jpg), from Google Arts & Culture.

Commons tags the file PD-Art with `PD-old-auto-expired` (Klee died in 1940): the work is public domain and the faithful two-dimensional reproduction adds no new copyright. Credit: Paul Klee, *Wald Bau*, Museo del Novecento / Google Arts & Culture / Wikimedia Commons.

The Commons original is 19931 × 21142 pixels (175,937,375 bytes, SHA-1 `d4be84ed7f67a48e5153c5da3cfcdbce1ab5adfc`). The crop below was cut from the 3840 × 4073 rendering that Commons serves of that file, retrieved 2026-10-06. The full image is not shipped.

The default wallpaper, `wallpapers/01-wald-bau-crop.jpg`, is a 3:2 crop from the middle of that rendering: 3840 × 2560 pixels starting 756 pixels from the top, scaled to 2880 × 1920 and re-encoded as JPEG. SHA-256: `ed46c4b2e63adf5f46a12f6ba35e6f2ddfd6466f8bd7ad50d565a6e94992bf8f`.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The near-black background (`#1c1716`) comes from the dark corners. Jade green (`#6fd39a`) is the primary accent; brick (`#ec8a6c`), violet-grey (`#a2a6e4`), ochre (`#e2b86a`), rose (`#e59ab2`) and teal (`#7fcfc0`) come from the faceted planes. Cream text (`#efe6dc`) echoes the pale patches. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

`theme.yaml` is the source. Besides `mode: dark` and the palette, it sets the same consumer color roles as the other Klimt themes: selection colors in the terminals, Qt and Neovim, btop's main text and highlight, opaque Qt placeholder and disabled text, dark text on Yazi's error progress, Neovim's terminal color 8, and primary-accent GTK links. `overrides/starship.toml` is the Starship palette template. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Hyprkarl's theme compiler builds the theme from `theme.yaml` (`hk-theme set klee-wald-bau`). It was first generated for the AGS-era layout with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6), using the Klimt templates. The 1.x port renders the same terminal, btop, wifitui, Yazi, Qt, GTK and Starship colors as that build, so the checks below, made on that build, still describe it.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are jade green, brick, violet-grey, ochre and rose, with dark text; the trailing segments are dark forest green and maroon.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.38:1**; muted and dim text on the lightest surface are **7.49:1** and **5.61:1**; selection is **9.68:1**. Every terminal color except ANSI black is at least **4.85:1** on every surface. Starship segment text is at least **5.49:1**, every colored segment is at least **7.11:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.11:1**. No desktop theme was activated.
