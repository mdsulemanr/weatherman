import requests
from bs4 import BeautifulSoup
import json

START_URL = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area"
BASE_URL = "https://en.wikipedia.org"


class CountryInfo:

    def __init__(self):
        self.soup = None

    def fetch_page(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content, response.status_code
        else:
            return None, response.status_code

    def get_country_urls(self):
        response_content, status_code = self.fetch_page(START_URL)
        soup = BeautifulSoup(response_content, "html.parser")
        country_urls = []

        for link in soup.select(".wikitable tbody tr td a"):
            url = link.get('href')
            if url and url.startswith('/wiki/') and not url.startswith('/wiki/File:'):
                full_url = BASE_URL + url
                if full_url not in country_urls:
                    country_urls.append(full_url)

        return country_urls

    def parse_country_page(self, url):
        response_content, status_code = self.fetch_page(url)
        if status_code != 200:
            return None

        soup = BeautifulSoup(response_content, "html.parser")
        self.soup = soup

        capital_name, lat_lang, images = self.country_details()
        country_info = {
            "name": self.country_name(),
            "capital": capital_name,
            "provinces": self.province_names(),
            "images": images,
            "lat_lang": lat_lang,
            "url": url,
            "response_code": status_code
        }
        return country_info

    def country_name(self):
        country_name = self.soup.find('h1', id="firstHeading")
        return country_name.text if country_name else None

    def country_details(self):
        capital_name = None
        lat_lang = None
        images = []

        infobox = self.soup.find('table', class_='infobox')
        if infobox:
            for row in infobox.find_all('tr'):
                header = row.find('th', class_='infobox-label')
                if header and 'Capital' in header.text:
                    capital_link = row.find('td', class_='infobox-data').find('a')
                    if capital_link:
                        capital_name = capital_link.text.strip()

                        geo_tag = row.find_next('span', class_='geo')
                        if geo_tag:
                            lat_long = geo_tag.text.strip()
                            lat, long = lat_long.split(';')
                            lat_lang = [
                                float(lat.strip()),
                                float(long.strip())]

                img_src = row.find('td', class_="infobox-image")
                if img_src:
                    flag_img_src = img_src.find('a', title=f"Flag of {self.country_name()}")
                    if flag_img_src:
                        flag_img = flag_img_src.find('img')
                        flag_img = "https:" + flag_img.get('src')
                        images.append(flag_img)

                    state_img_src = img_src.find_next('a',
                                                      title=f"State emblem (Coat of arms) of {self.country_name()}")
                    if state_img_src:
                        state_image = state_img_src.find('img')
                        state_emblem_img = "https:" + state_image.get('src')
                        images.append(state_emblem_img)
        return capital_name, lat_lang, images

    def province_names(self):
        provinces = []
        province_table = self.soup.find('table', class_="sortable")
        if province_table:
            province_table_element = province_table.find('span')
            if province_table_element:
                province_table_text = province_table_element.text
                if province_table_text:
                    if "Administrative division" in province_table_text:
                        for row in province_table.find_all('tr'):
                            province_link = row.find('a')
                            if province_link:
                                provinces.append(province_link.text)
        return provinces


def main():
    country_info = CountryInfo()
    country_urls = country_info.get_country_urls()
    for url in country_urls[1:]:
        country_data = country_info.parse_country_page(url)
        if country_data:
            print(json.dumps(country_data, indent=4))


if __name__ == "__main__":
    main()
