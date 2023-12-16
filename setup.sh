#!/bin/bash
#The first time setup script
chmod +x *

# Check if the script is being run as root
if [ "$(id -u)" -eq 0 ]; then
    echo "Script is running as root."
    
else
    echo "Script is not running as root. Please run the script with sudo or as root."
    
    exit 1
fi

#ask if config is set
echo "If config.json hasn't been set, now is a good time to do so"
echo "Continue (Y/N):"

read response

# Convert the response to uppercase for case-insensitive comparison
response=$(echo "$response" | tr '[:lower:]' '[:upper:]')

if [ "$response" = "Y" ]; then
    echo "Continuing..."
    # Add commands to execute when the answer is Yes (Y)
elif [ "$response" = "N" ]; then
    echo "Exiting..."
    # Add commands to execute when the answer is No (N)
else
    echo "Invalid response. Please enter Y or N."
fi

#Ensure depencies
echo "Installing depencies"
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 wget unzip python3-pip
pip3 install requests gpiozero discord_webhook



#create the service
echo "Creating systemd service"
current_directory=$(pwd)

cat >/etc/systemd/system/ruokalista-aanestyspaate.service <<EOL
[Unit]
Description=ruokalista-aanestyspaate

[Service]
ExecStart=python3 ${current_directory}/main.py
Restart=on-failure
RestartSec=100

[Install]
WantedBy=multi-user.target

EOL

sudo systemctl daemon-reload


#enable and start the service
echo "setting service to autostart and starting service"
sudo systemctl enable ruokalista-aanestyspaate.service
sudo systemctl start ruokalista-aanestyspaate.service

#add cronjobs
echo "Adding updateToken cronjob"
./addUpdateTokenCronjob.sh
echo "Adding Uptime cronjob"
./addUptimeCronjob.sh


#add permissions for everyone to start and stop the service
# Add an entry to sudoers file using visudo
echo "Adding entries to sudoers file..."
echo "ALL ALL=(ALL) NOPASSWD: /bin/sudo systemctl start ruokalista-aanestyspaate.service" >> /etc/sudoers
echo "ALL ALL=(ALL) NOPASSWD: /bin/sudo systemctl stop ruokalista-aanestyspaate.service" >> /etc/sudoers
echo "ALL ALL=(ALL) NOPASSWD: /bin/sudo systemctl status ruokalista-aanestyspaate.service" >> /etc/sudoers

# Check for any syntax errors in the sudoers file
echo "Checking sudoers file for syntax errors..."
visudo -c

if [ $? -eq 0 ]; then
    echo "Entry added to sudoers file successfully."
else
    echo "There was an error in the sudoers file. Please check and correct the syntax."
fi