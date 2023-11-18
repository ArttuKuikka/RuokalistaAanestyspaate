#!/usr/bin/env python3
import json
import sys
import requests
import subprocess

config = ""
with open('config.json', 'r') as f:
    config = json.load(f)
    f.close()

newToken = ""

useSsl = True
    #debug aikana älä käytä ssl
if sys.gettrace() != None:
    useSsl = False


content = {'id': 0, 'username': config["user"], 'password': config["password"]}
headers = {'Content-type': 'application/json'}
response = requests.post(config["base_url"] + "/api/Authenticate/login", headers=headers, json=content, verify=useSsl)

if(response.status_code != 200):
    msg = f"Error while refreshing token: code:{response.status_code} content: {response.content}"
    #webhook error
    raise Exception(msg)
        

responseJson = json.loads(response.content)
newToken = responseJson["token"]

print('new token: ' + newToken)
config["Token"] = newToken

with open('config.json', 'w') as wf:
    json.dump(config, wf)
    wf.close()
print("successfully updated token")


#tarkista toimivuus raspilla ja päivitä tarvittaessa
subprocess.run("sudo systemctl restart ruokalistaPaate.service")
print("successfully reloaded ruokalistapääte")

