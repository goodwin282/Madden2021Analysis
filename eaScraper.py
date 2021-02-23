# imports
import pandas as pd
from bs4 import BeautifulSoup
import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

# set up ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome("C:\Program Files\ChromeDriver\chromedriver.exe", options=options)

# open madden ratings first page
url = 'https://www.ea.com/games/madden-nfl/madden-nfl-21/player-ratings'
driver.get(url)
# first show we are hitting page
driver.title

# access shadow elements
def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root

# go to page
def go_to_page(page_number):
    page = str(page_number)
    s1 = driver.find_element_by_tag_name('ea-pagination')
    driver.execute_script("arguments[0].setAttribute('current-page', arguments[1])", s1, page)
    driver.implicitly_wait(10)
    return True

def get_page_player_rows():
    s1 = driver.find_element_by_tag_name('body')
    s2 = s1.find_elements_by_tag_name('ea-section')[0]
    s3 = s2.find_element_by_tag_name('ea-section-column')
    s4 = s3.find_element_by_tag_name('ea-player-ratings-data-table')

    shadow_section = expand_shadow_element(s4)
    s5 = shadow_section.find_element_by_class_name('eapl-player-ratings-data-table__wrapper')
    s6 = s5.find_element_by_id('tbody')
    players = s6.find_elements_by_class_name('eapl-player-ratings-data-table__tbody-row')
    return players

def go_to_player_page(player_row):
    s1 = player_row.find_element_by_class_name('eapl-player-ratings-data-table__tbody-row-data')
    s2 = s1.find_element_by_class_name('eapl-player-ratings-data-table__attributes')
    s3 = s2.find_element_by_class_name("eapl-player-ratings-data-table-columns")
    link = s3.find_element_by_tag_name('a')
    return driver.execute_script("arguments[0].click();", link)

def get_page_week_rows():
    s1 = driver.find_element_by_tag_name('body')
    s2 = s1.find_elements_by_tag_name('ea-section')[0]
    s3 = s2.find_element_by_tag_name('ea-section-column')
    s4 = s3.find_element_by_tag_name('ea-player-ratings-data-table')

    shadow_section = expand_shadow_element(s4)
    s5 = shadow_section.find_element_by_class_name('eapl-player-ratings-data-table__wrapper')
    s6 = s5.find_element_by_id('tbody')
    s7 = s6.find_element_by_class_name('eapl-player-ratings-data-table__tbody-row')
    s8 = s7.find_element_by_class_name('eapl-player-ratings-data-table__expand')
    s9 = s8.find_element_by_class_name("eapl-player-ratings-data-table__expand-iteration-wrapper")
    s10 = s9.find_element_by_class_name("eapl-player-ratings-data-table__expand-iteration")
    s11 = s10.find_element_by_class_name("eapl-player-ratings-data-table__expand-iteration-table")
    s12 = s11.find_element_by_tag_name('ea-player-ratings-iteration-table')

    shadow_section = expand_shadow_element(s12)
    s13 = shadow_section.find_element_by_class_name("eapl-player-ratings-iteration-table__wrapper")
    s14 = s13.find_element_by_id("iterationBody")
    week = s14.find_elements_by_class_name('eapl-player-ratings-iteration-table__tbody-row')
    return week

# get weekly ratings for player page with week list
def get_week_ratings(week_list):
    player_name = driver.title.split('-')[0].strip()
    player_position = driver.title.split('-')[1].strip()
    player_team = driver.title.split('-')[2].strip()
    week_and_ratings = []
    for week in week_list:
        s1 = week.find_element_by_class_name('eapl-player-ratings-iteration-table__tbody-row-data')
        s2a = s1.find_element_by_class_name('eapl-player-ratings-iteration-table__attributes')
        s3a = s2a.find_elements_by_tag_name('div')[0:2]
        week, total_rating = s3a[0].find_element_by_tag_name('span').text, int(s3a[1].find_element_by_tag_name('span').text)

        s2b = s1.find_element_by_class_name('eapl-player-ratings-iteration-table__tbody-ratings')
        s3b = s2b.find_element_by_class_name('eapl-player-ratings-iteration-table__visable-ratings')
        s4b = s3b.find_element_by_class_name('eapl-player-ratings-iteration-table__ratings-scroll-container')
        s5b = s4b.find_elements_by_class_name('eapl-player-ratings-iteration-table-columns')
        all_attributes = []
        visual_rating_style_shifts = ['transform: translateX(0%);', 'transform: translateX(-100%);', 'transform: translateX(-200%);', 'transform: translateX(-300%);',
        'transform: translateX(-400%);', 'transform: translateX(-430%);']
        atts = [range(0,10), range(10,20), range(20,30), range(30,40), range(40,50), range(50,53)]
        for i in range(6):
            slide_page(s1, visual_rating_style_shifts[i])
            sleep(1)
            for j in atts[i]:
                all_attributes.append(int(s5b[j].find_elements_by_tag_name('span')[0].text))
        week_and_ratings.append([player_name, player_position, player_team, week, total_rating, all_attributes])
    return week_and_ratings

