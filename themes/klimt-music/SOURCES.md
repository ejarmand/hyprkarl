# Klimt Music

## Artwork and image

Gustav Klimt, *Die Musik* (1895), Bayerische Staatsgemäldesammlungen – Neue Pinakothek München, inventory 8195. The [museum object record](https://www.sammlung.pinakothek.de/en/artwork/PdxzY1k4w5) supplies the title, attribution and downloadable image under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Image credit: Bayerische Staatsgemäldesammlungen. Preserve this credit, source link and license when sharing the reproduction; adaptations of the image must use the same license.

[Original museum JPEG](https://cdn.thenetexperts.info/image/authenticated/s--avOTlP_v--/q_80/artworks/GUSTAV-KLIMT-1862_DIE-MUSIK-8195_936137_CC-BY-SA_BSTGS.jpg), 3000 × 2345 pixels, 1,097,957 bytes, retrieved 2026-10-05. The unchanged image is `wallpapers/01-music.jpg`; its license applies to that reproduction separately from the theme configuration.

SHA-256: `5474ed50bfa5edeb829d2b0d5c2294a42a014c3ead8b305d38568b92cdf9651e`.

The full image license is preserved in `ARTWORK-LICENSE.txt`, downloaded from the [official CC BY-SA 4.0 legal text](https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt). The matching plain background is `wallpapers/02-default.png`.

## Palette

Visual interpretation of the museum image: the blue field and robe become a dark petrol background (`#19272b`); the lyre contributes muted gold (`#dfbb72`); rose details contribute `#d6b0c9`; weathered green-blue notes contribute `#a1c9c4`. Cream text echoes the warm pale areas. These colors were chosen by looking at the public image, not asserted as exact pigment measurements. Small painted accents were lightened and the blue field darkened for readable terminal text; the semantic red/green pair follows the same subdued warmth. Surface layers stay blue-gray rather than becoming neutral black.

## Generation and compatibility

Generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e`. `palette.yaml` and `templates/` are the regeneration inputs. Copy both into the generator's `palettes/klimt-music/`, then run `python generate.py klimt-music -o /tmp/klimt-music` and copy that output into this directory. Preserve `palette.yaml`, `templates/`, `SOURCES.md`, and `wallpapers/` when copying. The plain background is 3840 × 2160 pixels in the palette's background color; wallpapers are kept outside templates to avoid duplicate assets.

Vera-dark overrides preserve the current bar layout, dark GTK preference and `hyprkarl` GTK/Neovim names, explicit Neovim highlights, and both Foot color sections. Qt retains this account's `/home/earmand/.config/qt{5,6}ct/style-colors.conf` paths; another account must adjust them. Additional overrides set btop's main text, make Qt placeholder/disabled text opaque, and use dark text for Yazi error progress. Starship includes only the palette. Its colored segments are lyre gold, the lavender-grey bow, terracotta hair, turquoise and pale green, with dark text; the trailing segments are the blue-green inside the harp and the brown of the hair. Neighboring segments use different hues, and every colored segment is at least 5.3:1 against the terminal background. It leaves the user's prompt layout intact.

## Validation

Both complete generator runs, including GTK 3/4 compilation with LibSass 0.23, succeeded. Four generated TOML files parsed; Neovim loaded the colors and confirmed a dark `hyprkarl` colorscheme. Hyprland theme Lua parsed and ran against a stub `hl.config`; the complete desktop configuration was not loaded in this check. Foot sections match, bar layout matches Vera-dark, GTK identity is correct, and generated files contain no unresolved template expressions. The generator's shared pytest suite is handled with the combined theme change.

Independent WCAG relative luminance uses linear sRGB, rather than the generator's HSL luminance helper. Checks cover normal/muted/dim text, colored terminal and status text on all theme surfaces, selection, Yazi text pairs, Qt text/placeholder pairs, common GTK secondary and selection text, and current normal Starship segment pairs. ANSI black is a background/decorative color. Disabled GTK controls retain Colloid's reduced opacity and are outside the text target. No desktop theme was activated; native Foot runtime validation was unavailable because Foot is not installed in the build environment.

Measured ratios: main text/background **12.54:1**; muted and dim text on the lightest surface **5.43:1** and **4.88:1**; selection **8.41:1**. The lowest checked ordinary text pair is common GTK secondary text at **4.53:1**. Starship segment text is at least **5.31:1**, and prompt glyphs are at least **8.10:1** against the background.

The prompt layout reuses `color_yellow` for the directory segment and the Vim visual-mode glyph. Both are readable.
