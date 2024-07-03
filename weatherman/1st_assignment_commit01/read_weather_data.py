
# Data structure that stores every weather reading
class WeatherReading:
    def __init__(self, date, max_temp, mean_temp, min_temp, dew_point,
                 mean_dew_point, min_dew_point, max_humidity, mean_humidity,
                 min_humidity, max_pressure, mean_pressure, min_pressure,
                 max_visibility, mean_visibility, min_visibility,
                 max_wind_speed, mean_wind_speed, max_gust_speed,
                 precipitation, cloud_cover, events, wind_direction):
        self.date = date
        self.max_temp = max_temp
        self.mean_temp = mean_temp
        self.min_temp = min_temp
        self.dew_point = dew_point
        self.mean_dew_point = mean_dew_point
        self.min_dew_point = min_dew_point
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity
        self.max_pressure = max_pressure
        self.mean_pressure = mean_pressure
        self.min_pressure = min_pressure
        self.max_visibility = max_visibility
        self.mean_visibility = mean_visibility
        self.min_visibility = min_visibility
        self.max_wind_speed = max_wind_speed
        self.mean_wind_speed = mean_wind_speed
        self.max_gust_speed = max_gust_speed
        self.precipitation = precipitation
        self.cloud_cover = cloud_cover
        self.events = events
        self.wind_direction = wind_direction


# Provides weather data as a list of weather reading 'objects'
class WeatherDataParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse_weather_data(self):

        weather_data = []
        # Processing the files and adding entries to the readings structure
        with open(self.file_path, 'r') as file:
            header = next(file).strip().split(',')
            for line in file:
                values = line.strip().split(',')
                if len(values) == len(header):
                    # Assuming all values except date are float or int,
                    # handle empty values as None
                    weather_reading = WeatherReading(
                        date=values[0],
                        max_temp=float(values[1]) if values[1] else None,
                        mean_temp=float(values[2]) if values[2] else None,
                        min_temp=float(values[3]) if values[3] else None,
                        dew_point=float(values[4]) if values[4] else None,
                        mean_dew_point=float(values[5]) if values[5] else None,
                        min_dew_point=float(values[6]) if values[6] else None,
                        max_humidity=int(values[7]) if values[7] else None,
                        mean_humidity=int(values[8]) if values[8] else None,
                        min_humidity=int(values[9]) if values[9] else None,
                        max_pressure=float(values[10]) if values[10] else None,
                        mean_pressure=float(values[11]) if values[11] else None,
                        min_pressure=float(values[12]) if values[12] else None,
                        max_visibility=float(values[13]) if values[13] else None,
                        mean_visibility=float(values[14]) if values[14] else None,
                        min_visibility=float(values[15]) if values[15] else None,
                        max_wind_speed=int(values[16]) if values[16] else None,
                        mean_wind_speed=int(values[17]) if values[17] else None,
                        max_gust_speed=int(values[18]) if values[18] else None,
                        precipitation=float(values[19]) if values[19] else None,
                        cloud_cover=int(values[20]) if values[20] else None,
                        events=values[21],
                        wind_direction=int(values[22]) if values[22] else None
                    )
                    weather_data.append(weather_reading)
        return weather_data
