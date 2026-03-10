-- =========================================
-- IRON'S LUNARVIM CONFIGURATION
-- =========================================

-- 1. General Settings
lvim.log.level = "warn"
lvim.format_on_save.enabled = true
lvim.colorscheme = "lunar" -- Default dark theme

-- 2. Core Keybind Fixes
-- This safely closes the current buffer without killing your window layout
lvim.builtin.which_key.mappings["c"] = { "<cmd>BufferKill<CR>", "Close Buffer" }

-- 3. The Custom Code Runner
-- Analyzes filetype, auto-saves, and runs the code in a bottom terminal split.
local function run_code()
  -- Auto-save before running so you don't execute old code
  vim.cmd("silent! w") 

  local ft = vim.bo.filetype
  local fn = vim.fn.expand("%")
  local cmd = ""

  -- Execution routing based on filetype
  if ft == "python" then
    cmd = "python3 " .. fn
  elseif ft == "go" then
    cmd = "go run " .. fn
  elseif ft == "sh" or ft == "bash" then
    cmd = "bash " .. fn
  elseif ft == "javascript" then
    cmd = "node " .. fn
  elseif ft == "c" then
    cmd = "gcc " .. fn .. " -o out && ./out"
  elseif ft == "cpp" then
    cmd = "g++ " .. fn .. " -o out && ./out"
  else
    print("[-] No execution routing configured for filetype: " .. ft)
    return
  end

  -- Open a horizontal terminal of size 15 at the bottom
  vim.cmd("ToggleTerm size=15 direction=horizontal")
  -- Send the command to the terminal
  vim.cmd("TermExec cmd='" .. cmd .. "'")
end

-- Bind the runner to Space + r
lvim.keys.normal_mode["<Leader>r"] = run_code
-- Register it in the Which-Key menu so it looks official
lvim.builtin.which_key.mappings["r"] = { run_code, "Run Current File" }
-- =========================================
-- SYSTEM CLIPBOARD INTEGRATION
-- =========================================
-- Remap the default Yank and Paste commands to use the system clipboard.
-- Now, 'y' and 'p' will work exactly like they do in VSCode or a browser.
vim.keymap.set({"n", "v"}, "y", '"+y')
vim.keymap.set({"n", "v"}, "p", '"+p')
