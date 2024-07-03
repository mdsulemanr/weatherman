import csv
import os


class WeatherReading:
    def __init__(self, date, max_temp, min_temp,
                 max_humidity, mean_humidity):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity


class WeatherDataParser:

    def parse_weather_data(self, file_path):
        weather_data = []

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            PKT = headers[0]

            for row in reader:
                date = row[PKT]
                try:
                    max_temp = float(row['Max TemperatureC']) if row['Max TemperatureC'] else None
                except ValueError:
                    max_temp = None
                try:
                    min_temp = float(row['Min TemperatureC']) if row['Min TemperatureC'] else None
                except ValueError:
                    min_temp = None
                try:
                    max_humidity = float(row['Max Humidity']) if row['Max Humidity'] else None
                except ValueError:
                    max_humidity = None
                try:
                    mean_humidity = float(row[' Mean Humidity']) if row[' Mean Humidity'] else None
                except ValueError:
                    mean_humidity = None

                reading = WeatherReading(date, max_temp, min_temp, max_humidity, mean_humidity)
                weather_data.append(reading)
        return weather_data

    def get_weather_data(self, directory):
        all_year_weather = []

        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                weather_data = self.parse_weather_data(file_path)
                all_year_weather += weather_data
        return all_year_weather
