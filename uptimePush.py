import requests
import json
from os.path import exists


config = ""
filename = "config.json"

if(exists("config_override.json")):
    filename = "config_override.json"


with open(filename, 'r') as f:
    config = json.load(f)
    f.close()
# URL to perform GET request
url = config["uptimeKumaUrl"]

# Sending GET request using requests library
response = requests.get(url)

# Checking response status
if response.status_code == 200:
    print("GET request successful")
else:
    print(f"Failed to make GET request. Status code: {response.status_code}")
