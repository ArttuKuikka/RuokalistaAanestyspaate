#!/bin/bash

# Path to the Python script
python_script_path=$(pwd)

# Create a temporary file
temp_file=$(mktemp)

# Add the new job entry to the temporary file
echo "*/30 * * * * cd $python_script_path && python3 $python_script_path/uptimePush.py" > "$temp_file"

# Append the content of the existing crontab to the temporary file
crontab -l >> "$temp_file"

# Load the updated crontab from the temporary file
crontab "$temp_file"

# Clean up temporary file
rm "$temp_file"
