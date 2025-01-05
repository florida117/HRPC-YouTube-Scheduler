#!/bin/bash

# Specify the directory containing the files
TARGET_DIR_1="$HOME/git/HRPC-YouTube-Scheduler/Subtitles"

# Find and delete .srt files older than 10 days
find "$TARGET_DIR_1" -name "*.srt" -type f -mtime +10 -exec rm {} \;
# Find and delete .whisper files older than 10 days
find "$TARGET_DIR_1" -name "*.whisper" -type f -mtime +10 -exec rm {} \;


# Specify the directory containing the files
TARGET_DIR_2="$HOME/Documents/Church_Docs/HRPC_Subtitles"

# Find and delete .srt files older than 10 days
find "$TARGET_DIR_2" -name "*.srt" -type f -mtime +10 -exec rm {} \;
# Find and delete .whisper files older than 10 days
find "$TARGET_DIR_2" -name "*.whisper" -type f -mtime +10 -exec rm {} \;