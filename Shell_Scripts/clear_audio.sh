#!/bin/bash

# Specify the local Macintosh HD directory containing the .m4a files
TARGET_DIR_1="$HOME/git/HRPC-YouTube-Scheduler/Audio"

# Find and delete .m4a files older than 10 days
find "$TARGET_DIR_1" -name "*.m4a" -type f -mtime +10 -exec rm {} \;

# Specify the iCloud directory containing the .m4a files
TARGET_DIR_2="$HOME/Documents/Church_Docs/HRPC_Audio"

# Find and delete .m4a files older than 10 days
find "$TARGET_DIR_2" -name "*.m4a" -type f -mtime +10 -exec rm {} \;

# Specify the iCloud directory containing the normalised .mp3 files
TARGET_DIR_3="$HOME/Documents/Church_Docs/HRPC_Normalised"

# Find and delete normalised.mp3 files older than 10 days
find "$TARGET_DIR_3" -name "*.mp3" -type f -mtime +10 -exec rm {} \;

# Specify the iCloud directory containing the sermon audio files
TARGET_DIR_4="$HOME/Documents/Church_Docs/HRPC_Sermon/Audio"

# Find and delete sermon audio files older than 10 days
find "$TARGET_DIR_4" -name "*.mp3" -type f -mtime +10 -exec rm {} \;

# Specify the iCloud directory containing the sermon transcript files
TARGET_DIR_5="$HOME/Documents/Church_Docs/HRPC_Sermon/Transcript"

# Find and delete sermon audio files older than 10 days
find "$TARGET_DIR_5" -name "*.txt" -type f -mtime +10 -exec rm {} \;

# Specify the iCloud directory containing the sermon summary files
TARGET_DIR_6="$HOME/Documents/Church_Docs/HRPC_Sermon/Summary"

# Find and delete sermon audio files older than 10 days
find "$TARGET_DIR_6" -name "*.txt" -type f -mtime +10 -exec rm {} \;