import json
import time
from urllib.request import urlopen

import pandas as pd
import requests
from tqdm import tqdm

from athetes_unlimited_py.softball import get_au_softball_game_stats, get_au_softball_pbp
from athetes_unlimited_py.utils import raise_html_status_code


def get_aux_softball_season_id(season:int) -> int:
    """
    Given a season, `get_au_softball_season_id()` returns the proper season ID for the Athletes Unlimited softball season.

    Parameters
    ----------
    `season` (int, mandatory):
        The season you want a season ID for softball. 
        If there isn't a season ID for the inputted `season`, a `ValueError()` exception will be raised.
    
    Returns
    ----------
    The proper season ID corresponding to an Athletes Unlimited softball season.
    """
    seasonId = 0
    
    if season == 2022:
        seasonId = 39
        return seasonId 
    elif season == 2023:
        seasonId = 106
        return seasonId 
    else:
        raise ValueError(f'[season] can only be 2022 or 2023 at this time for softball.\nYou entered :\n\t{season}')


############################################################################################################################################################################################################################################################
##
## Season Functions
##
############################################################################################################################################################################################################################################################

def get_aux_softball_season_pbp(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) softball season, get and parse all play-by-play (PBP) data for an AU softball season.
    
    Parameters
    ----------
    `season` (int, mandatory):
        The AU softball season you want PBP data from.

    Returns
    ----------
    A pandas DataFrame containing PBP data from a AU season.

    """
    season_pbp_df = pd.DataFrame()
    seasonId = get_aux_softball_season_id(season)
    url = "https://auprosports.com/proxy.php?request=api/seasons/softball/v1"
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

    response = requests.get(url,headers=headers)
    sport_json_data = json.loads(response.text)
    
    for i in sport_json_data['data']:
        #print(i)
        if i['seasonId'] == seasonId:
            len_game_ids = len(i['gameIds'])

            for j in tqdm(i['gameIds']):
                print(f'\nOn game {j} of {len_game_ids+1} for {season}.')
                # try:
                #     game_df = get_softball_game_stats(season,j)
                # except:
                #     print(f'Couldn\'t parse game stats for game #{j}.')
                #     time.sleep(10)

                game_df = get_au_softball_pbp(seasonId,j)

                season_pbp_df = pd.concat([season_pbp_df,game_df],ignore_index=True)
                del game_df

    return season_pbp_df

def get_aux_softball_season_player_box(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) softball season, get and parse all box-score game stats for an AU softball season.
    This returns all player game stats, and does not return season stats or game averages.

    Parameters
    ----------
    `season` (int, mandatory):
        The AU softball season you want player box scores from.

    Returns
    ----------
    A pandas DataFrame containing player box score stats a AU season.

    """
    season_stats_df = pd.DataFrame()
    seasonId = get_aux_softball_season_id(season)
    url = "https://auprosports.com/proxy.php?request=api/seasons/softball/v1"
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

    response = requests.get(url,headers=headers)
    sport_json_data = json.loads(response.text)
    
    for i in sport_json_data['data']:
        #print(i)
        if i['seasonId'] == seasonId:
            len_game_ids = len(i['gameIds'])

            for j in tqdm(range(1,len_game_ids+1)):
                print(f'\nOn game {j} of {len_game_ids+1} for {season}.')
                # try:
                #     game_df = get_softball_game_stats(season,j)
                # except:
                #     print(f'Couldn\'t parse game stats for game #{j}.')
                #     time.sleep(10)

                game_df = get_au_softball_game_stats(seasonId,j,get_team_stats=False)

                season_stats_df = pd.concat([season_stats_df,game_df],ignore_index=True)
                del game_df

    season_stats_df['sport'] = 'aux_softball'
    return season_stats_df

