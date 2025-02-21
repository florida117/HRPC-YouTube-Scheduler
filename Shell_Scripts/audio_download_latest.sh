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

# Fetch the latest video URL from the channel
LATEST_VIDEO_URL=$(yt-dlp --flat-playlist --get-id --skip-download "$CHANNEL_URL" --playlist-reverse --playlist-items 1)
LATEST_VIDEO_NAME=$(yt-dlp  --flat-playlist --skip-download   "$CHANNEL_URL" --playlist-reverse --playlist-items 1  --print filename -o "%(title)s")

#Checks if there is a copy of audio in the iCloud drive folder, if not it proceeds with the download
#if [ ! -f "$DOWNLOAD_PATH2$LATEST_VIDEO_NAME.m4a" ]; then
    # Checks if the latest video livestream has finished then downloads it if true
    if yt-dlp --flat-playlist --skip-download --print "%(is_live)s" "https://www.youtube.com/watch?v=$LATEST_VIDEO_URL" | grep -q "False"; then
        # Delete the local file
        rm "$DOWNLOAD_PATH1/$LATEST_VIDEO_NAME.m4a"
        # Download the video in m4a audio format
        yt-dlp -x --audio-format m4a -o "$DOWNLOAD_PATH1/%(title)s.%(ext)s" "https://www.youtube.com/watch?v=$LATEST_VIDEO_URL"
        # Copy to iCloud
        cp "$DOWNLOAD_PATH1/$LATEST_VIDEO_NAME.m4a" "$DOWNLOAD_PATH2"
        ffmpeg -y -i "$DOWNLOAD_PATH1/$LATEST_VIDEO_NAME.m4a" -af "dynaudnorm=f=200:g=15, loudnorm=I=-16:TP=-1.5:LRA=8" -b:a 64k "$DOWNLOAD_PATH3/$LATEST_VIDEO_NAME.mp3"
        New_Name_Latest="${LATEST_VIDEO_NAME/Service /Service Sermon }"
        mv "$DOWNLOAD_PATH3/$LATEST_VIDEO_NAME.mp3" "$DOWNLOAD_PATH3/$New_Name_Latest.mp3"
        $HOME/hrpc_po.sh "Download of $LATEST_VIDEO_NAME finished successfully"
    fi
#fi