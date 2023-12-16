#!/bin/bash

# Path to the Python script
python_script_path=$(pwd)

# Add the script to crontab to run every 30 minutes
echo "*/30 * * * * cd $python_script_path && python3 $python_script_path/uptimePush.py" >> mycron

# Load the updated crontab
crontab mycron

# Clean up temporary file
rm mycron
