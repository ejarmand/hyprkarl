-- See https://wiki.hypr.land/Configuring/Basics/Autostart/
hl.on("hyprland.start", function()
    hl.exec_cmd("systemctl --user start hypridle.service")
    hl.exec_cmd("uwsm-app -- mako")
    hl.exec_cmd("uwsm app -- systemctl --user start hyprpolkitagent")
    hl.exec_cmd("uwsm app -- ags run")
    hl.exec_cmd("uwsm app -- hyprpaper")
    hl.exec_cmd("hk-wallpaper init || hk-wallpaper cycle")
    hl.exec_cmd("hk-starship-reload")

    -- Slow app launch fix -- set systemd vars
    hl.exec_cmd("systemctl --user import-environment $(env | cut -d'=' -f 1)")
    hl.exec_cmd("dbus-update-activation-environment --systemd --all")
    hl.exec_cmd("/usr/bin/gnome-keyring-daemon --start --components=secrets")

    -- Mic mute switch -> Wispr hands-free. Before Wispr: its helper only
    -- finds keyboards (this one's virtual keyboard) when it starts.
    hl.exec_cmd("uwsm app -- hk-wispr-switch")

    -- Wispr Flow in the tray (the launcher adds the accessibility flag that
    -- hk-wispr-word-add needs)
    hl.exec_cmd("uwsm app -- ~/.local/bin/wispr-flow --hidden")
end)
