import os
from collections import defaultdict


class WeatherReading:
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


class WeatherDataParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse_weather_data(self):
        weather_data = []
        with open(self.file_path, 'r') as file:
            header = next(file).strip().split(',')
            for line in file:
                values = line.strip().split(',')
                if len(values) == len(header):
                    weather_reading = WeatherReading(*values)
                    weather_data.append(weather_reading)
        print(weather_data)
        return weather_data


class WeatherAnalyzer:
    def __init__(self):
        self.year_data = defaultdict(list)
        self.month_data = defaultdict(list)

    def process_weather_data(self, weather_data):
        for reading in weather_data:
            # Extract year and month from the date
            year, month, _ = reading.date.split('-')
            self.year_data[year].append(reading)
            self.month_data[month].append(reading)

    def get_year_statistics(self, year):
        if year not in self.year_data:
            return None
        year_data = self.year_data[year]
        highest_temp_reading = max(year_data, key=lambda x: x.max_temp)
        lowest_temp_reading = min(year_data, key=lambda x: x.min_temp)
        most_humid_reading = max(year_data, key=lambda x: x.max_humidity)
        return {
            'highest_temperature': highest_temp_reading.max_temp,
            'highest_temperature_day': highest_temp_reading.date,
            'lowest_temperature': lowest_temp_reading.min_temp,
            'lowest_temperature_day': lowest_temp_reading.date,
            'most_humid_day': most_humid_reading.date,
            'humidity': most_humid_reading.max_humidity
        }

    def get_month_statistics(self, month):
        if month not in self.month_data:
            return None
        month_data = self.month_data[month]
        avg_max_temp = sum(reading.max_temp for reading in month_data) / len(month_data)
        avg_min_temp = sum(reading.min_temp for reading in month_data) / len(month_data)
        avg_mean_humidity = sum(reading.mean_humidity for reading in month_data) / len(month_data)
        return {
            'average_highest_temperature': avg_max_temp,
            'average_lowest_temperature': avg_min_temp,
            'average_mean_humidity': avg_mean_humidity
        }


# Directory containing .txt files
directory = "weather_data"

analyzer = WeatherAnalyzer()

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        parser = WeatherDataParser(file_path)
        weather_data = parser.parse_weather_data()

        # Process weather data
        analyzer.process_weather_data(weather_data)

# Get statistics for a given year
year_statistics = analyzer.get_year_statistics("2004")
print("Statistics for 2004:")
print(year_statistics)

# Get statistics for a given month
month_statistics = analyzer.get_month_statistics("04")
print("\nStatistics for April:")
print(month_statistics)
