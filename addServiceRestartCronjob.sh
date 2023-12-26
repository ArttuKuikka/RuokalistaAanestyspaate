#!/bin/bash

# Create a temporary file
temp_file=$(mktemp)

# Add the new job entry to the temporary file
echo "0 12 * * * sudo systemctl restart ruokalista-aanestyspaate.service" > "$temp_file"

# Append the content of the temporary file to the current crontab
crontab -l >> "$temp_file"
crontab "$temp_file"

# Clean up temporary file
rm "$temp_file"
