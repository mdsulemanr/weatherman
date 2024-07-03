import os


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


# Returns weather data for all .txt files as object
class GetWeatherData:
    # Directory containing .txt files
    directory = "weather_data"
    # store all weather objects
    all_year_weather = []

    def all_weather_data(self):
        # Recursively go over every file in the directory
        for filename in os.listdir(self.directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.directory, filename)
                parser = WeatherDataParser(file_path)
                weather_data = parser.parse_weather_data()
                self.all_year_weather += weather_data

        return self.all_year_weather


class WeatherAnalyzer:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    # Returns highest temperature within given date range
    def get_highest_temperature(self):
        highest_temp = float('-inf')
        highest_temp_day = None
        for reading in self.weather_data:
            if reading.max_temp is not None and reading.max_temp > highest_temp:
                highest_temp = reading.max_temp
                highest_temp_day = reading.date
        return highest_temp, highest_temp_day

    # Returns lowest temperature within given date range
    def get_lowest_temperature(self):
        lowest_temp = float('inf')
        lowest_temp_day = None
        for reading in self.weather_data:
            if reading.min_temp is not None and reading.min_temp < lowest_temp:
                lowest_temp = reading.min_temp
                lowest_temp_day = reading.date
        return lowest_temp, lowest_temp_day

    # Returns most humid day within given date range
    def get_most_humid_day(self):
        max_humidity = 0
        max_humidity_day = None
        for reading in self.weather_data:
            if reading.max_humidity is not None and reading.max_humidity > max_humidity:
                max_humidity = reading.max_humidity
                max_humidity_day = reading.date
        return max_humidity, max_humidity_day

    # Returns average humidity level given date range
    def get_average_temperature_humidity(self):
        total_max_temp = 0
        total_min_temp = 0
        total_mean_humidity = 0
        count = 0
        # Read each day weather object and sum up them
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

    """Draw Single horizontal bar chart on the console for the highest and lowest temperature,
     on each day against given month
     """

    def draw_single_line(self, month_data):

        # Iterate over each day's data
        for reading in month_data:
            date = reading.date
            if reading.max_temp is not None:
                highest_temp = reading.max_temp
            if reading.min_temp is not None:
                lowest_temp = reading.min_temp

            # Draw highest & lowest temperature in single line on console
            red_marks = '\033[31m +' * int(highest_temp)
            blue_marks = '\033[34m +' * int(lowest_temp)

            print(f"{date} {blue_marks}\033[0m{red_marks} \033[0m {lowest_temp} - {highest_temp}C")

    def draw_two_lines(self, month_data):

        # Iterate over each day's data
        for reading in month_data:
            date = reading.date
            if reading.max_temp is not None:
                highest_temp = reading.max_temp
            if reading.min_temp is not None:
                lowest_temp = reading.min_temp

            # Draw highest temperature line on console
            red_marks = '\033[31m +' * int(highest_temp)
            print("Highest temperature")
            print(f"{date} {red_marks}\033[0m{highest_temp} C")

            # Draw lowest temperature line on console
            blue_marks = '\033[34m +' * int(lowest_temp)
            print("Lowest Temperature")
            print(f"{date} {blue_marks}\033[0m{lowest_temp} C")


class GetWeatherReports:
    GetWeatherData = GetWeatherData()
    all_year_weather = GetWeatherData.all_weather_data()

    def __init__(self, years, months):
        self.years = years
        self.months = months

    def get_yearly_report(self):
        for year in self.years:
            # Extract weather data for a given year (e.g., 2005)
            year_data = [reading for reading in self.all_year_weather if reading.date.startswith(year)]

            # Pass year's data and create a weather parsing object
            analyzer = WeatherAnalyzer(year_data)

            highest_temp, highest_temp_day = analyzer.get_highest_temperature()
            lowest_temp, lowest_temp_day = analyzer.get_lowest_temperature()
            max_humidity, most_humid_day = analyzer.get_most_humid_day()

            print(f"For the year {year}:")
            print(f"Highest Temperature: {highest_temp}C on {highest_temp_day}")
            print(f"Lowest Temperature: {lowest_temp}C on {lowest_temp_day}")
            print(f"Most Humid Day: {most_humid_day} with Humidity {max_humidity}%")

    def get_monthly_report(self):
        for month in self.months:
            # Extract weather data for a given month (e.g., June 2005)
            month_data = [reading for reading in self.all_year_weather if reading.date.startswith(month)]

            # Pass month's data and create a weather parsing object
            analyzer = WeatherAnalyzer(month_data)

            avg_max_temp, avg_min_temp, avg_mean_humidity = analyzer.get_average_temperature_humidity()

            print(f"\nFor the month of {month}:")
            print(f"Highest Average: {int(avg_max_temp)}C")
            print(f"Lowest Average: {int(avg_min_temp)}C")
            print(f"Average Mean Humidity: {int(avg_mean_humidity)}%")

    def draw_double_line_chart(self):
        for month in self.months:
            # Extract data for a given month (e.g., April 2004)
            month_data = [reading for reading in self.all_year_weather if reading.date.startswith(month)]
            analyzer = WeatherAnalyzer(month_data)

            print(month)
            # Passing a list of WeatherReading objects for a specific month
            analyzer.draw_two_lines(month_data)

    def draw_single_line_chart(self):
        for month in self.months:
            # Extract data for a given month (e.g., April 2004)
            month_data = [reading for reading in self.all_year_weather if reading.date.startswith(month)]
            analyzer = WeatherAnalyzer(month_data)

            print(month)
            # Passing a list of WeatherReading objects for a specific month
            analyzer.draw_single_line(month_data)


# years = ['2004', '2016']
# months = ['2004-8']

# years = [input("Enter the year: ")]
# months = [input("Enter the month (as a number): ")]

years = input("Enter the years (comma-separated): ").split(",")
months = input("Enter the months (comma-separated as numbers): ").split(",")

reports = GetWeatherReports(years, months)
reports.get_yearly_report()
reports.get_monthly_report()
reports.draw_double_line_chart()
reports.draw_single_line_chart()
