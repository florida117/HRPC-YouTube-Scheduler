#!/bin/bash

PATH=$PATH:/opt/homebrew/Cellar
source $HOME/yt-dlp/HRPC_Python/.venv/bin/activate

# Call python script to upload the subtitles
python $HOME/yt-dlp/HRPC_Python/Evening_Subs.py