#!/usr/bin/env python3
import requests
import json
import sys
from datetime import datetime, time
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
globalConfig = ""
ledTurnedOn = False

red_led = LED(2, active_high=False)
green_led = LED(3, active_high=False)
blue_led = LED(4, active_high=False)

count_file_path = 'statistics.txt'


def setLed(r, g, b, duration):

    global ledTurnedOn
    if(not ledTurnedOn):
        try:
            ledTurnedOn = True
            red_led.value = r
            green_led.value = g
            blue_led.value = b
            sleep(duration)
        except gpiozero.exc.GPIOPinInUse:
            print('GPIO in use already')
        finally:
            red_led.value = 0
            green_led.value = 0
            blue_led.value = 0
            ledTurnedOn = False
        
def checkIfInTimeFrame():
    if(globalConfig["RegisterVotesOnlyInTimeFrame"]):
        StartAcceptingVotesTime = datetime.strptime(globalConfig["StartAcceptingVotesTime"], '%H.%M') 
        StopAcceptiongVotesTime = datetime.strptime(globalConfig["StopAcceptiongVotesTime"], '%H.%M') 
        if(datetime.now().time() > StartAcceptingVotesTime.time() and datetime.now().time() < StopAcceptiongVotesTime.time()):
            return True
        else:
            return False
    else:
        return True

def handle_button_press(url, token, taso):
        #log the amount the button has been pressed and tried to be pressed
        LogStatistics(2)

        if(checkIfInTimeFrame()):
            global last_press_time, press_count, isSleeping
            current_time = time.time()

            # Check if the button can be pressed based on time elapsed
            if current_time - last_press_time >= 1.5 and not isSleeping:
                last_press_time = current_time
                press_count = 1
                print("Äänestetään! taso:" + str(taso))
                try:
                    aanesta(url, token, taso)
                    LogStatistics(1)
                except Exception as ex:
                    print("Äänestys error: " + str(ex))
                    CreateWebhookException(str(ex))
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
            print(f"äänestys onnistui: code:{str(response.status_code)}, taso:{taso}  ({str(datetime.now())})" )






def main(url, token):
   
    #pinnit numeroitu Broadcom järjestelmällä, lisää https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering

    
    red_button = Button(6, hold_time=0.05)
    red_button.when_held = lambda: handle_button_press(url, token, 1)

    orange_button = Button(13, hold_time=0.05)
    orange_button.when_held = lambda: handle_button_press(url, token, 2)

    yellow_button = Button(19, hold_time=0.05)
    yellow_button.when_held = lambda: handle_button_press(url, token, 3)

    green_button = Button(26, hold_time=0.05)
    green_button.when_held = lambda: handle_button_press(url, token, 4)

    pause()


def LogStatistics(type):
    #log the amount the button has been pressed and tried to be pressed
    #Type 1 = button was pressed and vote was cast (count succesfull button presses)
    #type 2 = button was pressed (count all buttons presses)

    if not exists(count_file_path):
        with open(count_file_path, 'w') as file:
            file.write("0;0")
            file.close()

    with open(count_file_path, 'r') as file:
        file_content = file.read().strip()
        numbers = file_content.split(';')
        type1number = numbers[0]
        type2number = numbers[1]

        if(type == 1):
            type1number += 1
        if(type == 2):
            type2number += 1
        
        with open(count_file_path, 'w') as file2:
            file2.write(str(type1number) + ';' + str(type2number))
            file.close()
            file2.close()



def CreateWebhookException(msg):

    message = truncate_string(msg, 1800)
    webhook = DiscordWebhook(url=config["webhook_url"], content="äänestyslaatikko error (main): " + message)
    webhook.execute()
    
   
def truncate_string(input_string, max_length):
    if len(input_string) > max_length:
        # Truncate the string if it's longer than the specified maximum length
        truncated_string = input_string[:max_length]
        return truncated_string
    else:
        # Return the original string if it's within the maximum length
        return input_string



if __name__ == "__main__":
    filename = "config.json"

    if(exists("config_override.json")):
        filename = "config_override.json"


    with open(filename, 'r') as f:
        config = json.load(f)

    webhookurl = config["webhook_url"]
    useSsl = config["use_ssl"]
    globalConfig = config

    try:
        äänestys_url = str(config["base_url"]) + str(config["aanestys_url"])
        token = config["Token"]
        main(äänestys_url, token)
    
    except Exception as e:
        print("error: " + str(e))
        CreateWebhookException(str(e))
        setLed(1, 0, 0, 5)
