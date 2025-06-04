return {
    "ellisonleao/gruvbox.nvim",
    priority = 1000,
    config = function()
    vim.o.background = "dark" -- or "light" if you want light variant
    vim.cmd("colorscheme gruvbox")
  end,
}

