from collections import defaultdict


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
        humidity_counts = defaultdict(int)
        for reading in self.weather_data:
            if reading.mean_humidity is not None:
                humidity_counts[reading.mean_humidity] += 1
        most_humid_day = max(humidity_counts, key=humidity_counts.get)
        return most_humid_day, humidity_counts[most_humid_day]

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


class WeatherReports:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def generate_yearly_report(self, year):
        year_data = [reading for reading in self.analyzer.weather_data if reading.date.startswith(year)]
        highest_temp, highest_temp_day = self.analyzer.get_highest_temperature()
        lowest_temp, lowest_temp_day = self.analyzer.get_lowest_temperature()
        most_humid_day, max_humidity = self.analyzer.get_most_humid_day()

        yearly_report = f"For the year {year}:\n"
        yearly_report += "(a) Highest Temperature: {} on {}\n".format(highest_temp, highest_temp_day)
        yearly_report += "(b) Lowest Temperature: {} on {}\n".format(lowest_temp, lowest_temp_day)
        yearly_report += "(c) Most Humid Day: {} with Humidity {}\n".format(most_humid_day, max_humidity)

        return yearly_report

    def generate_monthly_report(self, month):
        month_data = [reading for reading in self.analyzer.weather_data if reading.date.startswith(month)]
        avg_max_temp, avg_min_temp, avg_mean_humidity = self.analyzer.get_average_temperature_humidity()

        monthly_report = f"For the month of {month}:\n"
        monthly_report += "(a) Average Highest Temperature: {}\n".format(avg_max_temp)
        monthly_report += "(b) Average Lowest Temperature: {}\n".format(avg_min_temp)
        monthly_report += "(c) Average Mean Humidity: {}\n".format(avg_mean_humidity)

        return monthly_report


# Example usage:
# Assuming weather_data is a list of WeatherReading objects

weather_data = [WeatherReading("2004-12-01", 12, 3, 20),
                WeatherReading("2004-12-02", 14, 5, 30),
                WeatherReading("2004-12-03", 10, 2, 25),
                WeatherReading("2004-04-01", 20, 10, 40),
                WeatherReading("2004-04-02", 22, 12, 45)]

analyzer = WeatherAnalyzer(weather_data)
reports = WeatherReports(analyzer)

# Generate yearly report for 2004
yearly_report = reports.generate_yearly_report("2004")
print(yearly_report)

# Generate monthly report for April
monthly_report = reports.generate_monthly_report("2004-04")
print(monthly_report)
