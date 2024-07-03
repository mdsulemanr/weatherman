import os


def parse_weather_data(file_path):
    weather_data = {}
    with open(file_path, 'r') as file:
        next(file)  # skip header
        for line in file:
            if line.strip():  # skip empty lines
                parts = line.strip().split(',')
                date = parts[0]
                weather_info = {
                    "Max TemperatureC": int(parts[1]) if parts[1] else None,
                    "Min TemperatureC": int(parts[3]) if parts[3] else None,
                    "Max Humidity": int(parts[7]),
                    "Mean Humidity": int(parts[8]),
                    "Min Humidity": int(parts[9])
                }
                weather_data[date] = weather_info
    return weather_data


def get_yearly_stats(weather_data, year):
    yearly_data = {date: data for date, data in weather_data.items() if date.startswith(year)}
    highest_temp_day = max(yearly_data, key=lambda x: yearly_data[x]["Max TemperatureC"])
    lowest_temp_day = min(yearly_data, key=lambda x: yearly_data[x]["Min TemperatureC"])
    most_humid_day = max(yearly_data, key=lambda x: yearly_data[x]["Max Humidity"])
    return {
        "Highest Temperature": (highest_temp_day, yearly_data[highest_temp_day]["Max TemperatureC"]),
        "Lowest Temperature": (lowest_temp_day, yearly_data[lowest_temp_day]["Min TemperatureC"]),
        "Most Humid Day": (most_humid_day, yearly_data[most_humid_day]["Max Humidity"])
    }


def get_monthly_stats(weather_data, year, month):
    monthly_data = {date: data for date, data in weather_data.items() if date.startswith(f"{year}-{month:02d}")}
    avg_max_temp = sum(data["Max TemperatureC"] for data in monthly_data.values() if data["Max TemperatureC"]) / len(
        monthly_data)
    avg_min_temp = sum(data["Min TemperatureC"] for data in monthly_data.values() if data["Min TemperatureC"]) / len(
        monthly_data)
    avg_mean_humidity = sum(data["Mean Humidity"] for data in monthly_data.values()) / len(monthly_data)
    return {
        "Average Highest Temperature": avg_max_temp,
        "Average Lowest Temperature": avg_min_temp,
        "Average Mean Humidity": avg_mean_humidity
    }


def draw_temperature_lines(weather_data, year, month):
    monthly_data = {date: data for date, data in weather_data.items() if date.startswith(f"{year}-{month:02d}")}
    for date, data in monthly_data.items():
        print(f"{date} Highest temperature")
        print("+" * data["Max TemperatureC"], data["Max TemperatureC"])
        print(f"{date} Lowest Temperature")
        print("+" * data["Min TemperatureC"], data["Min TemperatureC"])


def main():
    directory = "path_to_directory_containing_txt_files"
    weather_data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            weather_data.update(parse_weather_data(file_path))

    years = input("Enter the years (comma-separated): ").split(",")
    months = input("Enter the months (comma-separated as numbers): ").split(",")

    for year in years:
        for month in months:
            yearly_stats = get_yearly_stats(weather_data, year)
            monthly_stats = get_monthly_stats(weather_data, year, month)

            print(f"\nYearly Stats for {year}:")
            for key, value in yearly_stats.items():
                print(f"{key}: {value[1]} on {value[0]}")

            print(f"\nMonthly Stats for {year}/{month}:")
            for key, value in monthly_stats.items():
                print(f"{key}: {value}")

            print(f"\nTemperature Lines for {year}/{month}:")
            draw_temperature_lines(weather_data, year, month)
            print("=" * 50)


if __name__ == "__main__":
    main()
