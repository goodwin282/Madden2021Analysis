# imports
import pandas as pd
from bs4 import BeautifulSoup
import requests
from lxml import html

# scrape tables from pro football reference
def scrape_table(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    if ((url[-11:-4] == 'rushing') | (url[-11:-4] == 'defense')):
        column_headers = soup.findAll('tr')[1]
    else:
        column_headers = soup.findAll('tr')[0]

    column_headers = [i.getText() for i in column_headers.findAll('th')]
    rows = soup.findAll('tr')[1:]

    pos_stats = []
    for i in range(len(rows)):
      pos_stats.append([col.getText() for col in rows[i].findAll('td')])

    data = pd.DataFrame(pos_stats, columns=column_headers[1:])

    return data

qb_stats = scrape_table('https://www.pro-football-reference.com/years/2020/passing.htm')
rb_stats = scrape_table('https://www.pro-football-reference.com/years/2020/rushing.htm')
wr_stats = scrape_table('https://www.pro-football-reference.com/years/2020/receiving.htm')
def_stats = scrape_table('https://www.pro-football-reference.com/years/2020/defense.htm')

qb_stats.to_csv('playerStats2021/qb_stats.csv')
rb_stats.to_csv('playerStats2021/rb_stats.csv')
wr_stats.to_csv('playerStats2021/wr_stats.csv')
def_stats.to_csv('playerStats2021/def_stats.csv')
