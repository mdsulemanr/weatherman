import csv
import os


class WeatherDataParser:
    def __init__(self):
        self.all_weather_data = {}

    def parse_weather_data(self, file_path):
        weather_data = {}

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            pkr = headers[0]

            for row in reader:
                date = row[pkr]
                weather_info = {
                    "max_temp": int(row['Max TemperatureC']) if row['Max TemperatureC'] else None,
                    "min_temp": int(row['Min TemperatureC']) if row['Min TemperatureC'] else None,
                    "max_humidity": int(row['Max Humidity']) if row['Max Humidity'] else None,
                    "mean_humidity": int(row[' Mean Humidity']) if row[' Mean Humidity'] else None
                }
                weather_data[date] = weather_info
            return weather_data

    def parse_txt_files(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                weather_data = self.parse_weather_data(file_path)
                self.all_weather_data.update(weather_data)
        return self.all_weather_data
