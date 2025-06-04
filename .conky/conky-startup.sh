#!/bin/sh

if [ "$DESKTOP_SESSION" = "cinnamon" ]; then 
   sleep 20s
   killall conky
   cd "$HOME/.conky/Gotham"
   conky -c "$HOME/.conky/Gotham/Gotham" &
   exit 0
fi
