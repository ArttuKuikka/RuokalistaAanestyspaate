#!/bin/bash

# Path to the Python script
python_script_path=$(pwd)/uptimePush.py

# Add the script to crontab to run every 30 minutes
echo "*/30 * * * * python3 $python_script_path" >> mycron

# Load the updated crontab
crontab mycron

# Clean up temporary file
rm mycron
