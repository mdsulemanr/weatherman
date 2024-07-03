import requests
from bs4 import BeautifulSoup
import json
import threading

start_url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area"
base_url = "https://en.wikipedia.org"
lock = threading.Lock()


def get_country_urls(start_url):
    response = requests.get(start_url)
    soup = BeautifulSoup(response.content, "html.parser")
    country_urls = []

    for link in soup.select(".wikitable tbody tr td a"):
        url = link.get('href')
        if url and url.startswith('/wiki/') and not url.startswith('/wiki/File:'):
            full_url = base_url + url
            if full_url not in country_urls:
                country_urls.append(full_url)

    return country_urls


def parse_country_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    country_info = {
        "name": None,
        "capital": None,
        "provinces": [],
        "images": [],
        "lat_lang": [],
        "url": url,
        "response_code": response.status_code
    }

    country_name = soup.find('h1', id="firstHeading")
    if country_name:
        country_info["name"] = country_name.text

    infobox = soup.find('table', class_='infobox')
    if infobox:
        for row in infobox.find_all('tr'):
            header = row.find('th', class_='infobox-label')
            if header and 'Capital' in header.text:
                capital_link = row.find('td', class_='infobox-data').find('a')
                if capital_link:
                    country_info["capital"] = capital_link.text.strip()

                    geo_tag = row.find_next('span', class_='geo')
                    if geo_tag:
                        lat_long = geo_tag.text.strip()
                        lat, long = lat_long.split(';')
                        country_info["lat_lang"] = [
                            float(lat.strip()),
                            float(long.strip())
                        ]

            img_src = row.find('td', class_="infobox-image")
            if img_src:
                flag_img_src = img_src.find('a', title=f"Flag of {country_info['name']}")
                if flag_img_src:
                    flag_img = flag_img_src.find('img')
                    flag_img = "https:" + flag_img.get('src')
                    country_info["images"].append(flag_img)

                state_img_src = img_src.find_next('a', title=f"State emblem (Coat of arms) of {country_info['name']}")
                if state_img_src:
                    state_image = state_img_src.find('img')
                    state_emblem_img = "https:" + state_image.get('src')
                    country_info["images"].append(state_emblem_img)

    province_table = soup.find('table', class_="sortable")
    if province_table:
        province_table_element = province_table.find('span')
        if province_table_element:
            province_table_text = province_table_element.text
            if province_table_text:
                if "Administrative division" in province_table_text:
                    for row in province_table.find_all('tr'):
                        province_link = row.find('a')
                        if province_link:
                            country_info["provinces"].append(province_link.text)

    return country_info


def worker(url, results):
    country_data = parse_country_page(url)
    if country_data:
        with lock:
            results.append(country_data)
        print(json.dumps(country_data, indent=4))


def main():
    country_urls = get_country_urls(start_url)
    threads = []
    results = []

    for url in country_urls[1:]:
        print(url + '\n')
        thread = threading.Thread(target=worker, args=(url, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    with open('country_data.json', 'w') as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    main()
