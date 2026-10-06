-- Name: klimt-danae (loaded as hyprkarl)

local function hl(name, opts)
	vim.api.nvim_set_hl(0, name, opts)
end

vim.cmd("highlight clear")
vim.g.colors_name = "hyprkarl"
vim.opt.background = "dark"

----------------------------------------------------------------
-- Palette
----------------------------------------------------------------

local c = {
	bg = "#19151f",
	surface = "#27212f",
	surface_alt = "#383042",

	fg = "#f1e8dc",
	fg_muted = "#d6ccc0",
	fg_dim = "#bbb1aa",

	black = "#19151f",

	red = "#eb9a5c",
	red_bright = "#ffb48e",

	green = "#a8c890",
	green_bright = "#c2dfaa",

	yellow = "#ecc04a",
	yellow_bright = "#ffd874",

	blue = "#9ea6ec",
	blue_bright = "#bec4ff",

	magenta = "#bd96ee",
	magenta_bright = "#dcc0ff",

	cyan = "#8cc8c4",
	cyan_bright = "#ade0dc",

	white = "#ddd2c6",
	white_bright = "#fff4e8",

	cursor = "#ecc04a",

	border = "#ecc04a",
	border_soft = "#4e402a",

	highlight = "#ffd874",

	accent_primary = "#ecc04a",
	accent_secondary = "#eb9a5c",
	accent_tertiary = "#bd96ee",
}

----------------------------------------------------------------
-- Terminal colors
----------------------------------------------------------------

vim.g.terminal_color_0 = c.black
vim.g.terminal_color_1 = c.red
vim.g.terminal_color_2 = c.green
vim.g.terminal_color_3 = c.yellow
vim.g.terminal_color_4 = c.blue
vim.g.terminal_color_5 = c.magenta
vim.g.terminal_color_6 = c.cyan
vim.g.terminal_color_7 = c.fg

vim.g.terminal_color_8 = "#bbb1aa"
vim.g.terminal_color_9 = c.red_bright
vim.g.terminal_color_10 = c.green_bright
vim.g.terminal_color_11 = c.yellow_bright
vim.g.terminal_color_12 = c.blue_bright
vim.g.terminal_color_13 = c.magenta_bright
vim.g.terminal_color_14 = c.cyan_bright
vim.g.terminal_color_15 = c.white_bright

----------------------------------------------------------------
-- Core UI
----------------------------------------------------------------

hl("Normal", { fg = c.fg, bg = c.bg })
hl("NormalNC", { fg = c.fg, bg = c.surface })

hl("Cursor", { fg = c.bg, bg = c.cursor })
hl("CursorLine", { bg = c.surface })
hl("CursorLineNr", { fg = c.fg, bg = c.surface })

hl("LineNr", { fg = c.fg_dim })
hl("SignColumn", { bg = c.bg })

hl("Visual", { bg = "#ecc04a", fg = "#19151f" })
hl("Search", { fg = "#19151f", bg = "#ecc04a" })
hl("IncSearch", { fg = c.bg, bg = c.accent_primary })

hl("MatchParen", { fg = c.cyan_bright, bold = true })

hl("ColorColumn", { bg = c.surface })
hl("Conceal", { fg = c.fg_dim })

----------------------------------------------------------------
-- Windows / borders
----------------------------------------------------------------

hl("WinSeparator", { fg = c.border_soft })
hl("VertSplit", { fg = c.border_soft })

hl("FloatBorder", { fg = c.border })
hl("FloatTitle", { fg = c.accent_secondary })

hl("NormalFloat", { bg = c.surface })

----------------------------------------------------------------
-- Statusline
----------------------------------------------------------------

hl("StatusLine", { fg = c.fg, bg = c.surface_alt })
hl("StatusLineNC", { fg = c.fg_dim, bg = c.surface })

----------------------------------------------------------------
-- Popup menu
----------------------------------------------------------------

hl("Pmenu", { fg = c.fg_muted, bg = c.surface })
hl("PmenuSel", { fg = c.bg, bg = c.accent_secondary })
hl("PmenuSbar", { bg = c.surface })
hl("PmenuThumb", { bg = c.border })

