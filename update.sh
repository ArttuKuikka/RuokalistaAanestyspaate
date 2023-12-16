#!/bin/bash
user_home_dir=~
file_name=config.json
github_release_download_url="https://api.github.com/repos/ArttuKuikka/RuokalistaAanestyspaate/zipball/Release"

#Copy config to a safe place
echo "Copying $file_name to $user_home_dir"
cp $file_name $user_home_dir


#Download latest release from github
wget -O Release.zip $github_release_download_url

#shutdown the services
sudo systemctl stop ruokalista-aanestyspaate.service

#After downloading is succesfull remove old files and unzip new ones
shopt -s extglob
rm -f !("Release.zip")
shopt -u extglob
echo "All files except Release.zip have been removed."

#unzip new files
unzip Release.zip

#get folder name
# Pattern to match the start of folder names
pattern="ArttuKuikka-RuokalistaAanestyspaate-*"

# Find the first folder matching the pattern
matching_folder=$(find "$directory_path" -type d -name "$pattern" -print -quit)

#copy contents of unzipped file 
cp $matching_folder/* .

#Remove downloaded files
rm -rf $matching_folder/
rm -rf Release.zip

#start the services
sudo systemctl start ruokalista-aanestyspaate.service


