-- Remove the 1px border / animation around slurp's selection overlay (hk-screenshot)
hl.layer_rule({ match = { namespace = "selection" }, no_anim = true })
