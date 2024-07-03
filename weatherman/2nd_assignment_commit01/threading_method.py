import requests
from bs4 import BeautifulSoup
import json
import threading

START_URL = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area"
BASE_URL = "https://en.wikipedia.org"


class WikipediaCrawler:
    def __init__(self):
        self.country_urls = []
        self.lock = threading.Lock()

    def _get_response(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {url}: {e}")
            return None

    def get_country_urls(self):
        response = self._get_response(START_URL)
        if not response:
            return self.country_urls

        soup = BeautifulSoup(response.content, "html.parser")
        for link in soup.select(".wikitable tbody tr td a"):
            url = link.get('href')
            if url and url.startswith('/wiki/') and not url.startswith('/wiki/File:'):
                full_url = BASE_URL + url
                if full_url not in self.country_urls:
                    self.country_urls.append(full_url)

        return self.country_urls

    def parse_country_page(self, url):
        response = self._get_response(url)
        country_info = {
            "name": None,
            "capital": None,
            "provinces": [],
            "images": [],
            "lat_lang": [],
            "url": url,
            "response_code": response.status_code if response else None
        }
        if not response:
            return country_info

        soup = BeautifulSoup(response.content, "html.parser")

        self._parse_name(soup, country_info)
        self._parse_infobox(soup, country_info)
        self._parse_provinces(soup, country_info)

        return country_info

    def _parse_name(self, soup, country_info):
        country_name = soup.find('h1', id="firstHeading")
        if country_name:
            country_info["name"] = country_name.text

    def _parse_infobox(self, soup, country_info):
        infobox = soup.find('table', class_='infobox')
        if infobox:
            self._parse_capital(infobox, country_info)
            self._parse_images(infobox, country_info)

    def _parse_capital(self, infobox, country_info):
        for row in infobox.find_all('tr'):
            header = row.find('th', class_='infobox-label')
            if header and 'Capital' in header.text:
                capital_link = row.find('td', class_='infobox-data').find('a')
                if capital_link:
                    country_info["capital"] = capital_link.text.strip()
                    self._parse_lat_lang(row, country_info)

    def _parse_lat_lang(self, row, country_info):
        geo_tag = row.find_next('span', class_='geo')
        if geo_tag:
            lat_long = geo_tag.text.strip()
            lat, long = lat_long.split(';')
            country_info["lat_lang"] = [
                float(lat.strip()),
                float(long.strip())]

    def _parse_images(self, infobox, country_info):
        for row in infobox.find_all('tr'):
            img_src = row.find('td', class_="infobox-image")
            if not img_src:
                continue

            flag_img_src = img_src.find('a', title=f"Flag of {country_info['name']}")
            if flag_img_src:
                flag_img = flag_img_src.find('img')
                if flag_img:
                    country_info["images"].append("https:" + flag_img.get('src'))

            state_img_src = img_src.find_next('a', title=f"State emblem (Coat of arms) of {country_info['name']}")
            if state_img_src:
                state_image = state_img_src.find('img')
                if state_image:
                    country_info["images"].append("https:" + state_image.get('src'))

    def _parse_provinces(self, soup, country_info):
        province_table = soup.find('table', class_="sortable")
        if not province_table:
            return

        province_table_element = province_table.find('span')
        if not province_table_element:
            return

        province_table_text = province_table_element.text
        if not province_table_text or "Administrative division" not in province_table_text:
            return

        for row in province_table.find_all('tr'):
            province_link = row.find('a')
            if province_link:
                country_info["provinces"].append(province_link.text)

    def main(self):
        country_urls = self.get_country_urls()

        threads = []
        for url in country_urls[1:]:
            thread = threading.Thread(target=self.parse_and_print_country_page, args=(url,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def parse_and_print_country_page(self, url):
        country_data = self.parse_country_page(url)
        with self.lock:
            print(json.dumps(country_data, indent=4))


if __name__ == "__main__":
    crawler = WikipediaCrawler()
    crawler.main()
