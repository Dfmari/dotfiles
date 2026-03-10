# ==============================================================================
#  SAWAYAMA Z7 TURBOLANCE - SYSTEM CONFIGURATION 
# ==============================================================================
# --- 1. BOOT SEQUENCE & TELEMETRY ---
export GOPATH="$HOME/go"
export PYENV_ROOT="$HOME/.pyenv"
export EDITOR="nvim"
export PATH="$HOME/.local/bin:/usr/local/go/bin:$GOPATH/bin:$HACK_BASE/scripts:$HACK_BASE/bin:$PYENV_ROOT/bin:/usr/games:$PATH"
if [[ -z "$NVIM" && -z "$LUNARVIM_RUNTIME_DIR" && -z "$TMUX" && "$-" == *i* ]]; then
    z7_hud
fi
# --- 2. ZSH CORE SETTINGS ---
setopt autocd notify numericglobsort promptsubst hist_ignore_space hist_verify
bindkey -e
bindkey ' ' magic-space
bindkey '^[[H' beginning-of-line
bindkey '^[[F' end-of-line

HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt hist_expire_dups_first hist_ignore_dups share_history

# --- 3. ALIASES ---
alias vpn='ssh vpn'
alias c2='ssh c2'
alias update='sudo pacman -Syu'
alias ipinfo="curl -s ipinfo.io | jq -r 'to_entries[] | [.key, .value] | @tsv' | column -t"
alias ls='ls --color=auto'
alias ll='ls -l'
alias la='ls -A'
alias grep='grep --color=auto'
alias py='python3'

# --- 5. PLUGINS ---
if [ -f /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh ]; then
    source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
    ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=#555'
fi
if [ -f /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]; then
    source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
fi

# --- 6. POWERLEVEL10K (ENABLED) ---
source ~/powerlevel10k/powerlevel10k.zsh-theme
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# --- 7. INIT ---
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
