import csv
import os
import argparse
import statistics
from test_files.datetime_method import datetime
from operator import itemgetter


class WeatherAnalyzer:
    def __init__(self):
        self.weather_data = {}

    def add_reading(self, date, max_temp, min_temp, mean_humidity):
        year, month, day = date.split('-')
        if year not in self.weather_data:
            self.weather_data[year] = {}
        if month not in self.weather_data[year]:
            self.weather_data[year][month] = []
        self.weather_data[year][month].append({
            'date': date,
            'max_temp': max_temp,
            'min_temp': min_temp,
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
                mean_humidity = float(row[' Mean Humidity']) if row[' Mean Humidity'] else None

                self.add_reading(date, max_temp, min_temp, mean_humidity)

    def get_highest_temperature(self, year=None, month=None):
        relevant_data = []
        if year and month:
            relevant_data = [(entry['date'], entry['max_temp']) for entry in
                             self.weather_data.get(year, {}).get(month, []) if entry['max_temp'] is not None]
        elif year:
            for month_data in self.weather_data.get(year, {}).values():
                relevant_data.extend(
                    [(entry['date'], entry['max_temp']) for entry in month_data if entry['max_temp'] is not None])
        else:
            for year_data in self.weather_data.values():
                for month_data in year_data.values():
                    relevant_data.extend(
                        [(entry['date'], entry['max_temp']) for entry in month_data if entry['max_temp'] is not None])

        if not relevant_data:
            return None, None
        highest_temp_day = max(relevant_data, key=itemgetter(1))
        return highest_temp_day[1], highest_temp_day[0]

    def get_lowest_temperature(self, year=None, month=None):
        relevant_data = []
        if year and month:
            relevant_data = [(entry['date'], entry['min_temp']) for entry in
                             self.weather_data.get(year, {}).get(month, []) if entry['min_temp'] is not None]
        elif year:
            for month_data in self.weather_data.get(year, {}).values():
                relevant_data.extend(
                    [(entry['date'], entry['min_temp']) for entry in month_data if entry['min_temp'] is not None])
        else:
            for year_data in self.weather_data.values():
                for month_data in year_data.values():
                    relevant_data.extend(
                        [(entry['date'], entry['min_temp']) for entry in month_data if entry['min_temp'] is not None])

        if not relevant_data:
            return None, None
        lowest_temp_day = min(relevant_data, key=itemgetter(1))
        return lowest_temp_day[1], lowest_temp_day[0]

    def get_most_humid_day(self, year=None, month=None):
        relevant_data = []
        if year and month:
            relevant_data = [(entry['date'], entry['mean_humidity']) for entry in
                             self.weather_data.get(year, {}).get(month, []) if entry['mean_humidity'] is not None]
        elif year:
            for month_data in self.weather_data.get(year, {}).values():
                relevant_data.extend([(entry['date'], entry['mean_humidity']) for entry in month_data if
                                      entry['mean_humidity'] is not None])
        else:
            for year_data in self.weather_data.values():
                for month_data in year_data.values():
                    relevant_data.extend([(entry['date'], entry['mean_humidity']) for entry in month_data if
                                          entry['mean_humidity'] is not None])

        if not relevant_data:
            return None, None
        most_humid_day = max(relevant_data, key=itemgetter(1))
        return most_humid_day[0], most_humid_day[1]

    def get_average_temperature_humidity(self, year, month):
        month_data = self.weather_data.get(year, {}).get(month, [])
        if not month_data:
            return None, None, None

        max_temps = [entry['max_temp'] for entry in month_data if entry['max_temp'] is not None]
        min_temps = [entry['min_temp'] for entry in month_data if entry['min_temp'] is not None]
        mean_humidities = [entry['mean_humidity'] for entry in month_data if entry['mean_humidity'] is not None]

        avg_max_temp = statistics.mean(max_temps) if max_temps else None
        avg_min_temp = statistics.mean(min_temps) if min_temps else None
        avg_mean_humidity = statistics.mean(mean_humidities) if mean_humidities else None

        return avg_max_temp, avg_min_temp, avg_mean_humidity


def validate_year(year):
    try:
        datetime.strptime(year, "%Y")
        if not (1900 <= int(year) <= datetime.now().year):
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid year: {year}. Year must be between 1900 and {datetime.now().year}.")
    return year


def validate_month(month):
    try:
        datetime.strptime(month, "%m")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid month: {month}. Month must be between 01 and 12.")
    return month


def validate_year_month(year_month):
    try:
        datetime.strptime(year_month, "%Y/%m")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid year/month format: {year_month}. Format must be YYYY/MM.")
    return year_month


def main():
    parser = argparse.ArgumentParser(description='Process weather data.')
    parser.add_argument('directory', type=str, help='Directory path of the weather files')
    parser.add_argument('-c', '--monthly', type=validate_year_month,
                        help='Month to generate monthly report (e.g., 2011/03)')
    parser.add_argument('-a', '--average', type=validate_year_month,
                        help='Month to generate average report (e.g., 2011/03)')
    parser.add_argument('-e', '--yearly', type=validate_year, help='Year to generate yearly report (e.g., 2011)')

    args = parser.parse_args()

    analyzer = WeatherAnalyzer()

    for filename in os.listdir(args.directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(args.directory, filename)
            analyzer.parse_weather_file(file_path)

    if args.yearly:
        year = args.yearly
        highest_temp, highest_temp_day = analyzer.get_highest_temperature(year=year)
        lowest_temp, lowest_temp_day = analyzer.get_lowest_temperature(year=year)
        most_humid_day, max_humidity = analyzer.get_most_humid_day(year=year)

        print(f"For the year {year}:")
        print(f"(a) Highest Temperature: {highest_temp} on {highest_temp_day}")
        print(f"(b) Lowest Temperature: {lowest_temp} on {lowest_temp_day}")
        print(f"(c) Most Humid Day: {most_humid_day} with Humidity {max_humidity}")

    if args.monthly:
        year, month = args.monthly.split('/')
        highest_temp, highest_temp_day = analyzer.get_highest_temperature(year=year, month=month)
        lowest_temp, lowest_temp_day = analyzer.get_lowest_temperature(year=year, month=month)
        most_humid_day, max_humidity = analyzer.get_most_humid_day(year=year, month=month)

        print(f"For the month {args.monthly}:")
        print(f"(a) Highest Temperature: {highest_temp} on {highest_temp_day}")
        print(f"(b) Lowest Temperature: {lowest_temp} on {lowest_temp_day}")
        print(f"(c) Most Humid Day: {most_humid_day} with Humidity {max_humidity}")

    if args.average:
        year, month = args.average.split('/')
        avg_max_temp, avg_min_temp, avg_mean_humidity = analyzer.get_average_temperature_humidity(year=year,
                                                                                                  month=month)

        print(f"For the month {args.average}:")
        print(f"(a) Average Highest Temperature: {avg_max_temp}")
        print(f"(b) Average Lowest Temperature: {avg_min_temp}")
        print(f"(c) Average Mean Humidity: {avg_mean_humidity}")


if __name__ == "__main__":
    main()
