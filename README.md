# Madden2021Analysis
Scraped EA Website for all Madden 21 ratings from Launch through Conference Championships with light analysis of rating changes. 
Used Selenium web driver with Python to scrape the Madden 21 Ratings database located at https://www.ea.com/games/madden-nfl/madden-nfl-21/player-ratings.
Took full weekly ratings with updates (from Launch - Conference Championship games) of top ~800 players. 

Web Scrapers:
  - eaScraper.py : Scrapes the EA Sports website for Madden player ratings using Selenium with Python (ref: https://www.ea.com/games/madden-nfl/madden-nfl-21/player-ratings)
  - pfrScraper.py: Scrapes pro-football-reference player stats using BeautifulSoup python library (ref: https://www.pro-football-reference.com/)

Data Sets:
  - allRatings.csv : ratings for the top ~800 players in madden (40 pages)
  - playerStats2021/qb_stats.csv: Passing statistics from the 2021 season
  - playerStats2021/rb_stats.csv: Rushing statistics from the 2021 season
  - playerStats2021/wr_stats.csv: Receiving statistics from the 2021 season
  - playerStats2021/def_stats.csv: Defensive statistics from the 2021 season

Data Dictionaries:
  data_dict.txt : data dictionary for allRatings.csv data table

There are a few players missing as the scraper is not perfect. The EA structure seems to change when ratings get updated, forcing me to go back in and alter code.
The following players with >80 end of season rating are missing:
  - James Robinson
  - Logan Ryan
  - DJ Chark
  - Jordan Reed
  - Damon Harrison
  - Leveon Bell

I do plan to add them in at some point.
