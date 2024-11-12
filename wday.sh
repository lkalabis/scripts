#!/bin/bash

# Directory where the daily notes are stored
SECOND_BRAIN="$HOME/Documents/private/Notes/work-daily"

# Help message function
show_help() {
  cat <<EOF
Usage: $(basename "$0") [OPTION]

A script to manage daily work notes.

Options:
  -h, --help    Show this help message and exit
  -t            Create or open tomorrow's note
EOF
}

# Parse options
while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do
    case $1 in
        -h | --help )
            show_help
            exit 0
            ;;
        -t )
            # Set dates for tomorrow, the day after tomorrow, and today when '-t' is passed
            today=$(date -v +1d +"%d-%m-%Y")    # Tomorrow's date
            tomorrow=$(date -v +2d +"%d-%m-%Y") # Day after tomorrow's date
            yesterday=$(date +"%d-%m-%Y")       # Today's date
            ;;
    esac
    shift
done

# Default to today, tomorrow, and yesterday dates if -t is not specified
today=${today:-$(date +"%d-%m-%Y")}
tomorrow=${tomorrow:-$(date -v +1d +"%d-%m-%Y")}
yesterday=${yesterday:-$(date -v -1d +"%d-%m-%Y")}

# Set the file path for today's note
file="$SECOND_BRAIN/$today.md"

# Change to the notes folder; exit if it doesn't exist
cd "$SECOND_BRAIN" || exit 1

# Function to create a new note with a daily template
new_note() {
	touch "$file" # Create the file if it doesn't exist
	# Write the daily template into the file
	cat <<EOF >"$file"
---
id: work-daily_$today        # Unique identifier for the note
title: work-daily_$today     # Title of the note
tags:
  - work-daily               # Tag to categorize the note
---
# $today

[[$yesterday]] - [[$tomorrow]]  # Links to yesterday's and tomorrow's notes

## Todos

- [ ] 

## Log
EOF
}

# If the daily note does not exist, create it with the template
if [ ! -f "$file" ]; then
	echo "File does not exist, creating new daily note."
	new_note
fi

# Open the note in nvim, place the cursor at the bottom, enter insert mode,
# and apply the NoNeckPain plugin for centering
nvim '+ normal Gzzo' "$file"
