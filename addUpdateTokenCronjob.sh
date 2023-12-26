#!/bin/bash


# Path to the Python script
python_script_path=$(pwd)

# Add the script to crontab to run every week (on Sundays at midnight)
echo "0 0 * * 0 cd $python_script_path && python3 $python_script_path/updateToken.py" >> mycron

# Load the updated crontab
crontab mycron

# Clean up temporary file
rm mycron

sudo systemctl restart ruokalista-aanestyspaate.service
