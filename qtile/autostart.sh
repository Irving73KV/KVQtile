#!/bin/bash

function run {
  if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null;
  then
    $@&
  fi
}

# Utilities
run nm-applet &
run volumeicon &
run flameshot &
run nm-applet &
run blueman-applet &
run "conky --daemonize --pause=5" &

picom --config=$HOME/.config/picom/picom.conf &
blueman-applet &
/usr/bin/dunst &
nitrogen --restore &
lxappearance --sync &
picom &
mate-power-manager &





