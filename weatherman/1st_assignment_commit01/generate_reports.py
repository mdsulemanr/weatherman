from weather_analyzer import WeatherAnalyzer


class GetYearlyReport:

    def __init__(self, year, all_year_weather):
        self.year = year
        self.all_year_weather = all_year_weather

    def get_yearly_report(self):
        # for year in self.years:
        # Extract weather data for a given year (e.g., 2005)
        year_data = [reading for reading in self.all_year_weather if reading.date.startswith(self.year)]

        # Pass year's data and create a weather parsing object
        analyzer = WeatherAnalyzer(year_data)

        highest_temp, highest_temp_day = analyzer.get_highest_temperature()
        lowest_temp, lowest_temp_day = analyzer.get_lowest_temperature()
        max_humidity, most_humid_day = analyzer.get_most_humid_day()

        print(f"For the year {self.year}:")
        print(f"Highest Temperature: {highest_temp}C on {highest_temp_day}")
        print(f"Lowest Temperature: {lowest_temp}C on {lowest_temp_day}")
        print(f"Most Humid Day: {most_humid_day} with Humidity {max_humidity}%")


class GetMonthlyReports:

    def __init__(self, month, all_year_weather):
        self.month = month
        self.all_year_weather = all_year_weather

    def get_monthly_report(self):
        # Extract weather data for a given month (e.g., June 2005)
        month_data = [reading for reading in self.all_year_weather if reading.date.startswith(self.month)]

        # Pass month's data and create a weather parsing object
        analyzer = WeatherAnalyzer(month_data)

        avg_max_temp, avg_min_temp, avg_mean_humidity = analyzer.get_average_temperature_humidity()

        print(f"\nFor the month of {self.month}:")
        print(f"Highest Average: {int(avg_max_temp)}C")
        print(f"Lowest Average: {int(avg_min_temp)}C")
        print(f"Average Mean Humidity: {int(avg_mean_humidity)}%")

    def draw_multiline_chart(self):
        # Extract data for a given month (e.g., April 2004)
        month_data = [reading for reading in self.all_year_weather if reading.date.startswith(self.month)]
        analyzer = WeatherAnalyzer(month_data)

        # Passing a list of WeatherReading objects for a specific month
        analyzer.draw_lines(month_data)

    def draw_single_line_chart(self):
        # Extract data for a given month (e.g., April 2004)
        month_data = [reading for reading in self.all_year_weather if reading.date.startswith(self.month)]
        analyzer = WeatherAnalyzer(month_data)

        # Passing a list of WeatherReading objects for a specific month
        analyzer.draw_single_line(month_data)
