#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm
from urllib.request import urlopen
import re
import csv
import sqlite3


# In[ ]:

def create_csv():
    f = csv.writer(open('bollyactors.csv', 'w'))
    f.writerow(['Name', 'Desc', 'Image'])


    def extractData(list):
        actors_details_containers = list
        for i, container in enumerate(actors_details_containers):

            name = container.h3.a.text

            desc = container.find('p', class_ = '').text

            image = container.a.img.get('src')

            f.writerow([name, desc, image])

    url_to_scrape = [
        'https://www.imdb.com/list/ls068010962/',
        'https://www.imdb.com/list/ls068010962/?sort=list_order,asc&mode=detail&page=2'
        ]


    def extractPage(str):
        response = get(str)

        html_soup = BeautifulSoup(response.text, 'html.parser')

        html_soup = BeautifulSoup(response.text, 'html.parser')

        actors_details_containers = html_soup.find_all('div', class_ = 'lister-item mode-detail')

        images2 = html_soup.find_all('img', {'src':re.compile('.jpg')})

        extractData(actors_details_containers)

    for i in range(len(url_to_scrape)):
        extractPage(url_to_scrape[i])


def create_db():
    create_csv()
    conn = sqlite3.connect('bolly.db')
    c = conn.cursor()
    c.execute('CREATE TABLE BollywoodActors1 (Name, Desc, Image);')
    with open('bollyactors.csv', 'r') as csv_file:
        dr = csv.DictReader(csv_file)
        to_db = [(i['Name'], i['Desc'], i['Image']) for i in dr]
    c.executemany('INSERT INTO BollywoodActors (Name, Desc, Image) VALUES (?, ?, ?);', to_db)
    conn.commit()
    conn.close()

create_db()
