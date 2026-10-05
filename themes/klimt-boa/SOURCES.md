# Lady with a Hat and Feather Boa

The palette was chosen after downloading and visually inspecting the original reproduction of Gustav Klimt's *Lady with a Hat and Feather Boa*, 1909.

Source image: [Wikimedia Commons file page](https://commons.wikimedia.org/wiki/File:Gustav_Klimt_009.jpg). The original is 2024 × 2501 pixels, from The Yorck Project's 2002 reproduction collection. The file page identifies the artwork and the individual reproduction as public domain, and distinguishes the collection's compilation copyright under the GNU Free Documentation License. This palette's plain background is generated from `base.background`.

The same file page requests a US public-domain tag. Its existing life-term and Yorck PD-Art statements do not resolve that gap. The reproduction was used locally as a palette reference and is not bundled. The only shipped wallpaper is `wallpapers/01-default.png`.

## Palette choices

Violet from the hat, copper rose from the hair and background, ivory from the glove and face, and warm near-black from the feather boa. These are visual adaptations rather than exact pigment measurements. Surfaces are darkened, text is lifted toward cream, and terminal and status colours are brightened to remain readable. Some subdued cool hues are extended into blue and cyan terminal roles so commands and diagnostics retain distinct colours.

`theme.yaml` is the colour source. Besides `mode: dark` and the palette, it sets the consumer colour roles that keep the earlier look (selection, btop text, opaque Qt placeholders, Yazi error progress, Neovim search, primary-accent GTK links). `overrides/starship.toml` is a Starship template whose segment colors are picked from the painting. Neovim keeps a dark background.

## Generation and checks

Hyprkarl's theme compiler builds the theme from `theme.yaml` (`hk-theme set klimt-boa`). It was first generated with [hyprkarl-theme-generator](https://github.com/KarlJussila/hyprkarl-theme-generator) commit `2645fecd819980f7f1c4482cc52deaeb5fc4ee6e` for the AGS-era layout. The 1.x port renders the same terminal, btop, wifitui, Yazi, Qt, GTK and Starship colours as that build, so the checks below, made on that build, still describe it.

Regenerate the plain background with ImageMagick using `magick -size 3840x2160 xc:<base.background> wallpapers/01-default.png` from this theme directory.

Generation completed successfully, including GTK 3 and GTK 4 CSS. Generated TOML files parse, generated configuration has no unresolved template expressions, and bar layout matches Vera-dark.

Contrast was calculated independently with WCAG relative luminance from linear sRGB. Across all five dark surface layers, minimum text/status contrast is 4.56:1. Selection contrast is 8.05:1. Starship segment text is at least 4.71:1; the colored segments are violet hat, copper hair, ivory glove, cool sage and dusty rose, with dark text, and each is at least 5.4:1 against the terminal background. The trailing segments are plum. Prompt glyphs are at least 10.00:1 against the background.

Yazi's error-progress text uses the dark background colour on the error fill, giving 7.26:1. Btop explicitly uses the primary foreground. Qt active and inactive placeholders use the opaque secondary foreground, with at least 6.04:1 across the theme surfaces.

All listed pairs meet 4.5:1. The prompt layout reuses `color_yellow` for the directory segment and the Vim visual-mode glyph. Both are readable. These checks cover opaque palette colours; wallpaper overlays and application-specific opacity can change effective contrast.

The plain background is 3840 × 2160 pixels, filled with `#191418`. No active theme was switched.
