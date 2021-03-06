import argparse
import datetime
import json
import os
import re

import requests
from bs4 import BeautifulSoup

cleaned_results = []
now = str(datetime.datetime.now())
headers = ({
    "authority": "cdn.cookielaw.org",
    "method": "GET",
    "path": "/consent/69c5039d-4dfc-4172-bd11-428faaabf101/69c5039d-4dfc-4172-bd11-428faaabf101.json",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,nl;q=0.8",
    "cache-control": "no-cache",
    "origin": "https://www.funda.nl",
    "pragma": "no-cache",
    "referer": "https://www.funda.nl/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
})
ap = argparse.ArgumentParser()

ap.add_argument("-c", "--city", required=True,
                help="City name")
ap.add_argument("-s", "--street", required=True,
                help="Street name")
ap.add_argument("-r", "--radius", required=False,
                help="Radius in km")
ap.add_argument("-v", "--verbose", required=False,
                action='store_true',
                help="Additional printing")

args = vars(ap.parse_args())

city = args.get('city').lower()
street = args.get('street').lower()
radius = int(args.get('radius', 2))
verbose = args.get('verbose', False)

print(f'scraping houses in {street}, {city} in radius of {radius} km...')


def strip_number(element):
    if element is None:
        return 0

    reg_num = re.search("[0-9.]+", element.text.strip())
    if reg_num is None:
        return 0

    return int(float(reg_num.group().replace('.', '')))


for page_num in range(100):
    URL = f'https://www.funda.nl/koop/{city.replace(" ", "-")}/straat-{street.replace(" ", "-")}/+{radius}km/p{page_num + 1}'
    html = requests.get(URL, headers=headers)
    soup = BeautifulSoup(html.content, 'html.parser')
    results = soup.find_all('li', class_='search-result')

    if len(results) == 0:
        break

    for house_elem in results:
        street_name = house_elem.find('h2', class_='search-result__header-title')
        location_info = house_elem.find('h4', class_='search-result__header-subtitle').text.strip()
        postcode = re.search("^\d{4}\s?\w{2}", location_info).group()
        city = location_info[8:]
        price = house_elem.find('span', class_='search-result-price')
        additional_info = house_elem.find('ul', class_='search-result-kenmerken')
        room_total = additional_info.find_all('li')[1] if len(additional_info.find_all('li')) > 1 else None
        living_area = house_elem.find('span', title='Gebruiksoppervlakte wonen')
        plot_area = house_elem.find('span', title='Perceeloppervlakte')

        is_valid_house = True
        if is_valid_house:
            cleaned_results.append({
                "street_name": street_name.text.strip(),
                "postcode": postcode,
                "city": city,
                "price": strip_number(price),
                "room_total": strip_number(room_total),
                "plot_area": strip_number(plot_area),
                "living_area": strip_number(living_area),
                "scraped_at": now
            })

print(f'Found {len(cleaned_results)} results')

if verbose:
    print(f'Results overview:')

    if len(cleaned_results) > 0:
        for result in cleaned_results:
            print(f'street: {result["street_name"]}')
            print(f'postcode: {result["postcode"]}')
            print(f'city: {result["city"]}')
            print(f'price: € {result["price"]} k.k.')
            print(f'room_total: {result["room_total"]}')
            print(f'living_area: {result["living_area"]} m²')
            print(f'plot_area: {result["plot_area"]} m²')
            print(f'***************')
            print()

        print(f'Total results {len(cleaned_results)}')

current_data = {
    "entities": []
}

try:
    project_root = os.path.dirname(os.path.abspath(__file__))
    data_file = f'{project_root}/data/data.json'
    with open(data_file) as file:
        current_data = json.load(file)
except FileNotFoundError:
    pass

with open(data_file, 'w') as file:
    entities = [*current_data["entities"], *cleaned_results]
    updated_data = {
        "last_updated": now,
        "total_entities": len(entities),
        "entities": entities
    }
    json.dump(updated_data, file)