----------------------------------------------------------------
-- Diagnostics
----------------------------------------------------------------

hl("DiagnosticError", { fg = "#eb9a5c" })
hl("DiagnosticWarn", { fg = "#ecc04a" })
hl("DiagnosticInfo", { fg = c.accent_secondary })
hl("DiagnosticHint", { fg = "#a8c890" })

hl("DiagnosticUnderlineError", { undercurl = true, sp = "#eb9a5c" })
hl("DiagnosticUnderlineWarn", { undercurl = true, sp = "#ecc04a" })
hl("DiagnosticUnderlineInfo", { undercurl = true, sp = c.accent_secondary })
hl("DiagnosticUnderlineHint", { undercurl = true, sp = "#a8c890" })

----------------------------------------------------------------
-- Diff
----------------------------------------------------------------

hl("DiffAdd", { fg = "#a8c890" })
hl("DiffChange", { fg = c.accent_secondary })
hl("DiffDelete", { fg = "#eb9a5c" })
hl("DiffText", { fg = c.accent_primary })

----------------------------------------------------------------
-- Syntax
----------------------------------------------------------------

hl("Comment", { fg = c.fg_dim, italic = true })

hl("Identifier", { fg = c.fg_muted })
hl("Function", { fg = c.magenta_bright })

hl("Statement", { fg = c.blue_bright })
hl("Keyword", { fg = c.cyan, bold = true })

hl("Conditional", { fg = c.cyan })
hl("Repeat", { fg = c.cyan })

hl("Operator", { fg = c.blue })

hl("Constant", { fg = c.cyan })
hl("Number", { fg = c.red })
hl("Boolean", { fg = c.blue_bright })

hl("String", { fg = c.green_bright })

hl("Type", { fg = c.green })
hl("Structure", { fg = c.cyan })

hl("PreProc", { fg = c.blue_bright })

hl("Special", { fg = c.fg })

----------------------------------------------------------------
-- Treesitter
----------------------------------------------------------------

hl("@variable", { link = "Identifier" })
hl("@parameter", { fg = c.cyan_bright })
hl("@field", { fg = c.cyan })

hl("@function", { link = "Function" })
hl("@function.builtin", { fg = c.blue })

hl("@keyword", { link = "Keyword" })
hl("@operator", { link = "Operator" })

hl("@string", { link = "String" })
hl("@number", { link = "Number" })

----------------------------------------------------------------
-- Telescope
----------------------------------------------------------------

hl("TelescopeBorder", { fg = c.border })
hl("TelescopeSelection", { bg = c.surface_alt })
hl("TelescopePromptPrefix", { fg = c.accent_primary })
hl("TelescopeTitle", { fg = c.accent_secondary })

----------------------------------------------------------------
-- NeoTree
----------------------------------------------------------------

hl("NeoTreeDirectoryName", { fg = c.accent_secondary, bold = true })
hl("NeoTreeDirectoryIcon", { fg = c.accent_secondary })

hl("NeoTreeFileName", { fg = c.fg })
hl("NeoTreeFileNameOpened", { fg = c.fg, bold = true })

hl("NeoTreeGitAdded", { fg = "#a8c890" })
hl("NeoTreeGitDeleted", { fg = "#eb9a5c" })
hl("NeoTreeGitModified", { fg = "#ecc04a" })

----------------------------------------------------------------
-- WhichKey
----------------------------------------------------------------

hl("WhichKey", { fg = c.accent_primary })
hl("WhichKeyGroup", { fg = c.accent_secondary })
hl("WhichKeyDesc", { fg = c.fg })
hl("WhichKeyBorder", { link = "FloatBorder" })

----------------------------------------------------------------
-- Indent guides
----------------------------------------------------------------

hl("IndentBlanklineChar", { fg = c.surface_alt })
hl("MiniIndentscopeSymbol", { fg = c.accent_secondary })

----------------------------------------------------------------
-- Markdown
----------------------------------------------------------------

hl("markdownCode", { fg = c.cyan_bright })
hl("markdownHeadingDelimiter", { fg = c.accent_primary })
hl("markdownUrl", { fg = c.accent_secondary, underline = true })