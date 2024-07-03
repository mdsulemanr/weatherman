import requests
from bs4 import BeautifulSoup
import json
import re


start_url = "https://en.wikipedia.org/wiki/Pakistan"


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
            flag_img_src = img_src.find('a', title=f"Flag of {country_info['name']}").find('img')
            flag_img = "https:" + flag_img_src.get('src')
            country_info["images"].append(flag_img)

            state_img_src = img_src.find_next('a', title=f"State emblem (Coat of arms) of {country_info['name']}").find('img')
            state_emblem_img = "https:" + state_img_src.get('src')
            country_info["images"].append(state_emblem_img)

    province_table = soup.find('table', class_="sortable")
    if "Administrative division" in province_table.find('span').text:
        for row in province_table.find_all('tr'):
            province_link = row.find('a')
            if province_link:
                country_info["provinces"].append(province_link.text)

    if not country_info["provinces"]:
        for header in soup.find_all(['h2', 'h3']):
            if header.span and ('Provinces' in header.span.text):
                provinces_list = header.find_next('ul')
                if provinces_list:
                    country_info["provinces"] = [li.text.strip() for li in provinces_list.find_all('li')]
                break

    return country_info


def main():
    country_data = parse_country_page(start_url)
    if country_data:
        print(json.dumps(country_data, indent=4))


if __name__ == "__main__":
    main()
