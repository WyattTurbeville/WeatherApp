from geopy.geocoders import Nominatim
import requests
import json

class WeatherData():
    def __init__(self, time, temp, wind_speed, wind_direction, 
                clouds, precipitation):
        self.time= time
        self.temp = temp
        self.wind_speed = wind_speed
        self.wind_dirrection = wind_direction
        self.clouds = clouds
        self.precipitation = precipitation
        
    def __str__(self):
        return f"{self.time}, {self.temp}"
        
p1 = WeatherData(2, 76, 15, "west", "sunny", 2)

print(p1)

##########################

userSearch = "54022, usa" #input from the user to search location

#geolocator API installed into .venv
#establish user agent with OSM database
geolocator = Nominatim(user_agent="Radar-Earth")
location = geolocator.geocode(userSearch)

#pull lat and long from location object
latitude = location.latitude
longitude = location.longitude

#API request for endpoints to NWS using coordinates
response = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
dataPath = response.json()['properties']['forecast']

#use returned endpoint to request .json of weather forecast
response = requests.get(dataPath)
data = response.json()
#print(data)