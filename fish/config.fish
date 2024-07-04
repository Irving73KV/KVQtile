if status is-interactive
    # Commands to run in interactive sessions can go here
        colorscript -r
  end
export PATH="$PATH:/home/kv/.local/bin"
 
# ALIASES
#
alias ll "ls -l"
alias la "ls -a"
alias r "ranger"
alias nv "nvim"
alias shome "sh ~/Documents/shome.sh"
alias sroot "sh ~/Documents/sroot.sh"
#alias up "sudo dnf upgrade && flatpak update"
#alias in "sudo dnf install -y"
#alias un "sudo dnf remove "
alias up "yay -Syyu && flatpak update"
alias in "yay -S"
alias un "yay -Rcs"
alias sys "sudo systemctl"
alias neofetch "neofetch --ascii_distro arch_small "
