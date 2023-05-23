import requests
import json
from urllib.parse import urlparse

url = "OPDS URL" # Change to your server's OPDS URL

parsed_url = urlparse(url)

host_address = parsed_url.scheme + "://" + parsed_url.netloc
api_key = parsed_url.path.split('/')[-1]

print("Host Address:", host_address)
print("API Key:", api_key)

login_endpoint = "/api/Plugin/authenticate"
library_endpoint = "/api/Library"
scan_endpoint = "/api/Library/scan-all"
try:
    apikeylogin = requests.post(host_address + login_endpoint + "?apiKey=" + api_key + "&pluginName=pythonScanScript")
    apikeylogin.raise_for_status()
    jwt_token = apikeylogin.json()['token']
#   print("JWT Token:", jwt_token) # Only for debug
except requests.exceptions.RequestException as e:
    print("Error during authentication:", e)
    exit()

headers = {
    "Authorization": f"Bearer {jwt_token}",
    "Content-Type": "application/json"
}
response = requests.get(host_address + library_endpoint, headers=headers)

if response.status_code == 200:
    scan_response = requests.post(host_address + scan_endpoint, headers=headers)
    if scan_response.status_code == 200:
        print(f"Successfully scanned all libraries.")
    else:
        print(f"Failed to scan all libraries.")
        print(scan_response)
else:
    print("Error: Failed to retrieve data from the API.")
