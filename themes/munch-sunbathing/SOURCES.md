# Munch Sunbathing

## Artwork and image

Edvard Munch, *Sunbathing*, 1914–15, oil on canvas, Munch Museum, Oslo, MM.M.00062 ([museum record](https://munch.emuseum.com/en/objects/2851/solbad)). Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Edvard_Munch_-_Sunbathing_-_MM.M.00062_-_Munch_Museum.jpg).

Munch died in 1944, so the work is out of copyright in countries with a life-plus-70 term. In the US, a work first published before 1931 is public domain, and an unpublished work's term (life plus 70 years) ended in 2014; only a first publication in 1931 or later could keep it protected. Commons records it as public domain; its publication history has not been independently reconstructed. Commons tags the file PD-Art with `PD-old-auto-expired`, so the faithful reproduction adds no new copyright. Credit: Edvard Munch, *Sunbathing*, Munch Museum / Wikimedia Commons.

The Commons JPEG is 2000 × 1455 pixels (581,445 bytes, SHA-1 `e56ed359e8394d853f1baf3889e2a2f4663d59f7`, matching Commons) and shows the painting in its frame, so no full image is shipped. The default wallpaper, `wallpapers/01-sunbathing-crop.jpg`, is a 3:2 crop of it: 1890 × 1260 pixels starting at x = 55, y = 45, inside the frame, re-encoded as JPEG. SHA-256: `16697b1cc031041e39f22bae42449d4b1e712f50a1a954bd5084149c60a6acef`. The source is small, so this wallpaper is upscaled on most screens, and the crop shows small nude bathers.

The matching plain background is `wallpapers/02-default.png`.

## Palette

The deep blue background (`#151a2a`) darkens the sea. The sea's blue (`#86a8f6`) is the primary accent; the pink sand (`#f0a8c0`), the yellow rocks (`#f0d468`), green (`#92d27c`) and the red-orange of the figures (`#f48e70`) fill the other roles. Cream text (`#f3ebe6`) echoes the pale shore. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

`theme.yaml` is the source. Besides `mode: dark` and the palette, it sets the same consumer color roles as the other Klimt themes: selection colors in the terminals, Qt and Neovim, btop's main text and highlight, opaque Qt placeholder and disabled text, dark text on Yazi's error progress, Neovim's terminal color 8, and primary-accent GTK links. `overrides/starship.toml` is the Starship palette template. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Hyprkarl's theme compiler builds the theme from `theme.yaml` (`hk-theme set munch-sunbathing`). It was first generated for the AGS-era layout with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6), using the Klimt templates. The 1.x port renders the same terminal, btop, wifitui, Yazi, Qt, GTK and Starship colors as that build, so the checks below, made on that build, still describe it.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are yellow rock, sea blue, pink sand, green and red figure, with dark text; the trailing segments are deep sea and plum shadow.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.70:1**; muted and dim text on the lightest surface are **7.32:1** and **5.55:1**; selection is **7.37:1**. Every terminal color except ANSI black is at least **4.74:1** on every surface. Starship segment text is at least **5.45:1**, every colored segment is at least **7.37:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.38:1**. No desktop theme was activated.
