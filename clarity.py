#!/usr/bin/python3
import sys
import calendar
import os
from datetime import datetime, timedelta

# Define the input and output paths for the notes
INPUT_PATH = os.path.expanduser("~/Documents/private/Notes/work-daily")
OUTPUT_PATH = os.path.expanduser("~/Documents/private/Notes/clarity/")

# Function to extract entries from markdown files in a specified folder for a given month and year
def get_entries_from_files(folder, month_num, year):
    entries = {}  # Dictionary to store entries by day
    for filename in os.listdir(folder):
        if filename.endswith(".md"):  # Process only markdown files
            # Try to extract date from filename, if it matches the format "%d-%m-%Y.md"
            try:
                file_date = datetime.strptime(filename, "%d-%m-%Y.md")
            except ValueError:
                continue  # Skip files that do not match the date format

            # If the file's date matches the given month and year, process the file
            if file_date.month == month_num and file_date.year == year:
                with open(os.path.join(folder, filename), 'r') as file:
                    # Iterate through each line in the file and extract entries starting with "- C:"
                    for line in file:
                        if line.startswith("- C:"):
                            day = file_date.day  # Use the day of the file's date
                            if day not in entries:
                                entries[day] = []  # Initialize the entry list for this day if not present
                            entries[day].append(line.strip().replace("- C:", "").strip())  # Add the entry
    return entries

# Function to generate a markdown report for a given month
def generate_markdown(month_name_input):
    # Get the current year
    year = datetime.now().year

    # Map month names to their corresponding numbers (1-12)
    month_number = {month: index for index, month in enumerate(calendar.month_name) if month}

    # Check if the provided month name is valid
    if month_name_input not in month_number:
        print(f"Invalid month name provided: {month_name_input}")
        return

    # Get the numerical representation of the month
    month_num = month_number[month_name_input]

    # Get entries from files for the given month and year
    entries = get_entries_from_files(INPUT_PATH, month_num, year)

    # Get the number of days in the month
    num_days = calendar.monthrange(year, month_num)[1]

    # Start date of the month (first day)
    start_date = datetime(year, month_num, 1)

    # Initialize the markdown output with the month's header
    output = f"# {month_name_input} {year}\n\n"

    current_date = start_date  # Begin at the start of the month

    # Loop through the month, week by week
    while current_date.month == month_num:
        week_start = current_date  # Start of the current week

        # Find the next Friday of the week (weekday 4)
        week_end = week_start
        while week_end.weekday() != 4 and week_end.month == month_num:
            week_end += timedelta(days=1)

        # If the calculated week end goes into the next month, adjust it to the last day of the month
        if week_end.month != month_num:
            week_end = datetime(year, month_num, num_days)

        # Add the week block (start and end dates) to the markdown output
        output += f"## {week_start.strftime('%d.%m.%y')} - {week_end.strftime('%d.%m.%y')}\n"
        
        # Labels for each day of the week
        day_labels = ["Mo", "Di", "Mi", "Do", "Fr"]

        # Loop through each day of the current week
        for i in range((week_end - week_start).days + 1):
            day = week_start + timedelta(days=i)  # Calculate the current day in the loop
            if day.weekday() < 5:  # Process only weekdays (Monday to Friday)
                day_entry = f"[{day_labels[day.weekday()}]"  # Get the corresponding weekday label
                if day.day in entries:
                    day_entry += " " + ", ".join(entries[day.day])  # Add entries for that day if available
                output += day_entry + "\n"

        output += "\n"

        # Move to the next Monday
        current_date = week_end + timedelta(days=3)  # Skip to the next Monday
        while current_date.weekday() != 0 and current_date.month == month_num:
            current_date += timedelta(days=1)

    # Output file name based on the month and year
    output_file = f"{month_name_input}_{year}.md"

    # Write the generated markdown content to the output file
    with open(f"{OUTPUT_PATH}{output_file}", 'w') as file:
        file.write(output)

    # Print a confirmation message
    print(f"Markdown file '{output_file}' has been generated.")

# Main entry point for the script
if __name__ == "__main__":
    # Check if the correct number of arguments is provided (should be one argument: month name)
    if len(sys.argv) != 2:
        print("Usage: python clarity <month_name>")
        sys.exit(1)

    # Retrieve the month name input from the command-line arguments
    month_name_input = sys.argv[1]

    # Generate the markdown report for the given month
    generate_markdown(month_name_input)
