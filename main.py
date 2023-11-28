#!/usr/bin/env python3
import requests
import json
import sys
import datetime
from os.path import exists
from gpiozero import Button
from signal import pause
from discord_webhook import DiscordWebhook
from time import sleep

useSsl = True

def aanesta(url, token, taso):
    print(f"taso {taso} nappia painettu")
   
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.post(url + "?taso=" + str(taso), headers=headers, verify=useSsl)

    if(response.status_code != 200):
        raise Exception(f"HTTP status code exception: code {str(response.status_code)}. response: {str(response.content)}")
    
    if(response.status_code == 200):
        print(f"äänestys onnistui: code:{str(response.status_code)}, taso:{taso}  ({str(datetime.datetime.now())})" )
    sleep(0.8)


def main(url, token):
   
    #pinnit numeroitu Broadcom järjestelmällä, lisää https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering

    red_button = Button(6)
    red_button.when_pressed = lambda: aanesta(url, token, 1)

    light_red_button = Button(13)
    light_red_button.when_pressed = lambda: aanesta(url, token, 2)

    light_green_button = Button(19)
    light_green_button.when_pressed = lambda: aanesta(url, token, 3)

    green_button = Button(26)
    green_button.when_pressed = lambda: aanesta(url, token, 4)

    pause()

    
   



if __name__ == "__main__":
    filename = "config.json"

    if(exists("config_override.json")):
        filename = "config_override.json"


    with open(filename, 'r') as f:
        config = json.load(f)

    webhookurl = config["webhook_url"]
    useSsl = config["use_ssl"]

    try:
        äänestys_url = str(config["base_url"]) + str(config["aanestys_url"])
        token = config["Token"]
        main(äänestys_url, token)
    
    except Exception as e:
        print("error: " + str(e))
        webhook = DiscordWebhook(url=config["webhook_url"], content="äänestyslaatikko error (main): " + str(e))
        webhook.execute()