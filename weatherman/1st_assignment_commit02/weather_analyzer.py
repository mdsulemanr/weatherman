from statistics import mean


class WeatherAnalyzer:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def get_highest_temperature(self):
        highest_temp_reading = max(self.weather_data, key=lambda reading: (
            reading.max_temp if reading.max_temp is not None else float('-inf')))

        return highest_temp_reading.max_temp, highest_temp_reading.date

    def get_lowest_temperature(self):
        lowest_temp_reading = min(self.weather_data, key=lambda reading: (
            reading.min_temp if reading.min_temp is not None else float('inf')))

        return lowest_temp_reading.min_temp, lowest_temp_reading.date

    def get_most_humid_day(self):
        most_humid_reading = max(self.weather_data, key=lambda reading: (
            reading.mean_humidity if reading.mean_humidity is not None else float('-inf')))

        return most_humid_reading.mean_humidity, most_humid_reading.date

    def get_average_temperature_humidity(self):
        max_temps = [reading.max_temp for reading in self.weather_data if reading.max_temp is not None]
        min_temps = [reading.min_temp for reading in self.weather_data if reading.min_temp is not None]
        mean_humidity = [reading.mean_humidity for reading in self.weather_data if reading.mean_humidity is not None]

        if not max_temps or not min_temps or not mean_humidity:
            return None, None, None

        avg_max_temp = mean(max_temps)
        avg_min_temp = mean(min_temps)
        avg_mean_humidity = mean(mean_humidity)

        return avg_max_temp, avg_min_temp, avg_mean_humidity

    def display_multi_lines(self, date, highest_temp, lowest_temp):
        plane_text = '\033[0m'
        red_marks = '\033[31m +' * int(highest_temp)
        print("Highest temperature")
        print(f"{date} {red_marks}{plane_text} {highest_temp} C")

        blue_marks = '\033[34m +' * int(lowest_temp)
        print("Lowest Temperature")
        print(f"{date} {blue_marks}{plane_text} {lowest_temp} C")

    def draw_two_lines(self, month_data):

        for reading in month_data:
            date = reading.date
            if reading.max_temp is not None:
                highest_temp = reading.max_temp
            if reading.min_temp is not None:
                lowest_temp = reading.min_temp

            self.display_multi_lines(date, highest_temp, lowest_temp)

    def display_single_line(self, date, highest_temp, lowest_temp):
        red_marks = '\033[31m +' * int(highest_temp)
        blue_marks = '\033[34m +' * int(lowest_temp)
        plane_text = '\033[0m'

        print(f"{date} {blue_marks}{plane_text}{red_marks}{plane_text} {lowest_temp} - {highest_temp}C")

    def draw_single_line(self, month_data):

        for reading in month_data:
            date = reading.date
            if reading.max_temp is not None:
                highest_temp = reading.max_temp
            if reading.min_temp is not None:
                lowest_temp = reading.min_temp

            self.display_single_line(date, highest_temp, lowest_temp)
