# Hyprkarl

Hyprkarl is a complete desktop for CachyOS + Hyprland, inspired by Omarchy: a
Quickshell bar, menus, launcher, notifications, and lock screen, a theme
system that styles every application at once, and an updater that keeps
Hyprkarl's defaults flowing while your own settings stay yours.

> **Note:** Review `install.sh` before running it on a machine you care about.

## Screenshots

<table>
  <tr>
    <td><img src="themes/hyprkarl/previews/busy.png" alt="Busy desktop"/><br/><sub>Busy desktop</sub></td>
    <td><img src="themes/hyprkarl/previews/launcher.png" alt="App launcher"/><br/><sub>App launcher</sub></td>
  </tr>
  <tr>
    <td><img src="themes/hyprkarl/previews/menu.png" alt="Hyprkarl menu"/><br/><sub>Hyprkarl menu</sub></td>
    <td><img src="themes/hyprkarl/previews/wallpapers.png" alt="Wallpaper picker"/><br/><sub>Wallpaper picker</sub></td>
  </tr>
</table>

## Requirements

- CachyOS with the Hyprland edition, running Hyprland under UWSM (the
  default).
- A single user account; multi-user setups are not supported.
- Btrfs with LUKS encryption and the Limine boot loader are recommended.

Hyprkarl logs in through greetd and starts your session automatically,
relying on disk encryption for the password at boot. To get a login prompt
instead, remove the `[initial_session]` section from `/etc/greetd/config.toml`.

## Installation

```bash
git clone https://github.com/KarlJussila/hyprkarl.git ~/.local/share/hyprkarl
cd ~/.local/share/hyprkarl
./install.sh
```

The installer removes CachyOS's default Noctalia shell first. Configs in
`~/.config/` that Hyprkarl replaces, such as CachyOS's `hyprland.lua`, are
moved to `~/.local/state/hyprkarl/replaced-configs-<date>/`, and the
installer lists them.

To remove Hyprkarl's links again, run `~/.local/share/hyprkarl/uninstall.sh`.
It lists what it leaves behind: your own files, packages, and system changes.

## Making it yours

Your settings live in normal places outside the checkout, such as
`~/.config/hypr/hyprland.local.lua` and
`~/.config/quickshell/settings/shell.json`, and updates never touch them. See
the [configuration map](docs/configuration-map.md) for every location and
[Extending Hyprkarl](docs/extending-hyprkarl.md) for adding your own commands,
menu entries, widgets, and interfaces.

## Themes

`hyprkarl`, `everforest`, `gruvbox`, `loam`, and `tokyo-night` ship with
Hyprkarl. This fork adds:

- `vera-light`: cream paper, blue ink, teal, lavender, and raspberry.
- `vera-dark`: a deep blue background and softer versions of those accents.
- `klimt-music`: petrol, muted gold and rose from the 1895 *Music* study.
- `klimt-hope`: olive, gold and textile accents from *Hope II*.
- `klimt-boa`: warm black, violet and copper from *Lady with a Hat and Feather Boa*.
- `klimt-adele`: deep green, coral, sage and lilac from *Adele Bloch-Bauer II*.
- `klimt-virgin`: violet, cobalt, orange and emerald on warm black from *The Virgin*.
- `klimt-fan`: yellow, turquoise and coral on kimono navy from *Lady with a Fan*.
- `klimt-danae`: gold, copper and veil violet on violet-black from *Danaë*.
- `bonnard-cannet`: orange, agave blue and leaf green on shadow blue from Bonnard's *Le Cannet*.
- `bonnard-ete`: lime grass, flame orange and dress blue on deep foliage from Bonnard's *L'Été*.
- `redon-violette`: violet, mint and cobalt on warm dark from Redon's *Portrait of Violette Heymann*.
- `klee-wald-bau`, `klee-temple-gardens` and `klee-municipal-jewel`: jade and brick, temple orange and teal, and jewel tones from three Paul Klee paintings.
- `kandinsky-intimate-party`: olive-gold, violet and brown-red on slate from Kandinsky's *An Intimate Party*.
- `vrubel-demon`: coral sky, robe blue and crystal lilac on blue-black from Vrubel's *Demon Seated*.
- `van-gogh-irises`: iris blue, leaf teal and marigold on deep green from Van Gogh's *Irises*.
- `van-gogh-crows`: wheat yellow, sky blue and the red-brown path on deep blue from *Wheatfield with Crows*.
- `van-gogh-crabs`: crab orange, sea green and red shell on dark green from *Two Crabs*.
- `munch-linde-beach` and `munch-sunbathing`: the red hat, sand and sea, and the bright shore, from two Edvard Munch paintings.
- `khnopff-lock-my-door`: marble, orange lily and wing blue on near-black from Khnopff's *I Lock My Door upon Myself*.

