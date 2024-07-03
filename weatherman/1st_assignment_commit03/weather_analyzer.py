import statistics
from operator import itemgetter
from statistics import mean


class WeatherAnalyzer:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def get_highest_temperature(self):
        max_temp_data = [(date, data['max_temp']) for date, data in self.weather_data.items()
                         if data['max_temp'] is not None]
        if not max_temp_data:
            return None, None
        highest_temp_day = max(max_temp_data, key=itemgetter(1))
        return highest_temp_day[1], highest_temp_day[0]

    def get_lowest_temperature(self):
        min_temp_data = [(date, data['min_temp']) for date, data in self.weather_data.items()
                         if data['min_temp'] is not None]
        if not min_temp_data:
            return None, None
        lowest_temp_day = min(min_temp_data, key=itemgetter(1))
        return lowest_temp_day[1], lowest_temp_day[0]

    def get_most_humid_day(self):
        mean_humidity_data = [(date, data['mean_humidity']) for date, data in self.weather_data.items()
                              if data['mean_humidity'] is not None]
        if not mean_humidity_data:
            return None, None
        most_humid_day = max(mean_humidity_data, key=itemgetter(1))
        return most_humid_day[0], most_humid_day[1]

    def get_average_temperature_humidity(self):
        max_temps = [data['max_temp'] for data in self.weather_data.values() if data['max_temp'] is not None]
        min_temps = [data['min_temp'] for data in self.weather_data.values() if data['min_temp'] is not None]
        mean_humidity = [data['mean_humidity'] for data in self.weather_data.values() if
                         data['mean_humidity'] is not None]

        avg_max_temp = statistics.mean(max_temps) if max_temps else None
        avg_min_temp = statistics.mean(min_temps) if min_temps else None
        avg_mean_humidity = statistics.mean(mean_humidity) if mean_humidity else None

        return avg_max_temp, avg_min_temp, avg_mean_humidity
