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
            "url": url,
            "response_code": response.status_code if response else None
        }
        if not response:
            return country_info

        soup = BeautifulSoup(response.content, "html.parser")
        self._parse_name(soup, country_info)

        return country_info

    def _parse_name(self, soup, country_info):
        country_name = soup.find('h1', id="firstHeading")
        if country_name:
            country_info["name"] = country_name.text

    def parse_and_print_country_page(self, url):
        country_data = self.parse_country_page(url)
        with self.lock:
            print(json.dumps(country_data, indent=4))


def main():
    wiki_crawler = WikipediaCrawler()
    country_urls = wiki_crawler.get_country_urls()

    for url in country_urls[1:]:
        thread = threading.Thread(target=wiki_crawler.parse_and_print_country_page, args=(url,))
        thread.start()
        thread.join()



if __name__ == "__main__":
    main()
