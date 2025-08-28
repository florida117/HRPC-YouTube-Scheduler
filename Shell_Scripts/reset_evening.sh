#!/bin/bash

# Define the file paths
DIR="/Users/odysseus/git/HRPC-YouTube-Scheduler/Service_Details"
YES_FILE="$DIR/eve_yes.txt"
NO_FILE="$DIR/eve_no.txt"

# Check if eve_no.txt exists and eve_yes.txt does not
if [[ -f "$NO_FILE" && ! -f "$YES_FILE" ]]; then
    mv "$NO_FILE" "$YES_FILE"
    echo "Renamed eve_no.txt back to eve_yes.txt"
else
    echo "No change needed"
fi