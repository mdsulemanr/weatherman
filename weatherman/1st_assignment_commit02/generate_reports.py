from weather_analyzer import WeatherAnalyzer


class GetYearlyReport:

    def __init__(self, weather_data, all_year_weather):
        self.weather_data = weather_data
        self.all_year_weather = all_year_weather

    def get_yearly_report(self):

        one_year_data = [reading for reading in self.all_year_weather if reading.date.startswith(self.weather_data)]

        analyzer = WeatherAnalyzer(one_year_data)

        highest_temp, highest_temp_day = analyzer.get_highest_temperature()
        lowest_temp, lowest_temp_day = analyzer.get_lowest_temperature()
        max_humidity, most_humid_day = analyzer.get_most_humid_day()

        print(f"For the year {self.weather_data}:")
        print(f"Highest Temperature: {highest_temp}C on {highest_temp_day}")
        print(f"Lowest Temperature: {lowest_temp}C on {lowest_temp_day}")
        print(f"Most Humid Day: {most_humid_day} with Humidity {max_humidity}%")

    def get_monthly_report(self):

        month_data = [reading for reading in self.all_year_weather if reading.date.startswith(self.weather_data)]

        analyzer = WeatherAnalyzer(month_data)

        avg_max_temp, avg_min_temp, avg_mean_humidity = analyzer.get_average_temperature_humidity()

        print(f"\nFor the month of {self.weather_data}:")
        print(f"Highest Average: {int(avg_max_temp)}C")
        print(f"Lowest Average: {int(avg_min_temp)}C")
        print(f"Average Mean Humidity: {int(avg_mean_humidity)}%")

    def draw_multiline_chart(self):

        month_data = [reading for reading in self.all_year_weather if reading.date.startswith(self.weather_data)]
        analyzer = WeatherAnalyzer(month_data)

        analyzer.draw_two_lines(month_data)

    def draw_single_line_chart(self):

        month_data = [reading for reading in self.all_year_weather if reading.date.startswith(self.weather_data)]
        analyzer = WeatherAnalyzer(month_data)

        analyzer.draw_single_line(month_data)
