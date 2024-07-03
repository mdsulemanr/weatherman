import os


class WeatherReading:

    file_path = os.getcwd() + "/Data/Murree_weather_2004_Aug.txt"

    def __init__(self, date, max_temp, mean_temp, min_temp, dew_point, mean_dew_point, min_dew_point,
                 max_humidity, mean_humidity, min_humidity, max_pressure, mean_pressure, min_pressure,
                 max_visibility, mean_visibility, min_visibility, max_wind_speed, mean_wind_speed, max_gust_speed,
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

    def parse_weather_data(self):
        weather_data = []
        with open(self.file_path, 'r') as file:
            next(file)  # Skip header
            for line in file:
                values = line.strip().split(',')
                # Assuming all values except date are float or int, handle empty values appropriately
                # Create a dictionary for each day's data
                day_data = {
                    self.date: values[0],
                    self.max_temp: values[1] if values[1] else None,
                    self.mean_temp: values[2] if values[2] else None,
                    self.min_temp: values[3] if values[3] else None,
                    self.dew_point: values[4] if values[4] else None,
                    self.mean_dew_point: values[5] if values[5] else None,
                    self.min_dew_point: values[6] if values[6] else None,
                    self.max_humidity: values[7] if values[7] else None,
                    self.mean_humidity: values[8] if values[8] else None,
                    self.min_humidity: values[9] if values[9] else None,
                    self.max_pressure: values[10] if values[10] else None,
                    self.mean_pressure: values[11] if values[11] else None,
                    self.min_pressure: values[12] if values[12] else None,
                    self.max_visibility: values[13] if values[13] else None,
                    self.mean_visibility: values[14] if values[14] else None,
                    self.min_visibility: values[15] if values[15] else None,
                    self.max_wind_speed: values[16] if values[16] else None,
                    self.mean_wind_speed: values[17] if values[17] else None,
                    self.max_gust_speed: values[18] if values[18] else None,
                    self.precipitation: values[19] if values[19] else None,
                    self.cloud_cover: values[20] if values[20] else None,
                    self.events: values[21] if values[21] else None,
                    self.wind_direction: values[22] if values[22] else None
                }
                weather_data.append(day_data)
            return day_data

get_data = WeatherReading.parse_weather_data()
get_data.parse_weather_data()
