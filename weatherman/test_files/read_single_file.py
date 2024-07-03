import os


class WeatherData:
    file_path = os.getcwd() + "/Data/Murree_weather_2004_Aug.txt"

    def read_txt_file(self):
        data = []
        with open(self.file_path, 'r') as file:
            # Skip the header line
            next(file)
            for line in file:
                values = line.strip().split(',')
                # Create a dictionary for each day's data
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
                data.append(day_data)
        return data


file_data = WeatherData().read_txt_file()
print(file_data)
