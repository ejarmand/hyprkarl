-- See https://wiki.hypr.land/Configuring/Basics/Variables/ for color info
hl.config({
    general = {
        col = {
            active_border = "{{hyprrgb(hyprland.active_border)}}",
            inactive_border = "{{hyprrgb(hyprland.inactive_border)}}",
        },
    },
    group = {
        col = {
            border_inactive = "{{hyprrgb(hyprland.inactive_border)}}",
        },
    },
})
