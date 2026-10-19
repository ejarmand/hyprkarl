-- Wispr Flow status pill. Hyprland maps it as a normal window, so it took
-- keyboard focus (dictation pasted into the pill, not your app), and its
-- 512x614 transparent window drew a blurred, dimmed box with the small pill at
-- its bottom centre. Match on the title it maps with ("Status" comes later, too
-- late for map-time rules), keep it out of focus, and park it at the bottom
-- centre. Wispr fixes the window size, so a size rule cannot shrink it.
hl.window_rule({ match = { initial_title = "^(Flow Status Indicator)$" }, tag = "+wispr-pill" })

local function pill(rule)
    rule.match = { tag = "wispr-pill" }
    hl.window_rule(rule)
end

pill({ tag = "-default-opacity" })
pill({ no_focus = true })
pill({ no_initial_focus = true })
pill({ pin = true })
pill({ border_size = 0 })
pill({ no_shadow = true })
pill({ no_blur = true })
pill({ move = { "monitor_w*0.5-window_w*0.5", "monitor_h-window_h-12" } })