def get_aux_softball_season_team_box(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) softball season, get and parse all box-score game stats for an AU softball season.
    This returns all player game stats, and does not return season stats or game averages.

    Parameters
    ----------
    `season` (int, mandatory):
        The AU softball season you want player box scores from.

    Returns
    ----------
    A pandas DataFrame containing player box score stats a AU season.

    """
    season_stats_df = pd.DataFrame()
    seasonId = get_aux_softball_season_id(season)
    url = "https://auprosports.com/proxy.php?request=api/seasons/softball/v1"
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

    response = requests.get(url,headers=headers)
    sport_json_data = json.loads(response.text)
    
    for i in sport_json_data['data']:
        #print(i)
        if i['seasonId'] == seasonId:
            len_game_ids = len(i['gameIds'])

            for j in tqdm(range(1,len_game_ids+1)):
                print(f'\nOn game {j} of {len_game_ids+1} for {season}.')
                # try:
                #     game_df = get_softball_game_stats(season,j)
                # except:
                #     print(f'Couldn\'t parse game stats for game #{j}.')
                #     time.sleep(10)

                game_df = get_au_softball_game_stats(seasonId,j,get_team_stats=True)

                season_stats_df = pd.concat([season_stats_df,game_df],ignore_index=True)
                del game_df

    season_stats_df['sport'] = 'aux_softball'

    return season_stats_df

############################################################################################################################################################################################################################################################
##
## Season Stats
##
############################################################################################################################################################################################################################################################

def get_aux_softball_season_player_stats(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) softball season, get all season player stats for an AU softball season.

    Parameters
    ----------
    `season` (int, mandatory):
        The AU softball season you want season player stats from.

    Returns
    ----------
    A pandas DataFrame containing season player stats a AU season.

    """
    game_stats_df = get_aux_softball_season_player_box(season)
    # ['sport', 'api_version', 'season', 'seasonId', 'weekNumber', 
    #    'gameNumber', 'seasonType', 'playerId', 'uniformNumber',    
    #    'uniformNumberDisplay', 'primaryPositionLk', 'secondaryPositionLk',
    #    'first_name', 'last_name', 'full_name', 'week', 'game_num', 
    #    'season_type', 'G', 'GS', 'batting_PA', 'batting_AB', 'batting_R',
    #    'batting_H', 'batting_2B', 'batting_3B', 'batting_HR', 'batting_RBI',
    #    'batting_BB', 'batting_HBP', 'batting_K', 'batting_SB', 'batting_SBA',
    #    'batting_CS', 'batting_BA', 'batting_OBP', 'batting_SLG', 'batting_TB',
    #    'batting_SF', 'batting_SH', 'AU_POINTS', 'pitching_W', 'pitching_L',
    #    'pitching_ERA', 'pitching_SHO', 'pitching_CG', 'pitching_SV',
    #    'pitching_IP_str', 'pitching_IP', 'pitching_H', 'pitching_R',
    #    'pitching_ER', 'pitching_HR', 'pitching_BB', 'pitching_SO',
    #    'pitching_HBP', 'pitching_WP', 'pitching_WHIP', 'pitching_H9',
    #    'pitching_HR9', 'pitching_BB9', 'pitching_SO9', 'pitching_SO/BB',
    #    'pitching_RA9', 'pitching_PI', 'pitching_PI_balls',
    #    'pitching_PI_strikes', 'fielding_position', 'fielding_IP_str',
    #    'fielding_IP', 'fielding_PO', 'fielding_A', 'fielding_E', 'fielding_DP',
    #    'fielding_FLD%', 'fielding_CS', 'fielding_CS%', 'fielding_TC',
    #    'fielding_CH', 'fielding_RF/9']

    finished_df = game_stats_df.groupby(['sport', 'season', 'seasonId', 'playerId', 
        'first_name', 'last_name', 'full_name'],as_index=False)[[
        'G', 'GS', 'AU_POINTS',
        'batting_PA', 'batting_AB', 'batting_R',
        'batting_H', 'batting_2B', 'batting_3B', 'batting_HR', 'batting_RBI',
        'batting_BB', 'batting_HBP', 'batting_K', 'batting_SB', 'batting_SBA',
        'batting_CS', 'batting_TB', 'batting_SF', 'batting_SH', 
        'pitching_W', 'pitching_L', 'pitching_SHO', 'pitching_CG', 'pitching_QS',
        'pitching_SV', 'pitching_IP', 
        'pitching_H', 'pitching_R', 'pitching_ER', 'pitching_HR', 'pitching_BB', 
        'pitching_SO', 'pitching_HBP', 'pitching_WP', 'pitching_PI', 'pitching_PI_balls',
        'pitching_PI_strikes',
        'fielding_IP', 'fielding_PO', 'fielding_A', 'fielding_E', 'fielding_DP',
        'fielding_CS', 'fielding_TC'
    ]].sum()

    finished_df[['G', 'GS', 'AU_POINTS','batting_PA', 'batting_AB', 'batting_R','batting_H', 'batting_2B', 'batting_3B', 'batting_HR', 'batting_RBI','batting_BB', 'batting_HBP', 'batting_K', 'batting_SB', 'batting_SBA','batting_CS', 'batting_TB', 'batting_SF', 'batting_SH', 'pitching_W', 'pitching_L', 'pitching_SHO', 'pitching_CG', 'pitching_QS','pitching_SV', 'pitching_H', 'pitching_R', 'pitching_ER', 'pitching_HR', 'pitching_BB', 'pitching_SO', 'pitching_HBP', 'pitching_WP', 'pitching_PI', 'pitching_PI_balls','pitching_PI_strikes','fielding_IP', 'fielding_PO', 'fielding_A', 'fielding_E', 'fielding_DP','fielding_CS', 'fielding_TC']] = finished_df[['G', 'GS', 'AU_POINTS','batting_PA', 'batting_AB', 'batting_R','batting_H', 'batting_2B', 'batting_3B', 'batting_HR', 'batting_RBI','batting_BB', 'batting_HBP', 'batting_K', 'batting_SB', 'batting_SBA','batting_CS', 'batting_TB', 'batting_SF', 'batting_SH', 'pitching_W', 'pitching_L', 'pitching_SHO', 'pitching_CG', 'pitching_QS','pitching_SV','pitching_H', 'pitching_R', 'pitching_ER', 'pitching_HR', 'pitching_BB', 'pitching_SO', 'pitching_HBP', 'pitching_WP', 'pitching_PI', 'pitching_PI_balls','pitching_PI_strikes','fielding_IP', 'fielding_PO', 'fielding_A', 'fielding_E', 'fielding_DP','fielding_CS', 'fielding_TC']].astype('int')
    finished_df['pitching_IP'] = finished_df['pitching_IP'].astype('float')
    ## Batting
    finished_df.loc[finished_df['batting_AB'] >= 1, 'batting_BA'] = finished_df['batting_H'] / finished_df['batting_AB']
    finished_df['batting_BA'] = finished_df['batting_BA'].round(3)

    finished_df.loc[finished_df['batting_AB'] > 0,'batting_OBP'] = (finished_df['batting_H'] + finished_df['batting_BB'] + finished_df['batting_HBP']) / (finished_df['batting_AB'] + finished_df['batting_BB'] + finished_df['batting_HBP'] + finished_df['batting_SF'])
    finished_df['batting_OBP'] = finished_df['batting_OBP'].round(3)

    finished_df.loc[finished_df['batting_AB'] > 0,'batting_SLG'] = finished_df['batting_TB'] / finished_df['batting_AB']
    finished_df['batting_SLG'] = finished_df['batting_SLG'].round(3)

    finished_df.loc[finished_df['batting_AB'] > 0,'batting_OPS'] = finished_df['batting_OBP'] + finished_df['batting_SLG']
    finished_df['batting_OPS'] = finished_df['batting_OPS'].round(3)

    finished_df['batting_OPS+'] = None

    finished_df.loc[finished_df['batting_AB'] > 0,'batting_SecA'] = (finished_df['batting_BB'] + (finished_df['batting_TB'] - finished_df['batting_H']) + (finished_df['batting_SB'] - finished_df['batting_CS'])) / finished_df['batting_AB']
    finished_df['batting_SecA'] = finished_df['batting_SecA'].round(3)

    finished_df.loc[finished_df['batting_PA'] > 0,'batting_BB%'] = finished_df['batting_BB'] / finished_df['batting_PA']
    finished_df['batting_BB%'] = finished_df['batting_BB%'].round(3)

    finished_df.loc[finished_df['batting_PA'] > 0,'batting_K%'] = finished_df['batting_K'] / finished_df['batting_PA']
    finished_df['batting_K%'] = finished_df['batting_K%'].round(3)
    
    finished_df.loc[finished_df['batting_AB'] > 0,'batting_ISO'] = (finished_df['batting_TB'] - finished_df['batting_H']) / finished_df['batting_AB']
    finished_df['batting_ISO'] = finished_df['batting_ISO'].round(3)
    
    finished_df.loc[finished_df['batting_AB'] > 0,'batting_BABIP'] = (finished_df['batting_H'] + finished_df['batting_HR']) / (finished_df['batting_AB'] - finished_df['batting_K'] - finished_df['batting_HR'] + finished_df['batting_SF'])
    finished_df['batting_BABIP'] = finished_df['batting_BABIP'].round(3)

    finished_df.loc[(finished_df['batting_SB'] > 0) | (finished_df['batting_HR'] > 0),'batting_PSN'] = (2 * finished_df['batting_HR'] * finished_df['batting_SB']) / (finished_df['batting_HR'] * finished_df['batting_SB'])
    finished_df['batting_PSN'] = finished_df['batting_PSN'].round(3)

    ## Pitching
    finished_df['pitching_ERA'] = 9 * (finished_df['pitching_ER'] / finished_df['pitching_IP'])
    finished_df['pitching_ERA'] = finished_df['pitching_ERA'].round(3)

    finished_df['pitching_ERA+'] = None
    finished_df['pitching_FIP'] = None
    finished_df['pitching_FIP-'] = None
    finished_df['pitching_WHIP'] = (finished_df['pitching_BB'] + finished_df['pitching_H']) / finished_df['pitching_IP']
    finished_df['pitching_WHIP'] = finished_df['pitching_WHIP'].round(3)

    finished_df['pitching_H9'] = (9 * finished_df['pitching_H']) / finished_df['pitching_IP']
    finished_df['pitching_H9'] = finished_df['pitching_H9'].round(3)

    finished_df['pitching_HR9'] = (9 * finished_df['pitching_HR']) / finished_df['pitching_IP']
    finished_df['pitching_HR9'] = finished_df['pitching_HR9'].round(3)

    finished_df['pitching_BB9'] = (9 * finished_df['pitching_BB']) / finished_df['pitching_IP']
    finished_df['pitching_BB9'] = finished_df['pitching_BB9'].round(3)

    finished_df['pitching_SO9'] = (9 * finished_df['pitching_SO']) / finished_df['pitching_IP']
    finished_df['pitching_SO9'] = finished_df['pitching_SO9'].round(3)

    finished_df['pitching_SO/BB'] = finished_df['pitching_SO'] / finished_df['pitching_BB']
    finished_df['pitching_SO/BB'] = finished_df['pitching_SO/BB'].round(3)

    finished_df['pitching_RA9'] = 9 * (finished_df['pitching_R'] / finished_df['pitching_IP'])
    finished_df['pitching_RA9'] = finished_df['pitching_RA9'].round(3)
    
    ## Fielding
    finished_df['fielding_FLD%'] = (finished_df['fielding_PO'] + finished_df['fielding_A']) / (finished_df['fielding_PO'] + finished_df['fielding_A'] + finished_df['fielding_E'])
    finished_df['fielding_FLD%'] = finished_df['fielding_FLD%'].round(3)

    finished_df['fielding_CH'] = finished_df['fielding_PO'] + finished_df['fielding_A'] + finished_df['fielding_E']
    finished_df['fielding_CH'] = finished_df['fielding_CH'].round(3)

    #finished_df['fielding_CS%'] = 0
    #finished_df['fielding_CS%'] = finished_df['fielding_CS%'].round(3)

    finished_df['fielding_RF/9'] = (9 * (finished_df['fielding_PO'] + finished_df['fielding_A'])) / finished_df['fielding_IP']
    finished_df['fielding_RF/9'] = finished_df['fielding_RF/9'].round(3)

    # finished_df.to_csv('test.csv')
    # print(finished_df)
    # print(game_stats_df.columns)
    return finished_df

