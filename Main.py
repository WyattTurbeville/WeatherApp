import requests
import json

response = requests.get("https://api.weather.gov/gridpoints/TOP/31,80/forecast")
data = response.json()
print(data['properties']['periods'][0])