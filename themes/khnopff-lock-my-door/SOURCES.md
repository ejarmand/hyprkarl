# Khnopff I Lock My Door upon Myself

## Artwork and image

Fernand Khnopff, *I Lock My Door upon Myself*, 1891, oil on canvas, Neue Pinakothek, Munich. The title comes from Christina Rossetti's poem "Who Shall Deliver Me?". Source: the [Wikimedia Commons file](https://commons.wikimedia.org/wiki/File:%22I_Lock_My_Door_upon_Myself%22_de_F._Khnopff_(Petit_Palais,_Paris)_(40377462213).jpg), photographed on 2019-03-10 at the Petit Palais exhibition "Fernand Khnopff. Le maître de l'énigme".

The painting is public domain: Khnopff died in 1921. The photograph is a separate work by [Jean-Pierre Dalbéra](https://www.flickr.com/photos/dalbera/40377462213/), licensed [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/). Credit: Fernand Khnopff, *I Lock My Door upon Myself* (1891), Neue Pinakothek; photograph by Jean-Pierre Dalbéra, CC BY 2.0, via Wikimedia Commons. CC BY 2.0 requires attribution and a link to the license, which this file provides; it does not require share-alike.

The Commons original is 4576 × 2297 pixels (6,602,031 bytes, SHA-1 `eced76555f448000bd657912f631030a0e284ac2`), retrieved 2026-10-06. Changes for the shipped wallpaper, `wallpapers/01-lock-my-door-crop.jpg`, is a 3:2 crop of the original around the figure: 3446 × 2297 pixels starting 300 pixels from the left, scaled to 2880 × 1920 and re-encoded as JPEG (SHA-256 `dc163d52a0b055e4be25bb3591da69598451c364fd9355de6aab6cf19a16af5c`).

The matching plain background is `wallpapers/02-default.png`.

## Palette

The near-black background (`#15191a`) comes from the dark foreground drape. The orange lilies (`#f28a64`) are the primary accent; the blue of Hypnos's wing (`#8aa6f0`), the gilded strip (`#d8bc7a`), the grey-blue panels (`#9cc0cc`) and the olive-grey wall (`#b2bc92`) fill the other roles. Cream text (`#efe9e0`) echoes the marble head. The painting is muted, so these accents are lifted for readable text on a dark background. They were picked by eye and checked as swatches beside the painting element each is named for, not pigment measurements.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` and sassc 3.6.2 (LibSass 3.6.6). `palette.yaml` and `templates/` are the regeneration inputs; see "Regenerate the painting themes" in `docs/themes.md`. The templates are copied from `klimt-hope`, so the bar layout, GTK installation name `hyprkarl`, Foot color sections, Qt paths (`/home/earmand/.config/qt{5,6}ct/`) and other overrides match the Klimt themes. The plain background is 3840 × 2160 pixels in `base.background`: `magick -size 3840x2160 xc:<base.background> wallpapers/02-default.png`.

Starship includes only the palette and leaves the user's prompt layout intact. Its colored segments are Hypnos marble, orange lily, Hypnos wing blue, gilded strip and olive-grey wall, with dark text; the trailing segments are blue cloth and auburn hair.

## Validation

The generator run, including GTK 3/4 compilation, succeeded, and the generated files contain no unresolved template expressions. Contrast uses WCAG relative luminance from linear sRGB. Main text on the background is **14.67:1**; muted and dim text on the lightest surface are **7.45:1** and **5.63:1**; selection is **7.25:1**. Every terminal color except ANSI black is at least **4.76:1** on every surface. Starship segment text is at least **5.08:1**, every colored segment is at least **7.25:1** against the background, and prompt glyphs, including the Vim visual-mode glyph, are at least **7.25:1**. No desktop theme was activated.
