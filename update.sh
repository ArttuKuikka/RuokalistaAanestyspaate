#!/bin/bash
user_home_dir=~
file_name=config.json
github_release_download_url="https://github.com/ArttuKuikka/RuokalistaAanestyspaate/archive/refs/tags/Release.zip"

#Copy config to a safe place
echo "Copying $file_name to $user_home_dir"
cp $file_name $user_home_dir


#Download latest release from github
wget $github_release_download_url

#shutdown the services
sudo systemctl stop ruokalista-aanestyspaate.service

#After downloading is succesfull remove old files and unzip new ones
shopt -s extglob
rm -f !("Release.zip")
shopt -u extglob
echo "All files except Release.zip have been removed."

#unzip new files
unzip Release.zip

#copy contents of unzipped file 
cp RuokalistaAanestyspaate-Release/* .

#Remove downloaded files
rm -rf RuokalistaAanestyspaate-Release/
rm -rf Release.zip

#start the services
sudo systemctl start ruokalista-aanestyspaate.service


