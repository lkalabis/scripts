#!/usr/bin/python3
import os
from datetime import datetime, timedelta
import subprocess
import argparse
import sys

# Directory for daily notes
SECOND_BRAIN = os.path.expanduser("~/Documents/private/Notes/work-daily")

# Argument parser setup with formatter for better help output
parser = argparse.ArgumentParser(
    description="A script to manage daily work notes.",
    epilog="""
Examples:
  wday.py                          Opens today's note or creates it if it doesn't exist.
  wday.py -t                       Opens tomorrow's note or creates it if it doesn't exist.
  wday.py -d 15.11.2024            Opens or creates the note for a specific date (e.g., 15th Nov 2024).
  wday.py -r 13.11.2024-20.11.2024 Creates notes for each weekday in the specified date range.
  wday.py "some log entry"         Adds a log entry to today's note.
""",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument(
    "log_entry", nargs="*", help="Optional: Append a log entry to the note."
)
parser.add_argument(
    "-t", "--tomorrow", action="store_true", help="Create or open tomorrow's note."
)
parser.add_argument(
    "-d", "--date", type=str, help="Specify a date for the note in dd.mm.yyyy format."
)
parser.add_argument(
    "-r", "--range", type=str, help="Specify a date range in dd.mm.yyyy-dd.mm.yyyy format (only weekdays will be created)."
)

try:
    # Parse arguments
    args = parser.parse_args()
except SystemExit:
    sys.exit()

# Function to create a note for a specific date
def create_note_for_date(date_str, yesterday_str, tomorrow_str, log_entry=None):
    file_path = os.path.join(SECOND_BRAIN, f"{date_str}.md")
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            file.write(f"""---
id: work-daily_{date_str}
title: work-daily_{date_str}
tags:
  - work-daily
---
# {date_str}

[Yesterday's Note]({yesterday_str}.md) - [Tomorrow's Note]({tomorrow_str}.md)

## Todos

- [ ]

## Log
""")
            # Add log entry if provided
            if log_entry:
                file.write(f"\n- {log_entry}\n")

        print(f"Created note for {date_str} with log entry: {log_entry if log_entry else 'No log entry provided.'}")
    return file_path


# Determine dates based on arguments
if args.range:
    try:
        # Parse start and end dates from range
        start_str, end_str = args.range.split("-")
        start_date = datetime.strptime(start_str, "%d.%m.%Y")
        end_date = datetime.strptime(end_str, "%d.%m.%Y")
    except ValueError:
        print("Invalid date range format. Please use dd.mm.yyyy-dd.mm.yyyy format.")
        sys.exit(1)
    # Prepare log entry if available
    log_entry = " ".join(args.log_entry) if args.log_entry else None

    # Loop through the date range, creating notes only for weekdays
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Only process weekdays (0=Monday, ..., 4=Friday)
            date_str = current_date.strftime("%d-%m-%Y")
            yesterday_str = (current_date - timedelta(days=1)).strftime("%d-%m-%Y")
            tomorrow_str = (current_date + timedelta(days=1)).strftime("%d-%m-%Y")
            create_note_for_date(date_str, yesterday_str, tomorrow_str, log_entry)
        current_date += timedelta(days=1)
    sys.exit()  # Exit after processing the range

elif args.date:
    try:
        specific_date = datetime.strptime(args.date, "%d.%m.%Y")
        today = specific_date.strftime("%d-%m-%Y")
        yesterday = (specific_date - timedelta(days=1)).strftime("%d-%m-%Y")
        tomorrow = (specific_date + timedelta(days=1)).strftime("%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Please use dd.mm.yyyy format.")
        sys.exit(1)

elif args.tomorrow:
    today = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
    tomorrow = (datetime.now() + timedelta(days=2)).strftime("%d-%m-%Y")
    yesterday = datetime.now().strftime("%d-%m-%Y")

else:
    today = datetime.now().strftime("%d-%m-%Y")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")

# Single note creation or log entry logic
file_path = os.path.join(SECOND_BRAIN, f"{today}.md")
if not os.path.isfile(file_path):
    print("File does not exist, creating new daily note.")
    create_note_for_date(today, yesterday, tomorrow)
else:
    # Append log entry if provided and not using range
    if args.log_entry and not args.range:
        log_entry = " ".join(args.log_entry)
        with open(file_path, 'a') as file:
            file.write(f"\n- {log_entry}\n")

# Open the note with nvim if no log entry or only the '-t' or '-d' option is provided
if not args.log_entry or args.tomorrow or args.date:
   subprocess.run(['nvim', '+ normal Gzzo', file_path])
