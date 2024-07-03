import argparse
import os


# Use Command line arguments & pass values for creating single/multiple reports
def main():
    parser = argparse.ArgumentParser(description='add')
    parser.add_argument('x', type=float, help='Enter first value')
    parser.add_argument('y', type=float, help='Enter second value')
    # parser.add_argument('-m', '--multiply', type=str, help='Month to generate double bar charts (e.g., 2004-8)')
    # parser.add_argument('-d', '--division', type=str, help='Month to generate single bar chart (e.g., 2004-8)')

    args = parser.parse_args()
    print(args.x + args.y)


if __name__ == "__main__":
    main()
