#!/bin/bash

current_date=$(date "+%B %d %Y")
#echo "$current_date"

easter_date=$(ncal -e)
#echo "$easter_date"

maundy_thursday=$(date -v-3d -j -f "%B %d %Y" "$easter_date" "+%B %d %Y")
#echo "$maundy_thursday"

if [ "$current_date" == "$maundy_thursday" ]; then
    bash $HOME/git/HRPC-YouTube-Scheduler/Shell_Scripts/schedule_good_friday.sh >/Users/odysseus/myscript.log 2>&1
    sleep 10
    bash $HOME/git/HRPC-YouTube-Scheduler/Shell_Scripts/good_friday_website.sh >/Users/odysseus/myscript.log 2>&1
else
    echo "Not today"
fi