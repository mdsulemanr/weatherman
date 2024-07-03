import csv
import os


class WeatherDataParser:
    def __init__(self):
        self.all_weather_data = {}

    def add_reading(self, date, max_temp, min_temp, mean_humidity, max_humidity):
        year, month, day = date.split('-')
        if year not in self.all_weather_data:
            self.all_weather_data[year] = {}
        if month not in self.all_weather_data[year]:
            self.all_weather_data[year][month] = []
        self.all_weather_data[year][month].append({
            'date': date,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'max_humidity': max_humidity,
            'mean_humidity': mean_humidity
        })

    def parse_weather_file(self, file_path):

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            header = reader.fieldnames
            pkt = header[0]

            for row in reader:
                date = row[pkt]
                max_temp = float(row['Max TemperatureC']) if row['Max TemperatureC'] else None
                min_temp = float(row['Min TemperatureC']) if row['Min TemperatureC'] else None
                max_humidity = float(row['Max Humidity']) if row['Max Humidity'] else None
                mean_humidity = float(row[' Mean Humidity']) if row[' Mean Humidity'] else None

                self.add_reading(date, max_temp, min_temp, mean_humidity, max_humidity)

    def parse_txt_files(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                self.parse_weather_file(file_path)
        return self.all_weather_data
