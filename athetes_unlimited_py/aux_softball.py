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

    return season_stats_df

