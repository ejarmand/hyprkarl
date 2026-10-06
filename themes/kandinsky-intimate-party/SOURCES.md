# Kandinsky An Intimate Party

## Artwork and image

Wassily Kandinsky, *An Intimate Party*, 1942. Reference: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:Kandinsky,_Wassily_-_An_Intimate_Party,_1942,_GAC.jpg), from Google Arts & Culture.

No image of the painting is bundled. Kandinsky died in 1944, so the work is out of copyright in countries with a life-plus-70 term. Commons tags it `PD-old-auto-expired`, but that tag's US basis covers works published before 1931, and this painting dates from 1942. Its US status is unresolved, so, as with `klimt-boa`, the reproduction was used locally as a palette reference only. The only shipped wallpaper is the plain `wallpapers/01-default.png`.

## Palette

The dark slate background (`#161d22`) deepens the painting's blue-grey ground. The olive-gold of the large circle (`#d4c060`) is the primary accent; violet (`#b8a0f2`), the brown-red bars (`#ec9a7e`), the pale blue ring (`#8fc6dc`) and green (`#9fcf8a`) fill the other roles. Cream text (`#ece7dc`) echoes the white outlines. These colors were picked by eye and checked as swatches beside the painting element each is named for; they are adapted for readable text on a dark background, not pigment measurements.

## Generation and compatibility

`theme.yaml` is the source. Besides `mode: dark` and the palette, it sets the same consumer color roles as the other Klimt themes: selection colors in the terminals, Qt and Neovim, btop's main text and highlight, opaque Qt placeholder and disabled text, dark text on Yazi's error progress, Neovim's terminal color 8, and primary-accent GTK links. `overrides/starship.toml` is the Starship palette template. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/01-default.png`.

Hyprkarl's theme compiler builds the theme from `theme.yaml` (`hk-theme set kandinsky-intimate-party`). It was first generated for the AGS-era layout with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6), using the Klimt templates. The 1.x port renders the same terminal, btop, wifitui, Yazi, Qt, GTK and Starship colors as that build, so the checks below, made on that build, still describe it.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are gold circle, violet, pale blue ring, brown-red and green, with dark text; the trailing segments are slate and maroon.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **13.81:1**; muted and dim text on the lightest surface are **6.74:1** and **5.10:1**; selection is **9.33:1**. Every terminal color except ANSI black is at least **4.62:1** on every surface. Starship segment text is at least **6.02:1**, every colored segment is at least **7.58:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.58:1**. No desktop theme was activated.
