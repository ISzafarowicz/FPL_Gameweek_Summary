# FPL Gameweek Summary Dashboard <br>
This repository contains the FPL Gameweek Summary dashboard in a PBIX file format, as well as a BAT file for updating dashboard data and two folders: 'Dashboard_Data' and 'Scraping_Module'.<br>

## Getting Started <br>
To get started with the FPL Gameweek Summary Dashboard, follow these steps:<br>

1. Clone this repository to your local machine.<br>
2. Open the FPL Gameweek Summary.pbix file to view the dashboard.<br>
3. If you wish to update data on your local machine, install the required Python libraries by running <b>pip install -r requirements.txt.</b><br>

## Features<br>
### FPL Gameweek Summary PBIX File<br>
The FPL Gameweek Summary dashboard is a Power BI report that provides an overview of the Fantasy Premier League (FPL) game for the latest gameweek. <br>
The dashboard includes visualizations of key performance metrics, such as the total points scored by each player, their Expected Points as well as difference between Expected Points and actual points (Overachievers and Underachievers). <br>

### Update Dashboard BAT File <br>
<i>If you wish to update data locally, please make sure to edit update_dashboard.bat and specify path to your python.exe file (mine is "D:\Python\python.exe"). <br>
Alternatively, you can open update_dashboard.py script and run it inside your IDE. </i> <br>
The 'update_dashboard.bat' file is a batch file that automatically updates the dashboard data. When run, it scrapes the latest data from the FPL API using the FplScraper class defined in the 'scraping_fpl_api.py' file and saves it to the 'Dashboard_Data' folder. Refreshing data manually is not possible as the dashboard downloads data from the Github repository, not your local machine. <br>

## Folders<br>
### Dashboard_Data <br>
The 'Dashboard_Data' folder contains a CSV file for the latest gameweek's FPL data. This data is used by the FPL Gameweek Summary dashboard to generate the visualizations.<br>

### Scraping_Module <br>
The 'Scraping_Module' folder contains the 'scraping_fpl_api.py' file, which defines the FplScraper class used to scrape and clean data from the FPL API.<br>

## Usage<br>
To use the FPL Gameweek Summary dashboard, simply open the 'FPL Gameweek Summary.pbix' file using Power BI Desktop. To update the data in the dashboard locally, run the 'update_dashboard.bat' file (it will not update the dashboard itself). Note that you must have Python 3 installed to run the scraping script.<br>

## Disclaimer<br>
This dashboard and associated files are not affiliated with or endorsed by the Fantasy Premier League or its parent company. The data used in this dashboard is publicly available and has been scraped from the FPL API using the FplScraper class defined in the 'scraping_fpl_api.py' file.
