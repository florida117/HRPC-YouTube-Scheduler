#!/bin/bash

# Specify the local Macintosh HD directory containing the .m4a files
TARGET_DIR_1="$HOME/git/HRPC-YouTube-Scheduler/Audio"

# Find and delete .m4a files older than 10 days
find "$TARGET_DIR_1" -name "*.m4a" -type f -mtime +10 -exec rm {} \;

# Specify the iCloud directory containing the .m4a files
TARGET_DIR_2="$HOME/Documents/Church_Docs/HRPC_Audio"

# Find and delete .m4a files older than 10 days
find "$TARGET_DIR_2" -name "*.m4a" -type f -mtime +10 -exec rm {} \;

# Specify the iCloud directory containing the .m4a files
TARGET_DIR_3="$HOME/Documents/Church_Docs/HRPC_Normalised"

# Find and delete .m4a files older than 10 days
find "$TARGET_DIR_3" -name "*.mp3" -type f -mtime +10 -exec rm {} \;