#!/bin/bash
#TODO: restart service

# Path to the Python script
python_script_path=$(pwd)/updateToken.py

# Add the script to crontab to run every week (on Sundays at midnight)
echo "0 0 * * 0 python3 $python_script_path" >> mycron

# Load the updated crontab
crontab mycron

# Clean up temporary file
rm mycron
