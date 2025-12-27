#!/bin/bash

FFMPEG_BIN_PATH=$(echo /opt/homebrew/Cellar/ffmpeg/*/bin)
YTDLP_BIN_PATH=$(ls -d /opt/homebrew/Cellar/yt-dlp/* | sort -V | tail -n 1)/libexec/bin

PATH=$PATH:/usr/bin/:$HOME/git/HRPC-YouTube-Scheduler/.venv/bin/:$FFMPEG_BIN_PATH:/bin/:$YTDLP_BIN_PATH

# Set the YouTube channel URL
CHANNEL_URL="https://www.youtube.com/@hrpcbangor/streams"

# Set the path where you want to save the downloaded videos
DOWNLOAD_PATH1="$HOME/git/HRPC-YouTube-Scheduler/Audio"
DOWNLOAD_PATH2="$HOME/Documents/Church_Docs/HRPC_Audio/"
DOWNLOAD_PATH3="$HOME/Documents/Church_Docs/HRPC_Normalised"

# Take the URL from the local file containing the video ID
CHRISTMAS_VIDEO_URL=$(<$HOME/git/HRPC-YouTube-Scheduler/Service_Details/christmas_service_id.txt)
# And the same for the name
CHRISTMAS_VIDEO_NAME=$(<$HOME/git/HRPC-YouTube-Scheduler/Service_Details/christmas_service_title.txt)

#Checks if there is a copy of audio in the iCloud drive folder, if not it proceeds with the download
if [ ! -f "$DOWNLOAD_PATH2$CHRISTMAS_VIDEO_NAME.m4a" ]; then
    # Checks if the morning video livestream has finished then downlaods it if true
    if yt-dlp --flat-playlist --skip-download --print "%(is_live)s" "https://www.youtube.com/watch?v=$CHRISTMAS_VIDEO_URL" | grep -q "False"; then
        # Delete the local file        
        rm "$DOWNLOAD_PATH1/$CHRISTMAS_VIDEO_NAME.m4a"
        # Download the video in audio m4a format
        yt-dlp -x --audio-format m4a -o "$DOWNLOAD_PATH1/%(title)s.%(ext)s" "https://www.youtube.com/watch?v=$CHRISTMAS_VIDEO_URL"
        # Copy to iCloud
        cp "$DOWNLOAD_PATH1/$CHRISTMAS_VIDEO_NAME.m4a" "$DOWNLOAD_PATH2"
        ffmpeg -y -i "$DOWNLOAD_PATH1/$CHRISTMAS_VIDEO_NAME.m4a" -af "dynaudnorm=f=200:g=15, loudnorm=I=-16:TP=-1.5:LRA=8" -b:a 64k "$DOWNLOAD_PATH3/$CHRISTMAS_VIDEO_NAME.mp3"
        New_Name_Morning="${CHRISTMAS_VIDEO_NAME//Service /Service Sermon }"
        mv "$DOWNLOAD_PATH3/$CHRISTMAS_VIDEO_NAME.mp3" "$DOWNLOAD_PATH3/$New_Name_Morning.mp3"
        $HOME/hrpc_po.sh "Download of $CHRISTMAS_VIDEO_NAME finished successfully"
    fi
fi