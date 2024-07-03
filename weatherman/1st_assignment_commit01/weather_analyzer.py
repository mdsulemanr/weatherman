
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

    """Draw two horizontal bar charts on the console for the highest and lowest temperature,
     on each day against given month
     """
    def display_multi_lines(self, date, highest_temp, lowest_temp):
        # Draw highest temperature line on console
        plane_text = '\033[0m'
        red_marks = '\033[31m +' * int(highest_temp)
        print("Highest temperature")
        print(f"{date} {red_marks}{plane_text} {highest_temp} C")

        # Draw lowest temperature line on console
        blue_marks = '\033[34m +' * int(lowest_temp)
        print("Lowest Temperature")
        print(f"{date} {blue_marks}{plane_text} {lowest_temp} C")

    def draw_lines(self, month_data):
        highest_temp = float('-inf')
        lowest_temp = float('inf')

        # Iterate over each day's data
        for reading in month_data:
            date = reading.date
            if reading.max_temp is not None:
                highest_temp = reading.max_temp
            if reading.min_temp is not None:
                lowest_temp = reading.min_temp

            self.display_multi_lines(date, highest_temp, lowest_temp)

            # Draw highest temperature line on console
            # plane_text = '\033[0m'
            # red_marks = '\033[31m +' * int(highest_temp)
            # print("Highest temperature")
            # print(f"{date} {red_marks}{plane_text} {highest_temp} C")
            #
            # # Draw lowest temperature line on console
            # blue_marks = '\033[34m +' * int(lowest_temp)
            # print("Lowest Temperature")
            # print(f"{date} {blue_marks}{plane_text} {lowest_temp} C")

    def display_single_line(self, date, highest_temp, lowest_temp):
        red_marks = '\033[31m +' * int(highest_temp)
        blue_marks = '\033[34m +' * int(lowest_temp)
        plane_text = '\033[0m'

        print(f"{date} {blue_marks}{plane_text}{red_marks}{plane_text} {lowest_temp} - {highest_temp}C")

    """Draw Single horizontal bar chart on the console for the highest and lowest temperature,
     on each day against given month
     """
    def draw_single_line(self, month_data):
        highest_temp = float('-inf')
        lowest_temp = float('inf')

        # Iterate over each day's data
        for reading in month_data:
            date = reading.date
            if reading.max_temp is not None:
                highest_temp = reading.max_temp
            if reading.min_temp is not None:
                lowest_temp = reading.min_temp

            self.display_single_line(date, highest_temp, lowest_temp)
            # Draw highest & lowest temperature in single line on console
            # red_marks = '\033[31m +' * int(highest_temp)
            # blue_marks = '\033[34m +' * int(lowest_temp)
            # plane_text = '\033[0m'
            #
            # print(f"{date} {blue_marks}{plane_text}{red_marks}{plane_text} {lowest_temp} - {highest_temp}C")
