import argparse
import re

import requests
from bs4 import BeautifulSoup

cleaned_results = []
headers = ({
    'Referer': 'https://www.funda.nl/koop/woudenberg/straat-paulus-potterlaan/+2km/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
})
ap = argparse.ArgumentParser()

ap.add_argument("-c", "--city", required=True,
   help="City name")
ap.add_argument("-s", "--street", required=True,
   help="Street name")
ap.add_argument("-r", "--radius", required=False,
   help="Radius in km")

args = vars(ap.parse_args())

city = args.get('city').lower()
street = args.get('street').lower()
radius = int(args.get('radius', 2))

print(f'scraping houses in {street}, {city} in radius of {radius} km...')


def strip_number(element):
    if element is None:
        return 0

    reg_num = re.search("[0-9.]+", element.text.strip())
    if reg_num is None:
        return 0

    return int(float(reg_num.group().replace('.', '')))


for page_num in range(100):
    URL = f'https://www.funda.nl/koop/{city.replace(" ", "-")}/straat-{street.replace(" ", "-")}/+{radius}km/p{page_num+1}'
    print(URL)
    html = requests.get(URL, headers=headers)
    soup = BeautifulSoup(html.content, 'html.parser')
    results = soup.find_all('li', class_='search-result')

    if len(results) == 0:
        break

    for house_elem in results:
        street_name = house_elem.find('h2', class_='search-result__header-title')
        loaction_info = house_elem.find('h4', class_='search-result__header-subtitle')
        price = house_elem.find('span', class_='search-result-price')
        additional_info = house_elem.find('ul', class_='search-result-kenmerken')
        room_total = additional_info.find_all('li')[1] if len(additional_info.find_all('li')) > 1 else None
        living_area = house_elem.find('span', title='Gebruiksoppervlakte wonen')
        plot_area = house_elem.find('span', title='Perceeloppervlakte')


        is_valid_house = city in loaction_info.text.strip().lower()
        if is_valid_house:
            cleaned_results.append({
                "street_name": street_name.text.strip(),
                "loaction_info": loaction_info.text.strip(),
                "price": strip_number(price),
                "room_total": strip_number(room_total),
                "plot_area": strip_number(plot_area),
                "living_area": strip_number(living_area)
            })

print(f'Found {len(cleaned_results)} results')
print(f'Results overview:')

if len(cleaned_results) > 0:
    for result in cleaned_results:
        print(f'street: {result["street_name"]}')
        print(f'location info: {result["loaction_info"]}')
        print(f'price: € {result["price"]} k.k.')
        print(f'room_total: {result["room_total"]}')
        print(f'living_area: {result["living_area"]} m²')
        print(f'plot_area: {result["plot_area"]} m²')
        print(f'***************')
        print()

    print(f'Total results {len(cleaned_results)}')
