import csv
import os


class WeatherParser:
    weather_data = {}

    def add_reading(self):

        director_path = os.getcwd() + "/Data"
        file_names = os.listdir(director_path)
        for file_name in file_names:
            if file_name.endswith(".txt"):
                file_path = os.path.join(director_path, file_name)
                with open(file_path, 'r') as file:
                    file_reader = csv.DictReader(file)
                    headers = file_reader.fieldnames
                    pkt = headers[0]

                    for row in file_reader:
                        date = row[pkt]
                        year, month, day = date.split('-')
                        if year not in self.weather_data:
                            self.weather_data[year] = {}
                        if month not in self.weather_data[year]:
                            self.weather_data[year][month] = []

                        self.weather_data[year][month].append(
                            {
                                "date": date,
                                "max_temp": row['Max TemperatureC'],
                                "min_temp": row['Min TemperatureC']
                            }
                        )

        return self.weather_data

    def get_data(self):
        self.weather_data = self.add_reading()
        # month_data = []
        # for reading in self.weather_data.get("2004", {}).values():
        #     print(reading)
        #     month_data.append(reading)
        # print(month_data)

        year_weather_data = [month_data for month_data in self.weather_data.get("2011").values()]
        for reading in year_weather_data:
            print(reading)


parser = WeatherParser()
# parser.add_reading()
parser.get_data()
