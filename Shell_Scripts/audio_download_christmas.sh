#!/bin/bash

FFMPEG_BIN_PATH=$(echo /opt/homebrew/Cellar/ffmpeg/*/bin)

PATH=$PATH:/usr/bin/:$HOME/yt-dlp/HRPC_Python/.venv/bin/:"$FFMPEG_BIN_PATH":/bin/

# Set the YouTube channel URL
CHANNEL_URL="https://www.youtube.com/@hrpcbangor/streams"

# Set the path where you want to save the downloaded videos
DOWNLOAD_PATH1="$HOME/yt-dlp/Audio"
DOWNLOAD_PATH2="$HOME/Documents/Church_Docs/HRPC_Audio/"

# Take the URL from the local file containing the video ID
CHRISTMAS_VIDEO_URL=$(<$HOME/yt-dlp/christmas_service_id.txt)
# And the same for the name
CHRISTMAS_VIDEO_NAME=$(<$HOME/yt-dlp/christmas_service_title.txt)

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
    fi
fi