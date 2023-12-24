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
import time

useSsl = True
# Variable to track if button presses should be ignored
ignore_button_press = False

class ButtonPressHandler:
    def __init__(self):
        self.last_press_time = 0
        self.press_count = 0

    def handle_button_press(self, url, token, taso):
        global ignore_button_press
        if not ignore_button_press:
            current_time = time.time()
            ignore_button_press = True
            # Check if the button can be pressed based on time elapsed
            if current_time - self.last_press_time >= 3:
                self.last_press_time = current_time
                self.press_count = 1
                print("Äänestetään! taso:" + str(taso))
                try:
                    self.aanesta(url, token, taso)
                except Exception as ex:
                    print("Äänestys error: " + str(ex))

            else:
                # Increment press count if within the time window
                self.press_count += 1
                if self.press_count > 5:
                    print("Exceeded maximum presses. Sleeping for 10 seconds")
                    time.sleep(10)
                    self.last_press_time = time.time()
                    self.press_count = 0
                else:
                    print(f"Button press ignored. Try again after {3 - (current_time - self.last_press_time):.2f} seconds")
            sleep(1)
            ignore_button_press = False
        


    def aanesta(self, url, token, taso):
        headers = {'Authorization': 'Bearer ' + token}
        response = requests.post(url + "?taso=" + str(taso), headers=headers, verify=useSsl)

        if(response.status_code != 200):
            raise Exception(f"HTTP status code exception: code {str(response.status_code)}. response: {str(response.content)}")
        
        if(response.status_code == 200):
            print(f"äänestys onnistui: code:{str(response.status_code)}, taso:{taso}  ({str(datetime.datetime.now())})" )




def main(url, token):
   
    #pinnit numeroitu Broadcom järjestelmällä, lisää https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering

    handler = ButtonPressHandler()
    red_button = Button(6)
    red_button.when_pressed = lambda: handler.handle_button_press(url, token, 1)

    light_red_button = Button(13)
    light_red_button.when_pressed = lambda: handler.handle_button_press(url, token, 2)

    light_green_button = Button(19)
    light_green_button.when_pressed = lambda: handler.handle_button_press(url, token, 3)

    green_button = Button(26)
    green_button.when_pressed = lambda: handler.handle_button_press(url, token, 4)

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