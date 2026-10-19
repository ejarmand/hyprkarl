-- Hyprkarl's login services are started by hk-autostart, so a personal
-- ~/.local/bin/hk-autostart can replace them. Add your own startup commands in
-- ~/.config/hypr/hyprland.local.lua instead.
-- See https://wiki.hypr.land/Configuring/Basics/Autostart/
hl.on("hyprland.start", function()
    hl.exec_cmd("hk-autostart")

    -- Rebuild the Starship prompt from ~/.config/starship.toml and the theme
    hl.exec_cmd("hk-starship-reload")
end)
