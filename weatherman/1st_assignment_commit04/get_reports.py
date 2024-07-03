import argparse
from datetime import datetime

from read_weather_data import WeatherDataParser
from generate_reports import GetWeatherReport


def validate_year(year):
    year_start = 2004
    year_end = datetime.now().year

    if not (year.isdigit() and year_start <= int(year) <= year_end):
        raise argparse.ArgumentTypeError(f"Invalid year: {year}. Year must be between {year_start} and {year_end}.")
    return year


def validate_month(month):
    month_start = 1
    month_end = 12
    if not (month.isdigit() and month_start <= int(month) <= month_end):
        raise argparse.ArgumentTypeError(f"Invalid month: {month}."
                                         f" Month must be between {month_start} and {month_end}.")
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
