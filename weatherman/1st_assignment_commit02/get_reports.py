import argparse
from read_weather_data import WeatherDataParser
from generate_reports import GetYearlyReport


def main():
    weather_data = WeatherDataParser()

    parser = argparse.ArgumentParser(description='Process weather data.')
    parser.add_argument('directory', type=str, help='Directory path of the weather files')
    parser.add_argument('-a', '--monthly', type=str, help='Month to generate monthly report (e.g., 2004-8)')
    parser.add_argument('-b', '--doublechart', type=str, help='Month to generate double bar charts (e.g., 2004-8)')
    parser.add_argument('-c', '--singlechart', type=str, help='Month to generate single bar chart (e.g., 2004-8)')
    parser.add_argument('-e', '--yearly', type=str, help='Year to generate yearly report (e.g., 2004)')

    args = parser.parse_args()
    all_year_weather = weather_data.get_weather_data(args.directory)

    if args.yearly:
        year = args.yearly
        reports = GetYearlyReport(year, all_year_weather)
        reports.get_yearly_report()

    if args.monthly:
        year_month = args.monthly
        reports = GetYearlyReport(year_month, all_year_weather)
        reports.get_monthly_report()

    if args.doublechart:
        year_month = args.doublechart
        reports = GetYearlyReport(year_month, all_year_weather)
        reports.draw_multiline_chart()

    if args.singlechart:
        year_month = args.singlechart
        reports = GetYearlyReport(year_month, all_year_weather)
        reports.draw_single_line_chart()


if __name__ == "__main__":
    main()
