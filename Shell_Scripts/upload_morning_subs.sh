#!/bin/bash

PATH=$PATH:/opt/homebrew/Cellar
source $HOME/git/HRPC-YouTube-Scheduler/Python/.venv/bin/activate

# Call python script to upload the subtitles
python $HOME/git/HRPC-YouTube-Scheduler/Python/Morning_Subs.py