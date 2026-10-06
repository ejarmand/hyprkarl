-- Name: klee-temple-gardens (loaded as hyprkarl)

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
	bg = "#1f1714",
	surface = "#2e241f",
	surface_alt = "#40332c",

	fg = "#f3e8d8",
	fg_muted = "#d8ccbc",
	fg_dim = "#bcb0a2",

	black = "#1f1714",

	red = "#f28462",
	red_bright = "#ffa486",

	green = "#a6cf7a",
	green_bright = "#c2e69c",

	yellow = "#f3a64a",
	yellow_bright = "#ffc072",

	blue = "#93a8d4",
	blue_bright = "#b0c6ff",

	magenta = "#e6a0b6",
	magenta_bright = "#ffbed0",

	cyan = "#6fc8b8",
	cyan_bright = "#92e2d2",

	white = "#e0d4c4",
	white_bright = "#fff6e8",

	cursor = "#f3a64a",

	border = "#f3a64a",
	border_soft = "#543b21",

	highlight = "#ffc072",

	accent_primary = "#f3a64a",
	accent_secondary = "#6fc8b8",
	accent_tertiary = "#f28462",
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

vim.g.terminal_color_8 = "#bcb0a2"
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

hl("Visual", { bg = "#f3a64a", fg = "#1f1714" })
hl("Search", { fg = "#1f1714", bg = "#f3a64a" })
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

hl("DiagnosticError", { fg = "#f28462" })
hl("DiagnosticWarn", { fg = "#f3a64a" })
hl("DiagnosticInfo", { fg = c.accent_secondary })
hl("DiagnosticHint", { fg = "#a6cf7a" })

hl("DiagnosticUnderlineError", { undercurl = true, sp = "#f28462" })
hl("DiagnosticUnderlineWarn", { undercurl = true, sp = "#f3a64a" })
hl("DiagnosticUnderlineInfo", { undercurl = true, sp = c.accent_secondary })
hl("DiagnosticUnderlineHint", { undercurl = true, sp = "#a6cf7a" })

----------------------------------------------------------------
-- Diff
----------------------------------------------------------------

hl("DiffAdd", { fg = "#a6cf7a" })
hl("DiffChange", { fg = c.accent_secondary })
hl("DiffDelete", { fg = "#f28462" })
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

hl("NeoTreeGitAdded", { fg = "#a6cf7a" })
hl("NeoTreeGitDeleted", { fg = "#f28462" })
hl("NeoTreeGitModified", { fg = "#f3a64a" })

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