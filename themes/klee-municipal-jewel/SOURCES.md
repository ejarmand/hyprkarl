# Klee Municipal Jewel

## Artwork and image

Paul Klee, *Municipal Jewel*, 1917, The Metropolitan Museum of Art, The Berggruen Klee Collection, 1984 ([museum record](https://www.metmuseum.org/art/collection/search/483128)). Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Municipal_Jewel,_1917_-_Paul_Klee,_MET_DT7782.jpg), donated by the museum.

Commons tags the file PD-Art with `PD-old-auto-expired` (Klee died in 1940): the work is public domain and the faithful two-dimensional reproduction adds no new copyright. Credit: Paul Klee, *Municipal Jewel*, The Metropolitan Museum of Art / Wikimedia Commons.

The crop below was cut from the unchanged Commons JPEG, 4000 × 2109 pixels, 2,458,877 bytes, retrieved 2026-10-06 (SHA-1 `caffc6ea1ba1becdd214ff4d7c0358c2d68fbfd5`, matching Commons). The full image is not shipped.

The default wallpaper, `wallpapers/01-municipal-jewel-crop.jpg`, is a 3:2 crop of the painted area: 2850 × 1900 pixels starting 575 pixels from the left and 20 from the top, re-encoded as JPEG. SHA-256: `cd06f27ac7d01702d2f651dfadd1673692f0b665b79725becf25b99580f3a943`.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The blue-black background (`#15161d`) comes from the dark planes. Magenta pink (`#f286c6`) is the primary accent; sapphire (`#8a9df4`), emerald (`#6fd2a2`), ruby (`#f48a8e`), yellow (`#ecd06a`) and violet come from the jewel-like facets. Cream text (`#efe9e2`) echoes the pale houses. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

`theme.yaml` is the source. Besides `mode: dark` and the palette, it sets the same consumer color roles as the other Klimt themes: selection colors in the terminals, Qt and Neovim, btop's main text and highlight, opaque Qt placeholder and disabled text, dark text on Yazi's error progress, Neovim's terminal color 8, and primary-accent GTK links. `overrides/starship.toml` is the Starship palette template. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Hyprkarl's theme compiler builds the theme from `theme.yaml` (`hk-theme set klee-municipal-jewel`). It was first generated for the AGS-era layout with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6), using the Klimt templates. The 1.x port renders the same terminal, btop, wifitui, Yazi, Qt, GTK and Starship colors as that build, so the checks below, made on that build, still describe it.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are magenta pink, sapphire, emerald, yellow and violet, with dark text; the trailing segments are deep sapphire and deep ruby.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.96:1**; muted and dim text on the lightest surface are **7.56:1** and **5.74:1**; selection is **7.73:1**. Every terminal color except ANSI black is at least **4.62:1** on every surface. Starship segment text is at least **6.04:1**, every colored segment is at least **7.05:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.62:1**. No desktop theme was activated.
