

class WeatherAnalyzer:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def get_highest_temperature(self):
        highest_temp = float('-inf')
        highest_temp_day = None

        for data in self.weather_data:
            if data['max_temp']:
                if data['max_temp'] > highest_temp:
                    highest_temp = data['max_temp']
                    highest_temp_day = data['date']

        return highest_temp, highest_temp_day

    def get_lowest_temperature(self):
        lowest_temp = float('inf')
        lowest_temp_day = None

        for data in self.weather_data:
            if data['min_temp'] and data['min_temp'] < lowest_temp:
                lowest_temp = data['min_temp']
                lowest_temp_day = data['date']

        return lowest_temp, lowest_temp_day

    def get_most_humid_day(self):
        highest_humidity = float("-inf")
        most_humid_day = None

        for data in self.weather_data:
            if data['mean_humidity'] and data['mean_humidity'] > highest_humidity:
                highest_humidity = data['mean_humidity']
                most_humid_day = data['date']

        return highest_humidity, most_humid_day

    def get_average_temperature_humidity(self):
        max_temps = [data['max_temp'] for data in self.weather_data if data['max_temp']]
        min_temps = [data['min_temp'] for data in self.weather_data if data['min_temp']]
        mean_humidity = [data['mean_humidity'] for data in self.weather_data if data['mean_humidity']]

        avg_max_temp = sum(max_temps)/len(max_temps) if max_temps else None
        avg_min_temp = sum(min_temps)/len(min_temps) if min_temps else None
        avg_mean_humidity = sum(mean_humidity)/len(mean_humidity) if mean_humidity else None

        return avg_max_temp, avg_min_temp, avg_mean_humidity
