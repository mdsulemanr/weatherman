import os
import argparse
from collections import defaultdict


class WeatherReading:
    def __init__(self, date, max_temp, mean_temp, min_temp, dew_point, mean_dew_point,
                 min_dew_point, max_humidity, mean_humidity, min_humidity,
                 max_pressure, mean_pressure, min_pressure, max_visibility,
                 mean_visibility, min_visibility, max_wind_speed, mean_wind_speed,
                 max_gust_speed, precipitation, cloud_cover, events, wind_direction):
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


class WeatherAnalyzer:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def get_highest_temperature(self):
        highest_temp = float('-inf')
        highest_temp_day = None
        for reading in self.weather_data:
            if reading.max_temp is not None and reading.max_temp > highest_temp:
                highest_temp = reading.max_temp
                highest_temp_day = reading.date
        return highest_temp, highest_temp_day

    def get_lowest_temperature(self):
        lowest_temp = float('inf')
        lowest_temp_day = None
        for reading in self.weather_data:
            if reading.min_temp is not None and reading.min_temp < lowest_temp:
                lowest_temp = reading.min_temp
                lowest_temp_day = reading.date
        return lowest_temp, lowest_temp_day

    def get_most_humid_day(self):
        highest_humidity = float('-inf')
        most_humid_day = None
        for reading in self.weather_data:
            if reading.mean_humidity is not None and reading.mean_humidity > highest_humidity:
                highest_humidity = reading.mean_humidity
                most_humid_day = reading.date
        return most_humid_day, highest_humidity

    def get_average_temperature_humidity(self):
        total_max_temp = 0
        total_min_temp = 0
        total_mean_humidity = 0
        count = 0
        for reading in self.weather_data:
            if reading.max_temp is not None:
                total_max_temp += reading.max_temp
            if reading.min_temp is not None:
                total_min_temp += reading.min_temp
            if reading.mean_humidity is not None:
                total_mean_humidity += reading.mean_humidity
            count += 1
        if count == 0:
            return None, None, None
        avg_max_temp = total_max_temp / count
        avg_min_temp = total_min_temp / count
        avg_mean_humidity = total_mean_humidity / count
        return avg_max_temp, avg_min_temp, avg_mean_humidity


def parse_weather_file(file_path):
    weather_data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        headers = lines[0].strip().split(',')
        for line in lines[1:]:
            data = line.strip().split(',')
            date = data[0]
            max_temp = float(data[1]) if data[1] else None
            mean_temp = float(data[2]) if data[2] else None
            min_temp = float(data[3]) if data[3] else None
            dew_point = float(data[4]) if data[4] else None
            mean_dew_point = float(data[5]) if data[5] else None
            min_dew_point = float(data[6]) if data[6] else None
            max_humidity = float(data[7]) if data[7] else None
            mean_humidity = float(data[8]) if data[8] else None
            min_humidity = float(data[9]) if data[9] else None
            max_pressure = float(data[10]) if data[10] else None
            mean_pressure = float(data[11]) if data[11] else None
            min_pressure = float(data[12]) if data[12] else None
            max_visibility = float(data[13]) if data[13] else None
            mean_visibility = float(data[14]) if data[14] else None
            min_visibility = float(data[15]) if data[15] else None
            max_wind_speed = float(data[16]) if data[16] else None
            mean_wind_speed = float(data[17]) if data[17] else None
            max_gust_speed = float(data[18]) if data[18] else None
            precipitation = float(data[19]) if data[19] else None
            cloud_cover = float(data[20]) if data[20] else None
            events = data[21] if data[21] else None
            wind_direction = float(data[22]) if data[22] else None
            reading = WeatherReading(date, max_temp, mean_temp, min_temp, dew_point, mean_dew_point,
                                     min_dew_point, max_humidity, mean_humidity, min_humidity,
                                     max_pressure, mean_pressure, min_pressure, max_visibility,
                                     mean_visibility, min_visibility, max_wind_speed, mean_wind_speed,
                                     max_gust_speed, precipitation, cloud_cover, events, wind_direction)
            weather_data.append(reading)
    return weather_data


def main():
    parser = argparse.ArgumentParser(description='Process weather data.')
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory path of the weather files')
    parser.add_argument('-c', '--monthly', type=str, help='Month to generate monthly report (e.g., 2011/03)')
    parser.add_argument('-a', '--average', type=str, help='Month to generate average report (e.g., 2011/03)')
    parser.add_argument('-e', '--yearly', type=str, help='Year to generate yearly report (e.g., 2011)')

    args = parser.parse_args()

    weather_data = []
    for filename in os.listdir(args.directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(args.directory, filename)
            weather_data.extend(parse_weather_file(file_path))

    if args.yearly:
        year = args.yearly
        year_data = [reading for reading in weather_data if reading.date.startswith(year)]
        analyzer = WeatherAnalyzer(year_data)

        highest_temp, highest_temp_day = analyzer.get_highest_temperature()
        lowest_temp, lowest_temp_day = analyzer.get_lowest_temperature()
        most_humid_day, max_humidity = analyzer.get_most_humid_day()

        print(f"For the year {year}:")
        print(f"(a) Highest Temperature: {highest_temp} on {highest_temp_day}")
        print(f"(b) Lowest Temperature: {lowest_temp} on {lowest_temp_day}")
        print(f"(c) Most Humid Day: {most_humid_day} with Humidity {max_humidity}")

    if args.monthly:
        year_month = args.monthly.replace('/', '-')
        month_data = [reading for reading in weather_data if reading.date.startswith(year_month)]
        analyzer = WeatherAnalyzer(month_data)

        highest_temp, highest_temp_day = analyzer.get_highest_temperature()
        lowest_temp, lowest_temp_day = analyzer.get_lowest_temperature()
        most_humid_day, max_humidity = analyzer.get_most_humid_day()

        print(f"\nFor the month of {year_month}:")
        print(f"(a) Highest Temperature: {highest_temp} on {highest_temp_day}")
        print(f"(b) Lowest Temperature: {lowest_temp} on {lowest_temp_day}")
        print(f"(c) Most Humid Day: {most_humid_day} with Humidity {max_humidity}")

    if args.average:
        year_month = args.average.replace('/', '-')
        month_data = [reading for reading in weather_data if reading.date.startswith(year_month)]
        analyzer = WeatherAnalyzer(month_data)

        avg_max_temp, avg_min_temp, avg_mean_humidity = analyzer.get_average_temperature_humidity()

        print(f"\nFor the month of {year_month}:")
        print(f"(a) Average Highest Temperature: {avg_max_temp}")
        print(f"(b) Average Lowest Temperature: {avg_min_temp}")
        print(f"(c) Average Mean Humidity: {avg_mean_humidity}")


if __name__ == "__main__":
    main()
