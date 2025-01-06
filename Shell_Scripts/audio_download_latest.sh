#!/bin/bash

FFMPEG_BIN_PATH=$(echo /opt/homebrew/Cellar/ffmpeg/*/bin)

PATH=$PATH:/usr/bin/:$HOME/git/HRPC-YouTube-Scheduler/.venv/bin/:"$FFMPEG_BIN_PATH":/bin/

# Set the YouTube channel URL
CHANNEL_URL="https://www.youtube.com/@hrpcbangor/streams"

# Set the path where you want to save the downloaded videos
DOWNLOAD_PATH1="$HOME/git/HRPC-YouTube-Scheduler/Audio"
DOWNLOAD_PATH2="$HOME/Documents/Church_Docs/HRPC_Audio/"

# Fetch the latest video URL from the channel
LATEST_VIDEO_URL=$(yt-dlp --flat-playlist --get-id --skip-download "$CHANNEL_URL" --playlist-reverse --playlist-items 1)
LATEST_VIDEO_NAME=$(yt-dlp  --flat-playlist --skip-download   "$CHANNEL_URL" --playlist-reverse --playlist-items 1  --print filename -o "%(title)s")

#Checks if there is a copy of audio in the iCloud drive folder, if not it proceeds with the download
if [ ! -f "$DOWNLOAD_PATH2$LATEST_VIDEO_NAME.m4a" ]; then
    # Checks if the latest video livestream has finished then downloads it if true
    if yt-dlp --flat-playlist --skip-download --print "%(is_live)s" "https://www.youtube.com/watch?v=$LATEST_VIDEO_URL" | grep -q "False"; then
        # Delete the local file
        rm "$DOWNLOAD_PATH1/$LATEST_VIDEO_NAME.m4a"
        # Download the video in m4a audio format
        yt-dlp -x --audio-format m4a -o "$DOWNLOAD_PATH1/%(title)s.%(ext)s" "https://www.youtube.com/watch?v=$LATEST_VIDEO_URL"
        # Copy to iCloud
        cp "$DOWNLOAD_PATH1/$LATEST_VIDEO_NAME.m4a" "$DOWNLOAD_PATH2"
    fi
fi