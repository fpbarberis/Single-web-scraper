import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import chardet

# web to scrap
url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"
headers = {"Accept-Language": "en-US, en;q=0.5"}
results = requests.get(url, headers=headers)

# Detect encoding
encoding = chardet.detect(results.content)['encoding']

# if not detect, try utf-8
if encoding is None:
    encoding = 'utf-8'

# Decode the response of web page
soup = BeautifulSoup(results.content.decode(encoding), "html.parser")
# visualize the response
# print(soup.prettify())

# empty lists to store data
titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

# movies are in the lister-item mode-advanced div
movie_div = soup.find_all('div', class_='lister-item mode-advanced')

# loop through each container
for container in movie_div:
    # film name
    name = container.h3.a.text
    titles.append(name)

    # film year
    year = container.h3.find('span', class_='lister-item-year').text
    years.append(year)
