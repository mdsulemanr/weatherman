import requests
from bs4 import BeautifulSoup
import json


class CountryCrawler:
    def __init__(self, start_url, base_url):
        self.start_url = start_url
        self.base_url = base_url

    def fetch_page(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content, response.status_code
        else:
            return None, response.status_code

    def parse_country_page(self, url, content, status_code):
        soup = BeautifulSoup(content, "html.parser")

        country_info = {
            "name": None,
            "capital": None,
            "provinces": [],
            "Images": [],
            "lat_lang": [],
            "url": url,
            "response_code": status_code
        }

        # Country Name
        title_tag = soup.find('h1', id="firstHeading")
        if title_tag:
            country_info["name"] = title_tag.text

        # Infobox
        infobox = soup.find('table', class_='infobox')
        if infobox:
            self.extract_infobox_data(infobox, country_info)

        # Provinces
        self.extract_provinces(soup, country_info)

        return country_info

    def extract_infobox_data(self, infobox, country_info):
        # Capital
        for row in infobox.find_all('tr'):
            header = row.find('th')
            if header and ('Capital' in header.text or 'capital' in header.text):
                capital_link = row.find('td').find('a')
                if capital_link:
                    country_info["capital"] = capital_link.text.strip()
                    self.extract_lat_long(row, country_info)
                break

        # Images for Flag and State Emblem
        for img in infobox.find_all('img'):
            img_src = img.get('src')
            if img_src:
                if 'flag' in img_src or 'Flag' in img_src or 'emblem' in img_src or 'Emblem' in img_src:
                    full_img_url = 'https:' + img_src
                    country_info["Images"].append(full_img_url)

    def extract_lat_long(self, row, country_info):
        geo_tag = row.find_next('span', class_='geo-dec')
        if geo_tag:
            lat_long = geo_tag.text.strip()
            lat, long = lat_long.split(' ')
            country_info["lat_lang"] = [
                float(lat.replace('°', '').replace('N', '').replace('S', '-').strip()),
                float(long.replace('°', '').replace('E', '').replace('W', '-').strip())
            ]

    def extract_provinces(self, soup, country_info):
        provinces_header = soup.find(id='Administrative_divisions')
        if provinces_header:
            provinces_list = provinces_header.find_next('ul')
            if provinces_list:
                country_info["provinces"] = [li.text.strip() for li in provinces_list.find_all('li')]

        if not country_info["provinces"]:
            for header in soup.find_all(['h2', 'h3']):
                if header.span and ('Provinces' in header.span.text or 'Administrative divisions' in header.span.text):
                    provinces_list = header.find_next('ul')
                    if provinces_list:
                        country_info["provinces"] = [li.text.strip() for li in provinces_list.find_all('li')]
                    break

    def get_country_urls(self):
        content, status_code = self.fetch_page(self.start_url)
        if not content:
            return []

        soup = BeautifulSoup(content, "html.parser")
        country_urls = []

        # Extract all country URLs from the table
        for link in soup.select(".wikitable tbody tr td:nth-child(2) a"):
            url = link.get('href')
            if url and url.startswith('/wiki/') and not url.startswith('/wiki/File:'):
                full_url = self.base_url + url
                if full_url not in country_urls:
                    country_urls.append(full_url)

        return country_urls

    def crawl(self):
        country_urls = self.get_country_urls()
        all_countries_info = []

        for url in country_urls:
            content, status_code = self.fetch_page(url)
            if content:
                country_info = self.parse_country_page(url, content, status_code)
                all_countries_info.append(country_info)

        return all_countries_info


def main():
    start_url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area"
    base_url = "https://en.wikipedia.org"
    crawler = CountryCrawler(start_url, base_url)
    all_country_data = crawler.crawl()
    print(json.dumps(all_country_data, indent=4))


if __name__ == "__main__":
    main()
