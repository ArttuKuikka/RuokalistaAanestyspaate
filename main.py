#!/usr/bin/env python3
import requests
import json
import sys
import datetime
from os.path import exists
from gpiozero import Button
from gpiozero import LED
from signal import pause
from discord_webhook import DiscordWebhook
from time import sleep
import time

useSsl = True

last_press_time = 0
press_count = 0
isSleeping = False

def setLed(r, g, b, duration):
    red_led = LED(2, active_high=False)
    green_led = LED(3, active_high=False)
    blue_led = LED(4, active_high=False)
    try:
        red_led.value = r
        green_led.value = g
        blue_led.value = b
        sleep(duration)
    finally:
        red_led.close()
        green_led.close()
        blue_led.close()
        
def checkIfInTimeFrame():
    return True

def handle_button_press(url, token, taso):
        if(checkIfInTimeFrame()):
            current_time = time.time()
                
            # Check if the button can be pressed based on time elapsed
            if current_time - last_press_time >= 1.5 and not isSleeping:
                last_press_time = current_time
                press_count = 1
                print("Äänestetään! taso:" + str(taso))
                try:
                    aanesta(url, token, taso)
                    setLed(0, 1, 0, 0.5)
                except Exception as ex:
                    print("Äänestys error: " + str(ex))
                    webhook = DiscordWebhook(url=config["webhook_url"], content="äänestyslaatikko error (main)(http): " + str(ex))
                    webhook.execute()
                    setLed(1, 0, 0, 1)

            else:
                # Increment press count if within the time window
                press_count += 1
                if press_count > 3:
                    print("Exceeded maximum presses. Sleeping for 10 seconds")
                    isSleeping = True
                    time.sleep(10)
                    isSleeping = False
                    last_press_time = time.time()
                    press_count = 0
                else:
                    print(f"Button press ignored. Try again after {3 - (current_time - last_press_time):.2f} seconds")
        else:
            print("Not in timeframe")
            setLed(1,0,0,1)
        

def aanesta(url, token, taso):
        headers = {'Authorization': 'Bearer ' + token}
        response = requests.post(url + "?taso=" + str(taso), headers=headers, verify=useSsl)

        if(response.status_code != 200):
            raise Exception(f"HTTP status code exception: code {str(response.status_code)}. response: {str(response.content)}")
        
        if(response.status_code == 200):
            print(f"äänestys onnistui: code:{str(response.status_code)}, taso:{taso}  ({str(datetime.datetime.now())})" )






def main(url, token):
   
    #pinnit numeroitu Broadcom järjestelmällä, lisää https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering

    
    red_button = Button(6, hold_time=0.05)
    red_button.when_held = lambda: handle_button_press(url, token, 1)

    light_red_button = Button(13, hold_time=0.05)
    light_red_button.when_held = lambda: handle_button_press(url, token, 2)

    light_green_button = Button(19, hold_time=0.05)
    light_green_button.when_held = lambda: handle_button_press(url, token, 3)

    green_button = Button(26, hold_time=0.05)
    green_button.when_held = lambda: handle_button_press(url, token, 4)

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
        setLed(1, 0, 0, 5)