def slide_page(s1, position):
    # get element to slide weekly ratings
    sa2 = s1.find_element_by_class_name('eapl-player-ratings-iteration-table__tbody-ratings')
    sa3 = sa2.find_element_by_class_name('eapl-player-ratings-iteration-table__visable-ratings')
    sa4 = sa3.find_element_by_class_name('eapl-player-ratings-iteration-table__ratings-scroll-container')

    # get element to slide attribute titles
    sb1 = driver.find_element_by_tag_name('body')
    sb2 = sb1.find_element_by_tag_name('ea-section')
    sb3 = sb2.find_element_by_tag_name('ea-section-column')
    sb4 = sb3.find_element_by_tag_name('ea-player-ratings-data-table')
    shadow_section1 = expand_shadow_element(sb4)

    sb5 = shadow_section1.find_element_by_class_name('eapl-player-ratings-data-table__wrapper')
    sb6 = sb5.find_element_by_id('tbody')
    sb7 = sb6.find_element_by_class_name('eapl-player-ratings-data-table__tbody-row')
    sb8 = sb7.find_element_by_class_name('eapl-player-ratings-data-table__expand')
    sb9 = sb8.find_element_by_class_name('eapl-player-ratings-data-table__expand-iteration-wrapper')
    sb10 = sb9.find_element_by_class_name('eapl-player-ratings-data-table__expand-iteration')
    sb11 = sb10.find_element_by_class_name('eapl-player-ratings-data-table__expand-iteration-table')
    sb12 = sb11.find_element_by_tag_name('ea-player-ratings-iteration-table')

    shadow_section2 = expand_shadow_element(sb12)
    sb13 = shadow_section2.find_element_by_class_name('eapl-player-ratings-iteration-table__wrapper')
    sb14 = sb13.find_element_by_id('thead')
    sb15 = sb14.find_element_by_class_name('eapl-player-ratings-iteration-table__ratings')
    sb16 = sb15.find_element_by_class_name('eapl-player-ratings-iteration-table__visable-ratings')
    sb17 = sb16.find_element_by_class_name('eapl-player-ratings-iteration-table__ratings-scroll-container')

    return driver.execute_script("arguments[0].setAttribute('style', arguments[1])", sa4, position), driver.execute_script("arguments[0].setAttribute('style', arguments[1])", sb17, position)

# final step, get ratings
#### df = pd.DataFrame() # do not uncomment or df will be deleted
df = pd.read_csv('allRatings.csv')
list_no = []
def go_to_next_player(page_num, players):
    global df
    global list_no
    # for i in range(len(players_list)):
    # for i in range(20): # working better
    for i in range(0,1): # for testing/fixing
        driver.implicitly_wait(10)
        go_to_page(page_num)
        players = get_page_player_rows()
        driver.implicitly_wait(10)
        go_to_player_page(players[i])
        driver.implicitly_wait(10)

        try:
            weeks = get_page_week_rows()
            player_ratings = get_week_ratings(weeks)
            if len(player_ratings) < 22:
                while len(player_ratings) < 22:
                    player_ratings.append(['NA'])
            df1 = pd.DataFrame(player_ratings, columns = ['a', 'b', 'c', 'd', 'e', 'f'])
            colf_exploded = pd.DataFrame(df1['f'].values.tolist())
            df = df.append(pd.concat([df1.loc[:, 'a':'e'], colf_exploded], axis = 1))
        except:
            list_no = list_no.append(driver.title.split('-')[0])

        driver.implicitly_wait(10)
        driver.execute_script("window.history.go(-1)")
        print(len(df))

    return True

def scrape_all_pages(start_page, num_pages):
    global df
    page = start_page
    while page <= num_pages:
        go_to_page(page)
        players = get_page_player_rows()
        go_to_next_player(page, players)
        print(len(df))
        df.to_csv('allRatings.csv')
        page += 1
    return True

# get the top 800 players
go_to_page(2)
scrape_all_pages(2,2)

df
