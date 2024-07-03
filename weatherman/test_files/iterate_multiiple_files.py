import os


class WeatherDataParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse_weather_data(self):
        weather_data = []
        with open(self.file_path, 'r') as file:
            header = next(file).strip().split(',')
            for line in file:
                values = line.strip().split(',')
                if len(values) == len(header):
                    # Assuming all values except date are float or int, handle empty values appropriately
                    day_data = {
                        'Date': values[0],
                        'Max TemperatureC': values[1] if values[1] else None,
                        'Mean TemperatureC': values[2] if values[2] else None,
                        'Min TemperatureC': values[3] if values[3] else None,
                        'Dew PointC': values[4] if values[4] else None,
                        'MeanDew PointC': values[5] if values[5] else None,
                        'Min DewpointC': values[6] if values[6] else None,
                        'Max Humidity': values[7] if values[7] else None,
                        'Mean Humidity': values[8] if values[8] else None,
                        'Min Humidity': values[9] if values[9] else None,
                        'Max Sea Level PressurehPa': values[10] if values[10] else None,
                        'Mean Sea Level PressurehPa': values[11] if values[11] else None,
                        'Min Sea Level PressurehPa': values[12] if values[12] else None,
                        'Max VisibilityKm': values[13] if values[13] else None,
                        'Mean VisibilityKm': values[14] if values[14] else None,
                        'Min VisibilitykM': values[15] if values[15] else None,
                        'Max Wind SpeedKm/h': values[16] if values[16] else None,
                        'Mean Wind SpeedKm/h': values[17] if values[17] else None,
                        'Max Gust SpeedKm/h': values[18] if values[18] else None,
                        'Precipitationmm': values[19] if values[19] else None,
                        'CloudCover': values[20] if values[20] else None,
                        'Events': values[21] if values[21] else None,
                        'WindDirDegrees': values[22] if values[22] else None
                    }
                    weather_data.append(day_data)
        return weather_data


# Directory containing .txt files
directory = "weather_data"

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        parser = WeatherDataParser(file_path)
        weather_data = parser.parse_weather_data()
        print(weather_data)

        # Process weather data
        # analyzer = WeatherAnalyzer(weather_data)
        # analyzer.perform_calculations()
        # results = analyzer.get_results()
