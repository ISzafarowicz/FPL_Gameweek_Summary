import pandas as pd
from Scraping_Module.scraping_fpl_api import FplScraper

scraper = FplScraper()
curr_gw = scraper.load_gameweek(GW = 25)
curr_gw.to_csv('Dashboard_Data/current_gameweek_data.csv', index=False)
print('Current Gameweek Data Updated')