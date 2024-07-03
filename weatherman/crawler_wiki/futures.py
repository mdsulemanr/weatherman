import json

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

START_URL = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area"


def fetch_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return None


def parse_country_page(url):
    response = fetch_url(url)
    if not response:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

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
        country_name["name"] = country_name.text

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
                            float(long.strip())]

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


def main():
    response = fetch_url(START_URL)
    if not response:
        print("Failed to fetch the start URL.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    country_urls = set()

    for link in soup.select('table.wikitable a'):
        href = link.get('href')
        if href and href.startswith('/wiki/'):
            full_url = f"https://en.wikipedia.org{href}"
            country_urls.add(full_url)

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(parse_country_page, url): url for url in country_urls}
        for future in as_completed(future_to_url):
            country_data = future.result()
            if country_data:
                print(json.dumps(country_data, indent=4))


if __name__ == "__main__":
    main()
