import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://en.wikipedia.org/wiki/Pakistan'

class WikiCrawler:

    def parse_country_info(self):
        r = requests.get(BASE_URL)

        soup = BeautifulSoup(r.content, 'html.parser')


        country_info = {
            'name': None,
            'capital': None,
            'official_lang': None,
            'lat_lan': [],
            'off_lang': [],
            'native_lang': None,
            'religion': [],
        }


    def country_name(self, soup, country_info):
        country_name = soup.find('h1', id="firstHeading").text
        if country_name:
            country_info['name'] = country_name


    table = soup.find('table', class_='infobox')
    for row in table.find_all('tr'):
        img_row = row.find('td', class_="infobox-image")
        if img_row:
            img_url = img_row.find('a', title=f"Flag of {country}").find('img').get('src')
            if img_url:
                img_full_url = "https:" + img_url
                print(img_full_url)

            state_emblem = img_row.find_next('a', title=f"State emblem (Coat of arms) of {country}").find('img').get(
                'src')
            if state_emblem:
                state_emblem_url = "https:" + state_emblem
                print(state_emblem_url)

        cap_row = row.find('th', class_="infobox-label")
        if cap_row and "Capital" in cap_row.text:
            cap_line = cap_row.find_next('td')
            cap_text = cap_line.find('a').text
            print(cap_text)
            lat_lan = cap_line.find_next(class_="geo").text
            lat_lan_list = lat_lan.split(';')
            country_info['lat_lan'].append(lat_lan_list[0].strip())
            country_info['lat_lan'].append(lat_lan_list[1].strip())
            print(country_info["lat_lan"])

        off_lang_row = row.find('th', class_="infobox-label")
        if off_lang_row and "Official languages" in off_lang_row.text:
            lang_box = off_lang_row.find_next('div', class_="hlist")
            if lang_box:
                all_lang = lang_box.find('ul').find_all('li')
                for lang in all_lang:
                    country_info["off_lang"].append(lang.find('a').text)
                print(country_info["off_lang"])

        native_lang_row = row.find('th', class_="infobox-label")
        if native_lang_row and "Native languages" in native_lang_row.text:
            country_info["native_lang"] = native_lang_row.find_next('td').find('a').text
            print(country_info["native_lang"])

        native_lang_row = row.find('th', class_="infobox-label")
        if native_lang_row and "Religion" in native_lang_row.text:
            religion_box = row.find('td').find('div', class_="plainlist").find('ul')
            if religion_box:
                for religion_stats in religion_box:
                    religion = religion_stats.text.split(" ")[1].strip()
                    country_info["religion"].append(religion)
                print(country_info["religion"])

