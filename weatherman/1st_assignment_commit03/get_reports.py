import argparse

from read_weather_data import WeatherDataParser
from generate_reports import GetWeatherReport


def validate_year(year):
    if not (year.isdigit() and 2004 <= int(year) <= 2016):
        raise argparse.ArgumentTypeError(f"Invalid year: {year}. Year must be between 2004 and 2016.")
    return year


def validate_month(month):
    if not (month.isdigit() and 1 <= int(month) <= 12):
        raise argparse.ArgumentTypeError(f"Invalid month: {month}. Month must be between 1 and 12.")
    return month


def validate_year_month(year_month):
    try:
        year, month = year_month.split('-')
        validate_year(year)
        validate_month(month)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid year-month format: {year_month}. Format must be YYYY-MM.")
    return year_month


def main():
    weather_data_parser = WeatherDataParser()

    parser = argparse.ArgumentParser(description='Process weather data.')
    parser.add_argument('directory', type=str, help='Directory path of the weather files')
    parser.add_argument('-a', '--monthly', type=validate_year_month,
                        help='Month to generate monthly report (e.g., 2004-8)')
    parser.add_argument('-b', '--doublechart', type=validate_year_month,
                        help='Month to generate double bar charts (e.g., 2004-8)')
    parser.add_argument('-c', '--singlechart', type=validate_year_month,
                        help='Month to generate single bar chart (e.g., 2004-8)')
    parser.add_argument('-e', '--yearly', type=validate_year, help='Year to generate yearly report (e.g., 2004)')

    args = parser.parse_args()
    all_weather_data = weather_data_parser.parse_txt_files(args.directory)

    if args.yearly:
        year = args.yearly
        reports = GetWeatherReport(year, all_weather_data)
        reports.get_yearly_report()

    if args.monthly:
        year_month = args.monthly
        reports = GetWeatherReport(year_month, all_weather_data)
        reports.get_monthly_report()

    if args.doublechart:
        year_month = args.doublechart
        reports = GetWeatherReport(year_month, all_weather_data)
        reports.draw_multiline_chart()

    if args.singlechart:
        year_month = args.singlechart
        reports = GetWeatherReport(year_month, all_weather_data)
        reports.draw_single_line_chart()


if __name__ == "__main__":
    main()
