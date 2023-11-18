#!/usr/bin/env python3
import requests
import json
import sys
import datetime
from os.path import exists
import RPi.GPIO as GPIO

def aanesta(url, token, taso):
    useSsl = True
    #debug aikana älä käytä ssl
    if sys.gettrace() != None:
        useSsl = False

    headers = {'Authorization': 'Bearer ' + token}
    response = requests.post(url + "?taso=" + str(taso), headers=headers, verify=useSsl)

    if(response.status_code != 200):
        raise Exception(f"HTTP status code exception: code {str(response.status_code)}. response: {str(response.content)}")
    
    if(response.status_code == 200):
        print(f"äänestys onnistui: code:{str(response.status_code)}, taso:{taso}  ({str(datetime.datetime.now())})" )


def main(url, token):
   
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

    GPIO.add_event_detect(10,GPIO.RISING,callback=aanesta(url, token, 1)) # Setup event on pin 10 rising edge

    
   



if __name__ == "__main__":
    filename = "config.json"

    if(exists("config_override.json")):
        filename = "config_override.json"


    with open(filename, 'r') as f:
        config = json.load(f)

    webhookurl = config["webhook_url"]

    try:
        äänestys_url = str(config["base_url"]) + str(config["aanestys_url"])
        token = config["Token"]
        main(äänestys_url, token)
    
    except Exception as e:
        print("error: " + str(e))
        #webhook error code