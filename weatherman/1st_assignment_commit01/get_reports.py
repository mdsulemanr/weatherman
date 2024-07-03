import argparse
import os
from read_weather_data import WeatherDataParser
from generate_reports import GetYearlyReport
from generate_reports import GetMonthlyReports


# Use Command line arguments & pass values for creating single/multiple reports
def main():
    parser = argparse.ArgumentParser(description='Process weather data.')
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory path of the weather files')
    parser.add_argument('-a', '--monthly', type=str, help='Month to generate monthly report (e.g., 2004-8)')
    parser.add_argument('-b', '--doublechart', type=str, help='Month to generate double bar charts (e.g., 2004-8)')
    parser.add_argument('-c', '--singlechart', type=str, help='Month to generate single bar chart (e.g., 2004-8)')
    parser.add_argument('-e', '--yearly', type=str, help='Year to generate yearly report (e.g., 2004)')

    args = parser.parse_args()
    directory = args.directory
    all_year_weather = []

    # Recursively go over every file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            parser = WeatherDataParser(file_path)
            weather_data = parser.parse_weather_data()
            all_year_weather += weather_data

    # Generate yearly report
    if args.yearly:
        year = args.yearly
        reports = GetYearlyReport(year, all_year_weather)
        reports.get_yearly_report()

    # Generate monthly report
    if args.monthly:
        year_month = args.monthly
        reports = GetMonthlyReports(year_month, all_year_weather)
        reports.get_monthly_report()

    # Draw two bar horizontal chart
    if args.doublechart:
        year_month = args.doublechart
        reports = GetMonthlyReports(year_month, all_year_weather)
        reports.draw_multiline_chart()

    # Draw single bar horizontal chart
    if args.singlechart:
        year_month = args.singlechart
        reports = GetMonthlyReports(year_month, all_year_weather)
        reports.draw_single_line_chart()


if __name__ == "__main__":
    main()
