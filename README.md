# Daily Work Notes Script

This repository contains a Python script to help manage and create daily work notes in markdown format. The script supports creating notes for specific dates, as well as for a date range (only weekdays). Additionally, you can add log entries to each note.

## Features

- **Create or open a daily note** for today, tomorrow, or a specific date.
- **Create notes for a range of dates**, with an option to only create notes for weekdays.
- **Add log entries** to the note for the day.

## Requirements

- Python 3.x
- `nvim` (for opening notes in Neovim) or any markdown editor of your choice

## Usage
Create or open tomorrow's note:
```bash
python3 wday.py -t
```
Create or open a note for a specific date:
```bash
python3 wday.py -d 15.11.2024
```
Create notes for a range of dates (weekdays only):
```bash
python3 wday.py -r 13.11.2024-15.11.2024
```
Add a log entry to today's note:
```bash
python3 wday.py -r 13.11.2024-15.11.2024 "Finish reports"
```

## Notes Format
```
---
id: work-daily_dd-mm-yyyy
title: work-daily_dd-mm-yyyy
tags:
  - work-daily
---
# dd-mm-yyyy

[[Yesterday's Note]](dd-mm-yyyy.md) - [[Tomorrow's Note]](dd-mm-yyyy.md)

## Todos

- [ ] 

## Log
- Finish reports
```


# Daily Work Notes to Clarity Markdown Generator

This repository contains two Python scripts designed to help you manage and organize your daily work notes. The scripts are intended to generate a clarity report in markdown format based on your daily notes stored in markdown files.

## Scripts Overview

### 1. **Work Notes Extractor (`clarity.py`)**

This script processes your daily markdown files, extracts entries, and generates a weekly clarity report in markdown format for a specified month.

#### How It Works:
- The script scans a specified directory (`~/Documents/private/Notes/work-daily`) for markdown files with filenames formatted as `DD-MM-YYYY.md`.
- It looks for lines in those markdown files that start with `- C:` (representing clarity entries) and groups them by day.
- It then generates a markdown report that organizes these entries by weeks for a specific month and year.

#### Usage:
1. Clone the repository.
2. Ensure you have your markdown files in the `~/Documents/private/Notes/work-daily` folder, and they are named in the format `DD-MM-YYYY.md`.
3. Run the script by passing the month name as an argument.

```bash
python clarity.py <month_name>
```

### Notes on the README:
- **General Overview**: Describes the purpose of the repository and each script.
- **Usage**: Provides clear steps on how to use the scripts, including examples.
- **Folder Structure**: Details the directory layout, so users know where to place their files and where the output will be saved.
- **Contribution and License**: Adds standard sections for contribution and licensing.

You can customize it further as needed (e.g., adding a `requirements.txt` if you have any dependencies).

