'''This script gets data from a web page and converts it into a pandas DataFrame.'''

# Import libreries
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime
from datetime import timedelta
from urllib.parse import urljoin
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os

path = os.path.join(os.getcwd(), 'data')

# Date transformation
checkin_date = datetime.today() + timedelta(days=0)
checkout_date = checkin_date + timedelta(days=1)

checkin_date = checkin_date.strftime('%Y-%m-%d')
checkout_date = checkout_date.strftime('%Y-%m-%d')

# URL parametrization
city = 'Quito'
country = 'Ecuador'
adults = 2
rooms = 1
children = 1
children_ages = 2

URL = f'https://www.booking.com/searchresults.html?ss={city}%2C+{country}&dest_type=city'
URL += f'&checkin={checkin_date}&checkout={checkout_date}&group_adults={adults}&no_rooms={rooms}&group_children={children}&age={children_ages}'

# Set user-agent parameters simulating this script is not a web scraping script
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

request = requests.get(URL, headers=headers)
soup = bs(request.text, 'lxml')

table = soup.find_all('div', attrs={"data-testid": "property-card"})

# Get hotels
hotels = []
for row in table:
    name = row.find('div', attrs={"data-testid": "title"}
                    ).text.strip().replace(',', '').replace(';', '')
    hotels.append(name)

# Get location
locations = []
for row in table:
    location = row.find(
        'span', attrs={"data-testid": "address"}).text.strip().replace(';', '')
    locations.append(location)

# Get prices
prices = []
for row in table:
    price_all = row.find(
        'span', attrs={"data-testid": "price-and-discounted-price"}).text
    price = float(price_all.replace('MXN', '').replace(",", "").strip())
    prices.append(price)

df_hotels = pd.DataFrame(
    data={'Hotel': hotels, 'Location': locations, 'Price': prices})

file_name = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'.csv'

os.chdir(path)

df_hotels.to_csv(file_name, index=False, sep='\t')
