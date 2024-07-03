import requests
from bs4 import BeautifulSoup
import multiprocessing
import re
from urllib.parse import urljoin

BASE_URL = "https://en.wikipedia.org"
START_URL = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area"


# Function to get country URLs
def get_country_urls(start_url):
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    country_links = []
    for a_tag in soup.select('table.wikitable tbody tr td a'):
        href = a_tag.get('href')
        if href and href.startswith('/wiki/'):
            country_links.append(urljoin(BASE_URL, href))
    return list(set(country_links))  # remove duplicates


# Function to extract country details
def extract_country_details(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')

        # Country name
        country_name = soup.find('h1', id="firstHeading").text

        # Capital
        capital = None
        capital_match = re.search(r'Capital</th>\n<td.*?><a.*?>(.*?)</a>', response.text)
        if capital_match:
            capital = capital_match.group(1)

        # Provinces
        provinces = []
        provinces_header = soup.find('span', {'id': 'Administrative_divisions'})
        if provinces_header:
            provinces_list = provinces_header.find_next('ul')
            if provinces_list:
                provinces = [li.text for li in provinces_list.find_all('li')]

        # Images for Flag and State Emblem
        images = []
        for img in soup.select('.infobox img'):
            img_url = img.get('src')
            if img_url:
                images.append(urljoin(BASE_URL, img_url))

        # Latitude and Longitude of Capital
        lat_lon = None
        geo = soup.find('span', {'class': 'geo'})
        if geo:
            lat_lon = geo.text

        # Response code
        response_code = response.status_code

        # Collecting data
        country_data = {
            'Country Name': country_name,
            'Capital': capital,
            'Provinces': provinces,
            'Images': images,
            'Latitude and Longitude': lat_lon,
            'URL': url,
            'Response code': response_code
        }

        return country_data

    except Exception as e:
        print(f"Failed to process URL {url}: {e}")
        return None


# Function to process URL list with multiprocessing
def process_urls(urls):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(extract_country_details, urls)
    return [result for result in results if result is not None]


if __name__ == '__main__':
    country_urls = get_country_urls(START_URL)
    country_details = process_urls(country_urls)
    for country in country_details:
        print(country)
