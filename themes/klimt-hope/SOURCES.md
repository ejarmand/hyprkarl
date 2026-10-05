# Klimt Hope II

## Artwork and image

Gustav Klimt, *Hope, II* (1907–08), oil, gold and platinum on canvas, The Museum of Modern Art, New York, object 468.1978. The [museum object record](https://www.moma.org/collection/works/79792) verifies the identity; the image source used here is the [Google Art Project reproduction on Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Gustav_Klimt_-_Hope,_II_-_Google_Art_Project.jpg), rather than an installation photograph or a separately supplied MoMA photograph.

Commons labels the artwork public domain and the faithful two-dimensional reproduction PD-Art / [Public Domain Mark 1.0](https://creativecommons.org/publicdomain/mark/1.0/). That label is a rights-status statement, not a Creative Commons license. Credit: Gustav Klimt, *Hope, II*, MoMA; Google Art Project / Wikimedia Commons. Commons notes that faithful reproduction rights may differ between jurisdictions; the record expressly treats the reproduction as public domain in the United States.

[Original Commons JPEG](https://upload.wikimedia.org/wikipedia/commons/7/7c/Gustav_Klimt_-_Hope%2C_II_-_Google_Art_Project.jpg), 3648 × 3699 pixels, 4,159,432 bytes, retrieved 2026-10-05. The unchanged image is `wallpapers/03-hope.jpg`.

SHA-256: `73dca708334a72258153d8fa7bdad84ddbbbeadbac1c0d67dbce3a1ab35c563e`.

Two landscape crops of that same file are also shipped. They change only the framing, orientation and encoding, so they remain faithful reproductions of the public-domain painting:

- `wallpapers/01-hope-figure.jpg`, the default: the upper figure at full resolution, cropped to 2700 × 1800 (3:2) from the top of the original, about 480 pixels from the left edge. SHA-256: `d2a7fca204719c5e26e71122538fab3cf1c50212b2844723d91dc845ff5340d2`.
- `wallpapers/02-hope-lower.jpg`: the lower half of the painting, with its mosaic robe and three bowed heads, rotated 90° and scaled to 2046 × 1364 (3:2). SHA-256: `fe3d810107dd5d3c6ee569aeb0b9b38c254bfff5fe262c3d89310f0bdcd23620`.

Both crops were made by the repository owner and re-encoded as JPEG for size.

## Palette

Visual interpretation of the public image: the olive field becomes a dark olive background (`#212518`); gold ornaments contribute `#edc565`; the orange robe contributes the warm orange-red (`#efa387`); green and cooler textile flecks contribute `#b4ce86`, turquoise, blue and magenta accents. Warm cream text echoes the pale figure. These are adapted colors chosen from looking at the image, not exact pigment measurements. The olive field is darkened and the smaller textile hues lightened to make text readable, with related brighter variants for terminal emphasis. Semantic success/error roles use green/orange-red.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e`. `palette.yaml` and `templates/` are the regeneration inputs. Copy both into the generator's `palettes/klimt-hope/`, then run `python generate.py klimt-hope -o /tmp/klimt-hope` and copy that output into this directory. Preserve `palette.yaml`, `templates/`, `SOURCES.md`, and `wallpapers/` when copying. The plain background is 3840 × 2160 pixels in the palette's background color; wallpapers are kept outside templates to avoid duplicate assets.

Vera-dark overrides preserve the current bar layout, dark GTK preference and `hyprkarl` GTK/Neovim names, explicit Neovim highlights, and both Foot color sections. Qt retains this account's `/home/earmand/.config/qt{5,6}ct/style-colors.conf` paths; another account must adjust them. Additional overrides set btop's main text, make Qt placeholder/disabled text opaque, and use dark text for Yazi error progress. Starship includes only the palette. Its colored segments are persimmon robe, gold, lapis, mosaic green and emerald, with dark text; the trailing segments are bronze and olive-brown. Neighboring segments use different hues, and every colored segment is at least 4.6:1 against the terminal background. It leaves the user's prompt layout intact.

## Validation

Both complete generator runs, including GTK 3/4 compilation with LibSass 0.23, succeeded. Four generated TOML files parsed; Neovim loaded the colors and confirmed a dark `hyprkarl` colorscheme. Hyprland theme Lua parsed and ran against a stub `hl.config`; the complete desktop configuration was not loaded in this check. Foot sections match, bar layout matches Vera-dark, GTK identity is correct, and generated files contain no unresolved template expressions. The generator's shared pytest suite is handled with the combined theme change.

Independent WCAG relative luminance uses linear sRGB, rather than the generator's HSL luminance helper. Checks cover normal/muted/dim text, colored terminal and status text on all theme surfaces, selection, Yazi text pairs, Qt text/placeholder pairs, common GTK secondary and selection text, and current normal Starship segment pairs. ANSI black is a background/decorative color. Disabled GTK controls retain Colloid's reduced opacity and are outside the text target. No desktop theme was activated; native Foot runtime validation was unavailable because Foot is not installed in the build environment.

Measured ratios: main text/background **12.86:1**; muted and dim text on the lightest surface **6.21:1** and **5.31:1**; selection **9.52:1**. The lowest checked ordinary text pair is common GTK secondary text at **4.61:1**. Starship segment text is at least **4.68:1**, and prompt glyphs are at least **7.64:1** against the background.

The prompt layout reuses `color_yellow` for the directory segment and the Vim visual-mode glyph. Both are readable.
