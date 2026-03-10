


***

# 🌙 LUNARVIM TACTICAL FIELD GUIDE
**Designation:** IDE Layer for Neovim
**Primary Trigger (Leader Key):** `<Space>`

## 🧠 The Golden Rule: The "I'm Lost" Menu
If you ever forget a command, press `<Space>` and **take your hands off the keyboard**. 
After 1 second, the `which-key` plugin will pop up at the bottom of the screen showing you every available command and its corresponding key.

To search through *every* mapping in the system:
*   `<Space> s k` : Search Keymaps

---

## 📂 1. Reconnaissance (Finding & Browsing Files)

LunarVim uses **NvimTree** for the side-panel file explorer and **Telescope** for fuzzy finding. Telescope is your best friend.

| Command | Action | Plugin |
| :--- | :--- | :--- |
| `<Space> e` | Toggle File Explorer (left panel) | NvimTree |
| `<Space> f` | **Find Files** (Fuzzy search by name) | Telescope |
| `<Space> s t` | **Search Text** (Live grep across all files) | Telescope |
| `<Space> f r` | Find Recent files | Telescope |
| `<Space> ;` | Return to Dashboard (Alpha screen) | Alpha |

*Inside NvimTree (File Explorer):*
*   `a`: Add a new file/folder.
*   `d`: Delete file.
*   `r`: Rename file.

---

## 🪟 2. Maneuvering (Buffers & Splits)

In LunarVim, "Tabs" at the top of your screen are actually called "Buffers". 

| Command | Action |
| :--- | :--- |
| `<Space> c` | **Close current buffer** (Safely, without breaking layout) |
| `Shift + h` | Go to the **Left** buffer |
| `Shift + l` | Go to the **Right** buffer |
| `Ctrl + h` | Move cursor to the Left window split |
| `Ctrl + j` | Move cursor to the Bottom window split |
| `Ctrl + k` | Move cursor to the Top window split |
| `Ctrl + l` | Move cursor to the Right window split |

---

## 💻 3. Code Execution & Terminals

You don't need a separate Tmux session. LunarVim has built-in floating terminals.

| Command | Action |
| :--- | :--- |
| `Ctrl + \` | **Toggle Floating Terminal** |
| `<Space> r` | **Run Code** *(Custom hook we built in `config.lua`)* |
| `<Space> t f` | Open a floating terminal (Alternative) |
| `<Space> t h` | Open a horizontal terminal split |

*Note: To exit terminal mode and get your normal cursor back inside a terminal split, press `Ctrl + \` or type `exit`.*

---

## 🔬 4. Code Intelligence (LSP)

This is what separates a text editor from an IDE. When you open a Go or Python file, LunarVim automatically attaches a Language Server. Put your cursor over a variable or function and use these:

| Command | Action |
| :--- | :--- |
| `g d` | **Go to Definition** (Jump to where the function is written) |
| `g r` | **Go to References** (See everywhere this variable is used) |
| `K` *(Shift+k)* | **Hover Documentation** (Shows function signature/docs) |
| `g l` | **Line Diagnostics** (Why is this line showing a red error?) |
| `<Space> l f` | **Format File** (Runs Prettier/Black/Gofmt) |
| `<Space> l a` | **Code Actions** (Auto-import, quick fixes) |
| `<Space> l r` | **Rename** (Renames a variable globally across the project) |

---

## ⚙️ 5. Configuration & Overrides

LunarVim is entirely controlled by one file. Do not edit standard Neovim `init.lua` files.

*   **Quick Open Config:** `<Space> L c`
*   **Location:** `~/.config/lvim/config.lua`

**How to map your own keys:**
If you want to create a custom keybind (like `Ctrl+s` to save), you add it to `config.lua` like this:

```lua
-- Standard Vim Mapping (Normal Mode)
lvim.keys.normal_mode["<C-s>"] = ":w<CR>"

-- Which-Key Mapping (Space menu)
lvim.builtin.which_key.mappings["P"] = { "<cmd>Telescope projects<CR>", "Projects" }
```

