class WeatherData:
    #defines needed values to initialize a weather data object
    def __init__(self, temp, windSpeed, windDirection, clouds, 
                 percipitation, windChill):
        self.temp = temp
        self.windSpeed = windSpeed
        self.windDirection = windDirection
        self.clouds = clouds
        self.percipitation = percipitation
        self.windChill = windChill