#!/bin/bash

current_date=$(date "+%d %B %Y")

easter_date=$(ncal -e)

maundy_thursday=$(date -v-3d -j -f "%d %B %Y" "$easter_date" "+%d %B %Y")

if [ "$current_date" == "$maundy_thursday" ]; then
    echo "Echo"
else
    bash $HOME/git/HRPC-YouTube-Scheduler/Shell_Scripts/schedule_good_friday.sh >/Users/odysseus/myscript.log 2>&1
    sleep 10
    bash $HOME/git/HRPC-YouTube-Scheduler/Shell_Scripts/good_friday_website.sh >/Users/odysseus/myscript.log 2>&1
fi