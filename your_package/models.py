from geopy.geocoders import Nominatim
import requests
import json

##########################

class WeatherData:
    def __init__(self, time=None, temp=None, temp_high=None, temp_low=None, wind_speed=None,
                 wind_direction=None, clouds=None, precipitation_chance=None, humidity=None,
                 dewpoint=None, pressure=None, visibility=None):
        self.time= time
        self.temp = temp
        self.temp_high = temp_high 
        self.temp_low = temp_low
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.clouds = clouds
        self.precipitation_chance = precipitation_chance
        self.humidity = humidity
        self.dewpoint = dewpoint
        self.pressure = pressure
        self.visibility = visibility
        
    def __str__(self) -> str:
        return f"This objects temp is {self.temp}"

##########################

class Location:
    def __init__(self, name=None, locationAddress=None, weatherDataSet = []):
        self.name = name
        self.locationAddress = locationAddress
        self.weatherDataSet = weatherDataSet

##########################

class SearchProcessor: #take in user search, returns .json
    def __init__(self):
        pass
        
    def process_search(self, userSearch):
        #geolocator API installed into .venv
        #establish user agent with OSM database
        geolocator = Nominatim(user_agent="Radar-Earth")
        location = geolocator.geocode(userSearch)

        #pull lat and long from location object
        latitude = location.latitude
        longitude = location.longitude

        #API request for endpoints to NWS using coordinates
        response = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
        dataPath = response.json()['properties']['forecastGridData']

        #use returned endpoint to request .json of weather forecast
        response = requests.get(dataPath)
        data = response.json()
        
        return data

##########################

class DataProcessor: #populates and returns Location object
    def __init__(self):
        pass
    
    def process_data(self, data):
        key_attribute_pairs = [
            ('temperature', 'temp'),
            ('windSpeed', 'wind_speed'),
            ('windDirection', 'wind_direction'),
            ('skyCover', 'clouds'),
            ('probabilityOfPrecipitation', 'precipitation_chance'),
            ('relativeHumidity', 'humidity'),
            ('dewpoint', 'dewpoint'),
            ('pressure', 'pressure'),
            ('visibility', 'visibility')
        ]
        key_attribute_pairs2 = [
            ('maxTemperature', 'temp_high'),
            ('minTemperature', 'temp_low')
        ]
        
        hourlyData = []
        
        for i in range(13):
            hour = WeatherData
        
            for key, attribute in key_attribute_pairs:
                try:
                    # Access the value from data using the key
                    value = data['properties'][key]['values'][i]['value']
                    # Set the attribute of hour0 to the retrieved value
                    setattr(hour, attribute, value)
                except (KeyError, IndexError):
                    # Skip if KeyError or IndexError occurs
                    pass
        
            for key, attribute in key_attribute_pairs2:
                try:
                    # Access the value from data using the key
                    value = data['properties'][key]['values'][0]['value']
                    # Set the attribute of hour0 to the retrieved value
                    setattr(hour, attribute, value)
                except (KeyError, IndexError):
                    # Skip if KeyError or IndexError occurs
                    pass

            try:
                # Access the value from data using the key
                value = data['properties']['temperature']['values'][i]['validTime']
                # Set the attribute of hour0 to the retrieved value
                setattr(hour, attribute, value)
            except (KeyError, IndexError):
                # Skip if KeyError or IndexError occurs
                pass
            
            hourlyData.append(hour)
            
        createdLocation = Location("abc", "xyz", hourlyData)
        
        return createdLocation

##########################

class DataPipeline:
    def __init__(self):
        pass
    
    def totalProcess(self, userSearch):
        search_processor = SearchProcessor()
        data_processor = DataProcessor()

        file = search_processor.process_search(userSearch)
        place = data_processor.process_data(file)
        value = place.weatherDataSet[0]
        #so as it turns out, the json index doesnt actually start at local time
        #nor does it start at a set time such as UTC-11
        #it varies from office to office for whatever reason, but the problem is this:
        #if you go to pull data from now to +12h, you must need to know WHERE
        #in the index "now" starts at, bc it is not 0
        
        #problem solved, need to impliment this:
        #location > obtain timezone attribute from Nominatim > create pytz timezone object > 
        #get current time in timezone using datetime > convert to utc
        #this utc can then be used to find where to start the index at :)
        
        return value