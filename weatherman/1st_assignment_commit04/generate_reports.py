from weather_analyzer import WeatherAnalyzer

RED_COLOR = '\033[31m'
BLUE_COLOR = '\033[34m'
RESET_COLOR = '\033[0m'


class GetWeatherReport:

    def __init__(self, dates, all_weather_data):
        self.dates = dates
        self.all_weather_data = all_weather_data

    def get_year_weather_data(self):
        year = self.dates
        year_weather_data = [data for month_data in self.all_weather_data.get(year).values() for data in month_data]
        return year, year_weather_data

    def consolidate_yearly_report(self):
        year, year_weather_data = self.get_year_weather_data()
        analyzer = WeatherAnalyzer(year_weather_data)

        highest_temp, highest_temp_day = analyzer.get_highest_temperature()
        lowest_temp, lowest_temp_day = analyzer.get_lowest_temperature()
        max_humidity, most_humid_day = analyzer.get_most_humid_day()

        return year, highest_temp, highest_temp_day, lowest_temp, lowest_temp_day, max_humidity, most_humid_day

    def get_yearly_report(self):
        year, highest_temp, highest_temp_day, lowest_temp, lowest_temp_day, max_humidity, most_humid_day \
            = self.consolidate_yearly_report()

        print(f"For the year {year}:")
        print(f"Highest Temperature: {int(highest_temp)}C on {highest_temp_day}")
        print(f"Lowest Temperature: {int(lowest_temp)}C on {lowest_temp_day}")
        print(f"Most Humid Day: {most_humid_day} with Humidity {int(max_humidity)}%")

    def get_month_weather_data(self):
        year_month = self.dates
        year, month = self.dates.split('-')

        one_month_data = [data for month_data in self.all_weather_data.get(year).values() for data in month_data
                          if data["date"].startswith(year_month)]
        return year_month, one_month_data

    def consolidate_monthly_report(self):
        year_month, one_month_data = self.get_month_weather_data()
        analyzer = WeatherAnalyzer(one_month_data)

        avg_max_temp, avg_min_temp, avg_mean_humidity = analyzer.get_average_temperature_humidity()
        return year_month, avg_max_temp, avg_min_temp, avg_mean_humidity

    def get_monthly_report(self):
        month, avg_max_temp, avg_min_temp, avg_mean_humidity = self.consolidate_monthly_report()

        print(f"\nFor the month of {month}:")
        print(f"Highest Average: {int(avg_max_temp)}C")
        print(f"Lowest Average: {int(avg_min_temp)}C")
        print(f"Average Mean Humidity: {int(avg_mean_humidity)}%")

    def display_multi_lines(self, date, highest_temp, lowest_temp):

        red_marks = f"{RED_COLOR} +" * int(highest_temp)
        print("Highest temperature")
        print(f"{date} {red_marks}{RESET_COLOR} {highest_temp} C")

        blue_marks = f"{BLUE_COLOR} +" * int(lowest_temp)
        print("Lowest Temperature")
        print(f"{date} {blue_marks}{RESET_COLOR} {lowest_temp} C")

    def draw_multiline_chart(self):
        year, month = self.dates.split('-')
        month_data = self.all_weather_data.get(year).get(month)

        for reading in month_data:
            date = reading['date']
            if reading['max_temp']:
                highest_temp = reading['max_temp']
            if reading['min_temp']:
                lowest_temp = reading['min_temp']

            self.display_multi_lines(date, highest_temp, lowest_temp)

    def display_single_line(self, date, highest_temp, lowest_temp):

        red_marks = f"{RED_COLOR} +" * int(highest_temp)
        blue_marks = f"{BLUE_COLOR} +" * int(lowest_temp)

        print(f"{date} {blue_marks}{RESET_COLOR}{red_marks}{RESET_COLOR} {lowest_temp}C - {highest_temp}C")

    def draw_single_line_chart(self):
        year, month = self.dates.split('-')
        month_data = self.all_weather_data.get(year).get(month)

        for reading in month_data:
            date = reading['date']
            if reading['max_temp']:
                highest_temp = reading['max_temp']
            if reading['min_temp']:
                lowest_temp = reading['min_temp']

            self.display_single_line(date, highest_temp, lowest_temp)
