import os


def read_file():

    file_path = os.getcwd() + "/Data/Murree_weather_2004_Aug.txt"

    weather_conditions = ["PKT","Max TemperatureC","Mean TemperatureC","Min TemperatureC",
                          "Dew PointC","MeanDew PointC","Min DewpointC","Max Humidity",
                          "Mean Humidity", "Min Humidity", "Max Sea Level PressurehPa",
                          "Mean Sea Level PressurehPa", "Min Sea Level PressurehPa",
                          "Max VisibilityKm", "Mean VisibilityKm", "Min VisibilitykM",
                          "Max Wind SpeedKm/h", "Mean Wind SpeedKm/h", "Max Gust SpeedKm/h",
                          "Precipitationmm", "CloudCover", "Events","WindDirDegrees"]
    weather_reading = {}

    file = open(file_path, "r")
    for i in range(32):
        str_line = file.readline()
        list_line = str_line.split("\n")
        for reading in range (len((list_line))):
            print(reading)

    file.close()


read_file()