def get_aux_softball_season_team_stats(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) softball season, get all season team stats for an AU softball season.

    Parameters
    ----------
    `season` (int, mandatory):
        The AU softball season you want season player stats from.

    Returns
    ----------
    A pandas DataFrame containing season player stats a AU season.

    """
    game_stats_df = get_aux_softball_season_player_box(season)
    # ['sport', 'api_version', 'season', 'seasonId', 'weekNumber', 
    #    'gameNumber', 'seasonType', 'playerId', 'uniformNumber',    
    #    'uniformNumberDisplay', 'primaryPositionLk', 'secondaryPositionLk',
    #    'first_name', 'last_name', 'full_name', 'week', 'game_num', 
    #    'season_type', 'G', 'GS', 'batting_PA', 'batting_AB', 'batting_R',
    #    'batting_H', 'batting_2B', 'batting_3B', 'batting_HR', 'batting_RBI',
    #    'batting_BB', 'batting_HBP', 'batting_K', 'batting_SB', 'batting_SBA',
    #    'batting_CS', 'batting_BA', 'batting_OBP', 'batting_SLG', 'batting_TB',
    #    'batting_SF', 'batting_SH', 'AU_POINTS', 'pitching_W', 'pitching_L',
    #    'pitching_ERA', 'pitching_SHO', 'pitching_CG', 'pitching_SV',
    #    'pitching_IP_str', 'pitching_IP', 'pitching_H', 'pitching_R',
    #    'pitching_ER', 'pitching_HR', 'pitching_BB', 'pitching_SO',
    #    'pitching_HBP', 'pitching_WP', 'pitching_WHIP', 'pitching_H9',
    #    'pitching_HR9', 'pitching_BB9', 'pitching_SO9', 'pitching_SO/BB',
    #    'pitching_RA9', 'pitching_PI', 'pitching_PI_balls',
    #    'pitching_PI_strikes', 'fielding_position', 'fielding_IP_str',
    #    'fielding_IP', 'fielding_PO', 'fielding_A', 'fielding_E', 'fielding_DP',
    #    'fielding_FLD%', 'fielding_CS', 'fielding_CS%', 'fielding_TC',
    #    'fielding_CH', 'fielding_RF/9']

    finished_df = game_stats_df.groupby(['sport', 'api_version', 'season', 'seasonId','teamId'],as_index=False)[[
        'G', 'AU_POINTS',
        'batting_PA', 'batting_AB', 'batting_R',
        'batting_H', 'batting_2B', 'batting_3B', 'batting_HR', 'batting_RBI',
        'batting_BB', 'batting_HBP', 'batting_K', 'batting_SB', 'batting_SBA',
        'batting_CS', 'batting_TB', 'batting_SF', 'batting_SH', 
        'pitching_W', 'pitching_L', 'pitching_SHO', 'pitching_CG', 'pitching_QS',
        'pitching_SV', 'pitching_IP', 
        'pitching_H', 'pitching_R', 'pitching_ER', 'pitching_HR', 'pitching_BB', 
        'pitching_SO', 'pitching_HBP', 'pitching_WP', 'pitching_PI', 'pitching_PI_balls',
        'pitching_PI_strikes',
        'fielding_IP', 'fielding_PO', 'fielding_A', 'fielding_E', 'fielding_DP',
        'fielding_CS', 'fielding_TC'
    ]].sum()

    finished_df[['G',  'AU_POINTS','batting_PA', 'batting_AB', 'batting_R','batting_H', 'batting_2B', 'batting_3B', 'batting_HR', 'batting_RBI','batting_BB', 'batting_HBP', 'batting_K', 'batting_SB', 'batting_SBA','batting_CS', 'batting_TB', 'batting_SF', 'batting_SH', 'pitching_W', 'pitching_L', 'pitching_SHO', 'pitching_CG', 'pitching_QS','pitching_SV', 'pitching_H', 'pitching_R', 'pitching_ER', 'pitching_HR', 'pitching_BB', 'pitching_SO', 'pitching_HBP', 'pitching_WP', 'pitching_PI', 'pitching_PI_balls','pitching_PI_strikes','fielding_IP', 'fielding_PO', 'fielding_A', 'fielding_E', 'fielding_DP','fielding_CS', 'fielding_TC']] = finished_df[['G', 'AU_POINTS','batting_PA', 'batting_AB', 'batting_R','batting_H', 'batting_2B', 'batting_3B', 'batting_HR', 'batting_RBI','batting_BB', 'batting_HBP', 'batting_K', 'batting_SB', 'batting_SBA','batting_CS', 'batting_TB', 'batting_SF', 'batting_SH', 'pitching_W', 'pitching_L', 'pitching_SHO', 'pitching_CG', 'pitching_QS','pitching_SV','pitching_H', 'pitching_R', 'pitching_ER', 'pitching_HR', 'pitching_BB', 'pitching_SO', 'pitching_HBP', 'pitching_WP', 'pitching_PI', 'pitching_PI_balls','pitching_PI_strikes','fielding_IP', 'fielding_PO', 'fielding_A', 'fielding_E', 'fielding_DP','fielding_CS', 'fielding_TC']].astype('int')
    finished_df['pitching_IP'] = finished_df['pitching_IP'].astype('float')
    ## Batting
    finished_df.loc[finished_df['batting_AB'] >= 1, 'batting_BA'] = finished_df['batting_H'] / finished_df['batting_AB']
    finished_df['batting_BA'] = finished_df['batting_BA'].round(3)

    finished_df.loc[finished_df['batting_AB'] > 0,'batting_OBP'] = (finished_df['batting_H'] + finished_df['batting_BB'] + finished_df['batting_HBP']) / (finished_df['batting_AB'] + finished_df['batting_BB'] + finished_df['batting_HBP'] + finished_df['batting_SF'])
    finished_df['batting_OBP'] = finished_df['batting_OBP'].round(3)

    finished_df.loc[finished_df['batting_AB'] > 0,'batting_SLG'] = finished_df['batting_TB'] / finished_df['batting_AB']
    finished_df['batting_SLG'] = finished_df['batting_SLG'].round(3)

    finished_df.loc[finished_df['batting_AB'] > 0,'batting_OPS'] = finished_df['batting_OBP'] + finished_df['batting_SLG']
    finished_df['batting_OPS'] = finished_df['batting_OPS'].round(3)

    finished_df['batting_OPS+'] = None

    finished_df.loc[finished_df['batting_AB'] > 0,'batting_SecA'] = (finished_df['batting_BB'] + (finished_df['batting_TB'] - finished_df['batting_H']) + (finished_df['batting_SB'] - finished_df['batting_CS'])) / finished_df['batting_AB']
    finished_df['batting_SecA'] = finished_df['batting_SecA'].round(3)

    finished_df.loc[finished_df['batting_PA'] > 0,'batting_BB%'] = finished_df['batting_BB'] / finished_df['batting_PA']
    finished_df['batting_BB%'] = finished_df['batting_BB%'].round(3)

    finished_df.loc[finished_df['batting_PA'] > 0,'batting_K%'] = finished_df['batting_K'] / finished_df['batting_PA']
    finished_df['batting_K%'] = finished_df['batting_K%'].round(3)
    
    finished_df.loc[finished_df['batting_AB'] > 0,'batting_ISO'] = (finished_df['batting_TB'] - finished_df['batting_H']) / finished_df['batting_AB']
    finished_df['batting_ISO'] = finished_df['batting_ISO'].round(3)
    
    finished_df.loc[finished_df['batting_AB'] > 0,'batting_BABIP'] = (finished_df['batting_H'] + finished_df['batting_HR']) / (finished_df['batting_AB'] - finished_df['batting_K'] - finished_df['batting_HR'] + finished_df['batting_SF'])
    finished_df['batting_BABIP'] = finished_df['batting_BABIP'].round(3)

    finished_df.loc[(finished_df['batting_SB'] > 0) | (finished_df['batting_HR'] > 0),'batting_PSN'] = (2 * finished_df['batting_HR'] * finished_df['batting_SB']) / (finished_df['batting_HR'] * finished_df['batting_SB'])
    finished_df['batting_PSN'] = finished_df['batting_PSN'].round(3)

    ## Pitching
    finished_df['pitching_ERA'] = 9 * (finished_df['pitching_ER'] / finished_df['pitching_IP'])
    finished_df['pitching_ERA'] = finished_df['pitching_ERA'].round(3)

    finished_df['pitching_ERA+'] = None
    finished_df['pitching_FIP'] = None
    finished_df['pitching_FIP-'] = None
    finished_df['pitching_WHIP'] = (finished_df['pitching_BB'] + finished_df['pitching_H']) / finished_df['pitching_IP']
    finished_df['pitching_WHIP'] = finished_df['pitching_WHIP'].round(3)

    finished_df['pitching_H9'] = (9 * finished_df['pitching_H']) / finished_df['pitching_IP']
    finished_df['pitching_H9'] = finished_df['pitching_H9'].round(3)

    finished_df['pitching_HR9'] = (9 * finished_df['pitching_HR']) / finished_df['pitching_IP']
    finished_df['pitching_HR9'] = finished_df['pitching_HR9'].round(3)

    finished_df['pitching_BB9'] = (9 * finished_df['pitching_BB']) / finished_df['pitching_IP']
    finished_df['pitching_BB9'] = finished_df['pitching_BB9'].round(3)

    finished_df['pitching_SO9'] = (9 * finished_df['pitching_SO']) / finished_df['pitching_IP']
    finished_df['pitching_SO9'] = finished_df['pitching_SO9'].round(3)

    finished_df['pitching_SO/BB'] = finished_df['pitching_SO'] / finished_df['pitching_BB']
    finished_df['pitching_SO/BB'] = finished_df['pitching_SO/BB'].round(3)

    finished_df['pitching_RA9'] = 9 * (finished_df['pitching_R'] / finished_df['pitching_IP'])
    finished_df['pitching_RA9'] = finished_df['pitching_RA9'].round(3)
    
    ## Fielding
    finished_df['fielding_FLD%'] = (finished_df['fielding_PO'] + finished_df['fielding_A']) / (finished_df['fielding_PO'] + finished_df['fielding_A'] + finished_df['fielding_E'])
    finished_df['fielding_FLD%'] = finished_df['fielding_FLD%'].round(3)

    finished_df['fielding_CH'] = finished_df['fielding_PO'] + finished_df['fielding_A'] + finished_df['fielding_E']
    finished_df['fielding_CH'] = finished_df['fielding_CH'].round(3)

    #finished_df['fielding_CS%'] = 0
    #finished_df['fielding_CS%'] = finished_df['fielding_CS%'].round(3)

    finished_df['fielding_RF/9'] = (9 * (finished_df['fielding_PO'] + finished_df['fielding_A'])) / finished_df['fielding_IP']
    finished_df['fielding_RF/9'] = finished_df['fielding_RF/9'].round(3)

    # finished_df.to_csv('test.csv')
    # print(finished_df)
    # print(game_stats_df.columns)
    return finished_df
