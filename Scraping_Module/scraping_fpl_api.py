import requests
import pandas as pd
from datetime import datetime

class FplScraper:
    """
    A class for scraping data from the official Fantasy Premier League API.

    This class provides methods for retrieving data from the Fantasy Premier League API. 
    It requires the pandas, datetime, and requests packages to be installed in your environment.

    Attributes:
        base_url (str): The base URL for the Fantasy Premier League website.
    """

    def __init__(self, display_pandas_warnings=False):
        """
        Initializes a new instance of the FplScraper class.
        
        """
        self.base_url = "https://fantasy.premierleague.com/api/"
        self.display_pandas_warnings = display_pandas_warnings

    def load_latest_gameweek(self):
        """
        Scrapes data from the latest FPL gameweek.

        Returns:
            pandas dataframe: A dataframe containing data from the latest FPL gameweek.
        """
    #data scraping and cleaning
        if self.display_pandas_warnings == False:
            import warnings
            from pandas.core.common import SettingWithCopyWarning
            warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
        r = requests.get(self.base_url + 'bootstrap-static/')
        json = r.json()
        #deadline dates
        df_dates = pd.json_normalize(json['events'])
        df_dates = df_dates[['id', 'deadline_time']]
        df_dates['deadline_time'] = pd.to_datetime(df_dates['deadline_time'], utc=True)
        df_dates.columns = ['gameweek_number', 'deadline_time']
        today = datetime.now().date().strftime('%Y-%m-%d %H:%M:%S')
        past_dates = df_dates[df_dates.deadline_time < today]
        past_dates.sort_values('gameweek_number', ascending = False, inplace = True)
        GW = past_dates.iloc[0].gameweek_number


        #player web names, price ect.
        elements_df = pd.DataFrame(json['elements'])
        elements_types_df = pd.DataFrame(json['element_types'])
        teams_df = pd.DataFrame(json['teams']) 

        slim_elements_df = elements_df[['id','web_name','team','element_type','now_cost','selected_by_percent',
                                                'transfers_in','transfers_out','form','total_points','bonus',
                                                'points_per_game','value_season','minutes','goals_scored','assists',
                                                'clean_sheets','saves', 'ict_index']]
        slim_elements_df['position'] = slim_elements_df.element_type.map(elements_types_df.set_index('id').singular_name)
        slim_elements_df['team'] = slim_elements_df.team.map(teams_df.set_index('id').name)
        slim_elements_df['value'] = slim_elements_df.value_season.astype(float)
        slim_elements_df['form'] = slim_elements_df.form.astype(float)
        slim_elements_df['selected_by_percent'] = slim_elements_df.selected_by_percent.astype(float)
        slim_elements_df['ict_index'] = slim_elements_df.ict_index.astype(float)
        slim_elements_df['points_per_game'] = slim_elements_df['points_per_game'].astype(float)
        slim_elements_df['now_cost'] = slim_elements_df['now_cost'] / 10
        del slim_elements_df['value_season']
        del slim_elements_df['element_type']
        df_first = slim_elements_df[['id', 'web_name', 'team', 'now_cost', 'position']]

        #player stats for current gameweek
        r = requests.get(self.base_url + '/event/' + str(GW) + '/live/').json()
        df_second = pd.json_normalize(r['elements'])
        df_second = df_second.drop('explain', axis = 1)
        colnames = [col.replace('stats.', '') for col in df_second.columns]
        df_second.columns = colnames
        df = df_first.merge(df_second, how = 'left', on = 'id')

        point_calculator = pd.DataFrame({'position': ['Goalkeeper', 'Defender', 'Midfielder', 'Forward'], 'points_per_goal': [6, 6, 5, 4], 'points_per_assist': [3, 3, 3, 3], 'points_per_clean_sheet': [4, 4, 1, 0], 'points_per_save': [0.33, 0, 0, 0], 'points_per_minute': [0.033, 0.033, 0.033, 0.033]})
        df = df.merge(point_calculator, how = 'left', on = 'position')
        df['expected_goals'] = df['expected_goals'].astype(float)
        df['expected_assists'] = df['expected_assists'].astype(float)
        df['expected_goal_involvements'] = df['expected_goal_involvements'].astype(float)
        df['expected_goals_conceded'] = df['expected_goals_conceded'].astype(float)
        df['expected_points'] = df['expected_goals'] * df['points_per_goal'] + df['expected_assists'] * df['points_per_assist'] + df['clean_sheets'] * df['points_per_clean_sheet'] + df['saves'] * df['points_per_save'] + df['bonus'] + df['minutes'] * df['points_per_minute']
        df['xP_minus_Points'] = (df['expected_points'] - df['total_points'])
        df['Points_minus_xP'] = (df['total_points'] - df['expected_points'])
        df['gameweek'] = GW
        return df
    
test = FplScraper()
loading_test = test.load_latest_gameweek()
print(loading_test.head())



