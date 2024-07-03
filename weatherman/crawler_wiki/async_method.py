import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup
import json

start_url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area"
base_url = "https://en.wikipedia.org"


async def get_country_urls(session, start_url):
    async with session.get(start_url) as response:
        text = await response.text()
        soup = BeautifulSoup(text, "html.parser")
        country_urls = []

        for link in soup.select(".wikitable tbody tr td a"):
            url = link.get('href')
            if url and url.startswith('/wiki/') and not url.startswith('/wiki/File:'):
                full_url = base_url + url
                if full_url not in country_urls:
                    country_urls.append(full_url)

    return country_urls


async def parse_country_page(session, url):
    async with session.get(url) as response:
        if response.status_code != 200:
            return None

        text = await response.text()
        soup = BeautifulSoup(text, "html.parser")

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


async def main():
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        country_urls = await get_country_urls(session, start_url)
        results = []

        tasks = [parse_country_page(session, url) for url in country_urls[1:]]
        for task in asyncio.as_completed(tasks):
            data = await task
            if data:
                results.append(data)
                print(json.dumps(data, indent=4))

        # Optionally, save results to file
        # with open('country_data.json', 'w') as f:
        #     json.dump(results, f, indent=4)

    end_time = time.time()
    total_execution_time = end_time - start_time
    print(f"Total execution time: {total_execution_time} seconds")

# To start, we run our make_all_requests coroutine with asyncio.run
# and pass through the same argument as the original version.
if __name__ == "__main__":
    asyncio.run(main())
