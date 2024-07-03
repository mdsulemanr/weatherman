import sys

"""
These arguments are stored in a list named 'argv' inside sys module.
You can use these passed arguments using indexing like sys.argv[0] (for first arguments).

Use:- Passing file name as command line arguments instead of hard coding in script. such as:
Passing database name.
Remote ip to which we want to connect.
"""

Murree_weather_2004_Aug = sys.argv[1]
# full_path = "/Users/muhammadsalmanrafi/PycharmProjects/weatherman/Data/Murree_weather_2004_Aug.txt"

with open(Murree_weather_2004_Aug, 'r') as f:
    content = f.read()
print(content)
