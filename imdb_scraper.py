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
resume = []

# movies are in the lister-item mode-advanced div
movie_div = soup.find_all('div', class_='lister-item mode-advanced')

# loop through each container
for container in movie_div:
    # name
    name = container.h3.a.text
    titles.append(name)

    # year
    year = container.h3.find('span', class_='lister-item-year').text
    years.append(year)

    # time
    runtime = container.p.find('span', class_='runtime').text if container.p.find(
        'span', class_='runtime').text else '-'
    time.append(runtime)

    # rating
    rating = float(container.strong.text)
    imdb_ratings.append(rating)

    # metascore
    metascore = container.find('span', class_='metascore').text if container.find(
        'span', class_='metascore').text else '-'
    # remove spaces after number
    metascore = metascore.strip()
    metascores.append(metascore)

    # votes
    nv = container.find_all('span', attrs={'name': 'nv'})
    vote = nv[0].text
    votes.append(vote)

    # grosses
    grosses = nv[1].text if len(nv) > 1 else '-'
    us_gross.append(grosses)

    # resume
    p_tags = container.find_all('p', class_='text-muted')
    text = p_tags[1].text if len(p_tags) >= 2 else '-'
    resume.append(text)
