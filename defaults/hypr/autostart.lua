-- Hyprkarl's login services are started by hk-autostart, so a personal
-- ~/.local/bin/hk-autostart can replace them. Add your own startup commands in
-- ~/.config/hypr/hyprland.local.lua instead.
-- See https://wiki.hypr.land/Configuring/Basics/Autostart/
hl.on("hyprland.start", function()
    hl.exec_cmd("hk-autostart")

    -- Secret Service for apps that keep passwords in the keyring
    hl.exec_cmd("/usr/bin/gnome-keyring-daemon --start --components=secrets")

    -- Mic mute switch -> Wispr hands-free. Before Wispr: its helper only
    -- finds keyboards (this one's virtual keyboard) when it starts.
    hl.exec_cmd("uwsm app -- hk-wispr-switch")

    -- Wispr Flow in the tray (the hk-app launcher adds the accessibility flag
    -- that hk-wispr-word-add needs)
    hl.exec_cmd("uwsm app -- ~/.local/bin/wispr-flow --hidden")
end)
