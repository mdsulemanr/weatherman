import argparse
from _datetime import datetime

from read_weather_data import WeatherDataParser
from generate_reports import GetWeatherReport


def validate_year(year):
    min_year = 2004
    max_year = datetime.now().year
    if not (year.isdigit() and min_year <= int(year) <= max_year):
        raise argparse.ArgumentTypeError(f"Invalid year: {year}. Year must be between {min_year} and {max_year}.")
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
