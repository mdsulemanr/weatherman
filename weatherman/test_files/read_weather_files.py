import os
import csv


class WeatherReading:
    def __init__(self, date, max_temp, min_temp, mean_humidity):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.mean_humidity = mean_humidity


class WeatherAnalyzer:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def get_highest_temperature(self):
        return max((reading.max_temp, reading.date) for reading in self.weather_data if reading.max_temp)

    def get_lowest_temperature(self):
        return min((reading.min_temp, reading.date) for reading in self.weather_data if reading.min_temp)

    def get_most_humid_day(self):
        return max((reading.mean_humidity, reading.date) for reading in self.weather_data if reading.mean_humidity)

    def get_average_temperature_humidity(self):
        valid_readings = [reading for reading in self.weather_data if
                          reading.max_temp and reading.min_temp and reading.mean_humidity]
        if not valid_readings:
            return None, None, None
        avg_max_temp = sum(reading.max_temp for reading in valid_readings) / len(valid_readings)
        avg_min_temp = sum(reading.min_temp for reading in valid_readings) / len(valid_readings)
        avg_mean_humidity = sum(reading.mean_humidity for reading in valid_readings) / len(valid_readings)
        return avg_max_temp, avg_min_temp, avg_mean_humidity


def load_weather_data_from_file(file_path):
    weather_data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = row['PKT']
            max_temp = int(row['Max TemperatureC']) if row['Max TemperatureC'] else None
            min_temp = int(row['Min TemperatureC']) if row['Min TemperatureC'] else None
            mean_humidity = int(row['Mean Humidity']) if row['Mean Humidity'] else None
            reading = WeatherReading(date, max_temp, min_temp, mean_humidity)
            weather_data.append(reading)
    return weather_data


def draw_temperature_lines(month_data):
    # Sort the data by date
    sorted_data = sorted(month_data, key=lambda x: x.date)

    # Iterate over each day's data
    for reading in sorted_data:
        date = reading.date[-2:]
        highest_temp = reading.max_temp
        lowest_temp = reading.min_temp

        # Draw highest temperature line
        print("Highest temperature")
        print(date + ' ' + '+' * highest_temp, highest_temp, "C")

        # Draw lowest temperature line
        print("Lowest Temperature")
        print(date + ' ' + '+' * lowest_temp, lowest_temp, "C")


def main():
    # Directory containing weather data files
    directory = "weather_data"

    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            month_data = load_weather_data_from_file(file_path)

            # Example usage:
            analyzer = WeatherAnalyzer(month_data)
            highest_temp, highest_temp_day = analyzer.get_highest_temperature()
            lowest_temp, lowest_temp_day = analyzer.get_lowest_temperature()
            most_humid_day, max_humidity = analyzer.get_most_humid_day()
            avg_max_temp, avg_min_temp, avg_mean_humidity = analyzer.get_average_temperature_humidity()

            # Print the results for a given year
            print("For the year 2004:")
            print("(a) Highest Temperature:", highest_temp, "on", highest_temp_day)
            print("(b) Lowest Temperature:", lowest_temp, "on", lowest_temp_day)
            print("(c) Most Humid Day:", most_humid_day, "with Humidity", max_humidity)

            # Print the results for a given month
            print("\nFor the month of April:")
            print("(a) Average Highest Temperature:", avg_max_temp)
            print("(b) Average Lowest Temperature:", avg_min_temp)
            print("(c) Average Mean Humidity:", avg_mean_humidity)

            # Draw temperature lines for a given month
            draw_temperature_lines(month_data)


if __name__ == "__main__":
    main()