Both Vera themes include a plain background matching their palette; see [the
Vera theme notes](docs/themes.md#vera-light-and-dark). The Klimt and
other painting themes are dark palettes with Starship prompt colors, 3:2 crops
of their paintings and matching plain backgrounds. The *Music* museum image
and the Bonnard *Le Cannet*, Vrubel and Munch beach photographs are distributed
under CC BY-SA 4.0, and the Khnopff photograph under CC BY 2.0. Each theme's
`SOURCES.md` records its painting reference, image availability and color
adaptations; see [the Klimt theme notes](docs/themes.md#klimt-painting-themes)
and [the other painting themes](docs/themes.md#other-painting-themes). Switch from
`Hyprkarl Menu -> Config -> Theme` or with `hk-theme set <name>`. A theme is one `theme.yaml`; add your own, or override
part of a shipped one, under `~/.config/hyprkarl/themes/`. See
[Themes](docs/themes.md).

<details>
<summary>hyprkarl</summary>

<table>
  <tr>
    <td><img src="themes/hyprkarl/previews/busy.png" alt="Busy desktop"/><br/><sub>Busy desktop</sub></td>
    <td><img src="themes/hyprkarl/previews/launcher.png" alt="App launcher"/><br/><sub>App launcher</sub></td>
  </tr>
  <tr>
    <td><img src="themes/hyprkarl/previews/menu.png" alt="Hyprkarl menu"/><br/><sub>Hyprkarl menu</sub></td>
    <td><img src="themes/hyprkarl/previews/wallpapers.png" alt="Wallpaper picker"/><br/><sub>Wallpaper picker</sub></td>
  </tr>
</table>

</details>

<details>
<summary>everforest</summary>

<table>
  <tr>
    <td><img src="themes/everforest/previews/busy.png" alt="Busy desktop"/><br/><sub>Busy desktop</sub></td>
    <td><img src="themes/everforest/previews/launcher.png" alt="App launcher"/><br/><sub>App launcher</sub></td>
  </tr>
  <tr>
    <td><img src="themes/everforest/previews/menu.png" alt="Hyprkarl menu"/><br/><sub>Hyprkarl menu</sub></td>
    <td><img src="themes/everforest/previews/wallpapers.png" alt="Wallpaper picker"/><br/><sub>Wallpaper picker</sub></td>
  </tr>
</table>

</details>

<details>
<summary>gruvbox</summary>

<table>
  <tr>
    <td><img src="themes/gruvbox/previews/busy.png" alt="Busy desktop"/><br/><sub>Busy desktop</sub></td>
    <td><img src="themes/gruvbox/previews/launcher.png" alt="App launcher"/><br/><sub>App launcher</sub></td>
  </tr>
  <tr>
    <td><img src="themes/gruvbox/previews/menu.png" alt="Hyprkarl menu"/><br/><sub>Hyprkarl menu</sub></td>
    <td><img src="themes/gruvbox/previews/wallpapers.png" alt="Wallpaper picker"/><br/><sub>Wallpaper picker</sub></td>
  </tr>
</table>

</details>

<details>
<summary>loam</summary>

<img src="themes/loam/previews/palette.png" alt="Loam palette" />

<table>
  <tr>
    <td><img src="themes/loam/previews/busy.png" alt="Loam busy desktop"/><br/><sub>Busy desktop</sub></td>
    <td><img src="themes/loam/previews/launcher.png" alt="Loam app launcher"/><br/><sub>App launcher</sub></td>
  </tr>
  <tr>
    <td><img src="themes/loam/previews/menu.png" alt="Loam Hyprkarl menu"/><br/><sub>Hyprkarl menu</sub></td>
    <td><img src="themes/loam/previews/wallpapers.png" alt="Loam wallpaper picker"/><br/><sub>Wallpaper picker</sub></td>
  </tr>
</table>

</details>

<details>
<summary>tokyo-night</summary>

<img src="themes/tokyo-night/previews/palette.png" alt="Tokyo Night palette" />

<table>
  <tr>
    <td><img src="themes/tokyo-night/previews/busy.png" alt="Tokyo Night busy desktop"/><br/><sub>Busy desktop</sub></td>
    <td><img src="themes/tokyo-night/previews/launcher.png" alt="Tokyo Night app launcher"/><br/><sub>App launcher</sub></td>
  </tr>
  <tr>
    <td><img src="themes/tokyo-night/previews/menu.png" alt="Tokyo Night Hyprkarl menu"/><br/><sub>Hyprkarl menu</sub></td>
    <td><img src="themes/tokyo-night/previews/wallpapers.png" alt="Tokyo Night wallpaper picker"/><br/><sub>Wallpaper picker</sub></td>
  </tr>
</table>

</details>

## Keybindings

Search all of them with `SUPER + K`. Your own go in
`~/.config/hypr/hyprland.local.lua`.

```
SUPER + K              ->  Searchable list of keybinds
SUPER + ALT + SPACE    ->  Hyprkarl menu
SUPER + SPACE          ->  App launcher
SUPER + SHIFT + F      ->  File manager (yazi)
SUPER + ENTER          ->  Terminal
SUPER + [0-9]          ->  Navigate to workspace
SUPER + SHIFT + [0-9]  ->  Move window to workspace
SUPER + F              ->  Fullscreen
SUPER + T              ->  Toggle tiling/floating
SUPER + ALT + D        ->  Pause or resume the Wispr mic switch
```

`SUPER + CTRL + SPACE` is left unbound for Wispr Flow's hands-free shortcut.

## Updating

Run `hk-update all`, or click the update icon in the bar when one appears. It
shows what changed, then installs packages, runs one-time migrations, and
applies the new configuration. Releases are tagged `vX.Y.Z` on `main`;
`hk-version` prints yours. See [CHANGELOG.md](CHANGELOG.md) and
[Versions](docs/updating.md#versions).

## Documentation

- [Getting started](docs/getting-started.md)
- [Using Hyprkarl](docs/using-hyprkarl.md): menus, keybindings, themes,
  wallpapers, and utilities
- [Configuration map](docs/configuration-map.md): where everything lives
- [Shell configuration](docs/shell-configuration.md): bar, widgets,
  notifications
- [Menu configuration](docs/menu-configuration.md)
- [Themes](docs/themes.md)
- [Extending Hyprkarl](docs/extending-hyprkarl.md): commands, hooks, QML,
  replacing built-in parts
- [Lock screen and polkit](docs/authentication-surfaces.md)
- [Updating](docs/updating.md) and [Upgrading to 1.0](docs/upgrading-to-1.0.md)
- [Command reference](docs/commands.md)
- [Troubleshooting](docs/troubleshooting.md)
- For contributors: [Repo conventions](docs/repo-conventions.md) and
  [Script style](docs/shell-style.md)
