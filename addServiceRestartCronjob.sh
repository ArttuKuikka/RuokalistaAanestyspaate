#!/bin/bash

# Add the script to crontab to run every week (on Sundays at midnight)
echo "0 12 * * * sudo systemctl restart ruokalista-aanestyspaate.service" >> mycron

# Load the updated crontab
crontab mycron

# Clean up temporary file
rm mycron
