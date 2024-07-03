import csv
import os
import argparse
import statistics


class WeatherAnalyzer:
    def __init__(self):
        self.weather_data = {}

    def add_reading(self, date, max_temp, min_temp, mean_humidity):
        self.weather_data[date] = {
            'max_temp': max_temp,
            'min_temp': min_temp,
            'mean_humidity': mean_humidity
        }

    def parse_weather_file(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                date = row['PKT']
                max_temp = float(row['Max TemperatureC']) if row['Max TemperatureC'] and row[
                    'Max TemperatureC'].replace('.', '', 1).isdigit() else None
                min_temp = float(row['Min TemperatureC']) if row['Min TemperatureC'] and row[
                    'Min TemperatureC'].replace('.', '', 1).isdigit() else None
                mean_humidity = float(row[' Mean Humidity']) if row[' Mean Humidity'] and row[' Mean Humidity'].replace(
                    '.', '', 1).isdigit() else None

                self.add_reading(date, max_temp, min_temp, mean_humidity)

    def get_highest_temperature(self):
        if not self.weather_data:
            return None, None
        highest_temp = float('-inf')
        highest_temp_day = None
        for date, data in self.weather_data.items():
            if data['max_temp'] is not None and data['max_temp'] > highest_temp:
                highest_temp = data['max_temp']
                highest_temp_day = date
        return highest_temp, highest_temp_day

    def get_lowest_temperature(self):
        if not self.weather_data:
            return None, None
        lowest_temp = float('inf')
        lowest_temp_day = None
        for date, data in self.weather_data.items():
            if data['min_temp'] is not None and data['min_temp'] < lowest_temp:
                lowest_temp = data['min_temp']
                lowest_temp_day = date
        return lowest_temp, lowest_temp_day

    def get_most_humid_day(self):
        if not self.weather_data:
            return None, None
        highest_humidity = float('-inf')
        most_humid_day = None
        for date, data in self.weather_data.items():
            if data['mean_humidity'] is not None and data['mean_humidity'] > highest_humidity:
                highest_humidity = data['mean_humidity']
                most_humid_day = date
        return most_humid_day, highest_humidity

    def get_average_temperature_humidity(self):
        max_temps = [data['max_temp'] for data in self.weather_data.values() if data['max_temp'] is not None]
        min_temps = [data['min_temp'] for data in self.weather_data.values() if data['min_temp'] is not None]
        mean_humidities = [data['mean_humidity'] for data in self.weather_data.values() if
                           data['mean_humidity'] is not None]

        avg_max_temp = statistics.mean(max_temps) if max_temps else None
        avg_min_temp = statistics.mean(min_temps) if min_temps else None
        avg_mean_humidity = statistics.mean(mean_humidities) if mean_humidities else None

        return avg_max_temp, avg_min_temp, avg_mean_humidity


def main():
    parser = argparse.ArgumentParser(description='Process weather data.')
    parser.add_argument('directory', type=str, help='Directory path of the weather files')
    parser.add_argument('-c', '--monthly', type=str, help='Month to generate monthly report (e.g., 2011/03)')
    parser.add_argument('-a', '--average', type=str, help='Month to generate average report (e.g., 2011/03)')
    parser.add_argument('-e', '--yearly', type=str, help='Year to generate yearly report (e.g., 2011)')

    args = parser.parse_args()

    analyzer = WeatherAnalyzer()

    for filename in os.listdir(args.directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(args.directory, filename)
            analyzer.parse_weather_file(file_path)

    if args.yearly:
        year = args.yearly
        year_data = {date: data for date, data in analyzer.weather_data.items() if date.startswith(year)}
        yearly_analyzer = WeatherAnalyzer()
        yearly_analyzer.weather_data = year_data

        highest_temp, highest_temp_day = yearly_analyzer.get_highest_temperature()
        lowest_temp, lowest_temp_day = yearly_analyzer.get_lowest_temperature()
        most_humid_day, max_humidity = yearly_analyzer.get_most_humid_day()

        print(f"For the year {year}:")
        print(f"(a) Highest Temperature: {highest_temp} on {highest_temp_day}")
        print(f"(b) Lowest Temperature: {lowest_temp} on {lowest_temp_day}")
        print(f"(c) Most Humid Day: {most_humid_day} with Humidity {max_humidity}")

    if args.monthly:
        year_month = args.monthly.replace('/', '-')
        month_data = {date: data for date, data in analyzer.weather_data.items() if date.startswith(year_month)}
        monthly_analyzer = WeatherAnalyzer()
        monthly_analyzer.weather_data = month_data

        highest_temp, highest_temp_day = monthly_analyzer.get_highest_temperature()
        lowest_temp, lowest_temp_day = monthly_analyzer.get_lowest_temperature()
        most_humid_day, max_humidity = monthly_analyzer.get_most_humid_day()

        print(f"For the month {args.monthly}:")
        print(f"(a) Highest Temperature: {highest_temp} on {highest_temp_day}")
        print(f"(b) Lowest Temperature: {lowest_temp} on {lowest_temp_day}")
        print(f"(c) Most Humid Day: {most_humid_day} with Humidity {max_humidity}")

    if args.average:
        year_month = args.average.replace('/', '-')
        month_data = {date: data for date, data in analyzer.weather_data.items() if date.startswith(year_month)}
        average_analyzer = WeatherAnalyzer()
        average_analyzer.weather_data = month_data

        avg_max_temp, avg_min_temp, avg_mean_humidity = average_analyzer.get_average_temperature_humidity()

        print(f"For the month {args.average}:")
        print(f"(a) Average Highest Temperature: {avg_max_temp}")
        print(f"(b) Average Lowest Temperature: {avg_min_temp}")
        print(f"(c) Average Mean Humidity: {avg_mean_humidity}")


if __name__ == "__main__":
    main()
