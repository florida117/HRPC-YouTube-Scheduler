#!/bin/bash

if test -f $HOME/yt-dlp/eve_no.txt; then
    sudo mv $HOME/yt-dlp/eve_no.txt $HOME/yt-dlp/eve_yes.txt
fi
