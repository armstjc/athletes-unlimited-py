import json
import time
#from urllib.request import urlopen

import pandas as pd
import requests
from tqdm import tqdm

from athetes_unlimited_py.utils import raise_html_status_code

############################################################################################################################################################################################################################################################
##
## Volleyball-only utilities
##
############################################################################################################################################################################################################################################################

def get_au_volleyball_season(season_id:int) -> int:
    """
    Given a season ID, `get_au_volleyball_season()` returns the proper season for the corresponding Athletes Unlimited volleyball season.

    Parameters
    ----------
    `season_id` (int, mandatory):
        The season ID you want a season for in Athletes Unlimited volleyball. 
        If there isn't a season for the inputted `season_id`, a `ValueError()` exception will be raised.
    
    Returns
    ----------
    The proper season corresponding to an Athletes Unlimited volleyball season ID.
    """
    season = 0
    
    if season_id == 3:
        season = 2021
        return season 
    elif season_id == 11:
        season = 2022
        return season
    elif season_id == 138:
        season = 2023
        return season 
    else:
        raise ValueError(f'[season] can only be 2021, 2022, or 2023 at this time for volleyball.\nYou entered :\n\t{season}')

def get_au_volleyball_season_id(season:int) -> int:
    """
    Given a season, `get_au_volleyball_season_id()` returns the proper season ID for the Athletes Unlimited volleyball season.

    Parameters
    ----------
    `season` (int, mandatory):
        The season you want a season ID for volleyball. 
        If there isn't a season ID for the inputted `season`, a `ValueError()` exception will be raised.
    
    Returns
    ----------
    The proper season ID corresponding to an Athletes Unlimited volleyball season.
    """
    seasonId = 0
    
    if season == 2021:
        seasonId = 3
        return seasonId 
    elif season == 2022:
        seasonId = 11
        return seasonId 
    elif season == 2023:
        seasonId = 138
        return seasonId 
    else:
        raise ValueError(f'[season] can only be 2021, 2022, or 2023 at this time for volleyball.\nYou entered :\n\t{season}')

############################################################################################################################################################################################################################################################
##
## Game Functions
##
############################################################################################################################################################################################################################################################

def get_au_volleyball_game_stats(season_id:int,game_num:int,get_team_stats=False,get_player_and_team_stats=False,rename_cols=False) -> pd.DataFrame():
    """
    Retrieves the player and/or team game stats for an Atheltes Unlimited (AU) volleyball game.

    Parameters
    ----------
    `season_id` (int, mandatory):
        The AU volleyball season ID you want a game from.
    
    `game_num` (int, mandatory):
        The game number you want player and/or team stats from.
        This is not the game ID!
        A `ValueError` will be raised if `game_num` is set to less than 1.
    
    `get_team_stats` (bool, optional) = False:
        Optional boolean argument. 
        If set to `True`, the pandas DataFrame returned by `get_volleyball_game_stats()` will only return team stats for that game, 
        and will not return player stats, unless `get_player_and_team_stats` is set to `True` if `get_team_stats` is set to `True`.
    
    `get_player_and_team_stats` (bool, optional) = False:

    `rename_cols` (bool, optional) = False:
        NOT IMPLEMENTED YET!
        `get_volleyball_game_stats()` will have no change in functionality at this time if `rename_cols` is set to `True`.
        

    Returns
    ----------
    A pandas DataFrame containing player and/or team stats for a given AU game within a given AU season ID.
    """

    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    player_stats_df = pd.DataFrame()
    team_stats_df = pd.DataFrame()
    row_df = pd.DataFrame()

    if game_num < 1:
        raise ValueError('`game_num` cannot be less than 0.')
    
    key = int(time.time()) # Yes, the key is literaly the int of the Epoch time at the time of the GET request.
    url = f"https://auprosports.com/proxy.php?request=/api/stats/volleyball/v1/{season_id}/by-game/{game_num}?statType=volleyball%26k={key}"

    response = requests.get(url,headers=headers)
    raise_html_status_code(response.status_code)
    
    json_data = json.loads(response.text)

    sport = json_data['metaSport']['sport']
    api_version = json_data['metaSport']['version']

    for i in tqdm(json_data['data']):
        row_df = pd.DataFrame({'sport':sport,'api_version':api_version},index=[0])
        
        ##############################################################################################################################
        ## Player/Team info
        ##############################################################################################################################
        row_df['season'] = get_au_volleyball_season(i['seasonId'])
        row_df['seasonId'] = i['seasonId']
        row_df['weekNumber'] = 0
        row_df['gameNumber'] = 0
        row_df['seasonType'] = ""

        row_df['playerId'] = i['playerId']
        row_df['uniformNumber'] = i['uniformNumber']
        row_df['uniformNumberDisplay'] = str(i['uniformNumberDisplay'])
        
        row_df['primaryPositionLk'] = i['primaryPositionLk']
        row_df['secondaryPositionLk'] = i['secondaryPositionLk']
        row_df['first_name'] = str(i['firstName']).replace('\u2019','\'')
        row_df['last_name'] = str(i['lastName']).replace('\u2019','\'')
        row_df['full_name'] = f"{i['firstName']} {i['lastName']}".replace('\u2019','\'')

        ##############################################################################################################################
        ## Player/Team stats
        ##############################################################################################################################
        row_df['player_id'] = i['stats'][0]['playerId']
        row_df['first_name'] = i['stats'][0]['firstName']
        row_df['last_name'] = i['stats'][0]['lastName']
        row_df['uniform_number'] = i['stats'][0]['uniformNumber']
        row_df['uniform_number_display'] = str(i['stats'][0]['uniformNumberDisplay'])
        row_df['primary_position_lk'] = i['stats'][0]['primaryPositionLk']
        row_df['secondary_position_lk'] = i['stats'][0]['secondaryPositionLk']
        row_df['team_id'] = i['stats'][0]['teamId']
        row_df['sets_played'] = i['stats'][0]['setsPlayed']
        row_df['player_id'] = i['stats'][0]['playerId']
        row_df['kills'] = i['stats'][0]['kills']
        row_df['kills_per_set'] = i['stats'][0]['killsPerSet']
        row_df['attack_errors'] = i['stats'][0]['attackErrors']
        row_df['attack_attempts'] = i['stats'][0]['attackAttempts']
        row_df['attack_percentage'] = i['stats'][0]['attackPercentage']
        row_df['assists'] = i['stats'][0]['assists']
        row_df['assists_per_set'] = i['stats'][0]['assistsPerSet']
        row_df['setting_errors'] = i['stats'][0]['settingErrors']
        row_df['service_errors'] = i['stats'][0]['serviceErrors']
        row_df['service_aces'] = i['stats'][0]['serviceAces']
        row_df['service_aces_per_set'] = i['stats'][0]['serviceAcesPerSet']
        row_df['total_reception_attempts'] = i['stats'][0]['totalReceptionAttempts']
        row_df['reception_errors'] = i['stats'][0]['receptionErrors']
        row_df['positive_reception_pct'] = i['stats'][0]['positiveReceptionPct']
        row_df['digs'] = i['stats'][0]['digs']
        row_df['digs_per_set'] = i['stats'][0]['digsPerSet']
        row_df['blocks'] = i['stats'][0]['blocks']
        row_df['blocks_per_set'] = i['stats'][0]['blocksPerSet']
        row_df['au_total_points'] = i['stats'][0]['auTotalPoints']
        row_df['week_number'] = i['stats'][0]['weekNumber']
        row_df['game_number'] = i['stats'][0]['gameNumber']
        row_df['season_type'] = i['stats'][0]['seasonType']


        ##############################################################################################################################
        ## Save the data to the correct DataFrame
        ##############################################################################################################################

        if i['type'] == "Team":
            team_stats_df = pd.concat([team_stats_df,row_df],ignore_index=True)
        else:
            player_stats_df = pd.concat([player_stats_df,row_df],ignore_index=True)

        row_df['type'] = i['type']
        row_df['teamId'] = i['teamId']

        if i['homeTeamFlg'] == True:
            row_df['homeTeamFlg'] = 1
        else:
            row_df['homeTeamFlg'] = 0

        del row_df

    ##############################################################################################################################
    ## Once we're done, return the correct dataframe.
    ##############################################################################################################################
    
    if get_player_and_team_stats == True:
        stats_df = pd.concat([player_stats_df,team_stats_df],ignore_index=True)
        del player_stats_df,team_stats_df
        return stats_df
    elif get_team_stats == True:        
        del player_stats_df
        return team_stats_df
    else:
        del team_stats_df
        return player_stats_df

def get_au_volleyball_pbp(season_id:int,game_id:int,return_participation_data=False) -> pd.DataFrame():
    """
    Retrieves the play-by-play (PBP) data for an Atheltes Unlimited (AU) volleyball game.

    Parameters
    ----------
    `season_id` (int, mandatory):
        The AU volleyball season ID you want a game from.
    
    `game_id` (int, mandatory):
        The AU volleyball game ID you want PBP data from.
    
    `return_participation_data` (bool, optional) = `False`:
        Optional argument. 
        If set to `True`, `get_au_volleyball_pbp()` will return a secondary pandas DataFrame
        containing roster information for this AU volleyball game.

    Returns
    ----------
    A pandas DataFrame containing PBP data for a given AU game ID within a given AU season ID.
    If `return_participation_data` is set to `True`, an additional pandas DataFrame containing roster data for this game will be returned as well.
    """

    # season_id = get_au_volleyball_season_id(season)
    season = get_au_volleyball_season(season_id)

    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    game_pbp_df = pd.DataFrame()
    roster_df = pd.DataFrame()
    row_df = pd.DataFrame()
        
    if game_id < 1:
        raise ValueError('`game_id` cannot be less than 0.')
    
    key = int(time.time()) # Yes, the key is literaly the int of the Epoch time at the time of the GET request.
    url = f"https://auprosports.com/proxy.php?request=/api/play-by-play/volleyball/v1/event/{season_id}/game/{game_id}?k={key}"

    response = requests.get(url,headers=headers)
    raise_html_status_code(response.status_code)
    

    json_data = json.loads(response.text)

    del headers, key
    #print(json_data)
    for i in tqdm(json_data['data'][0]['plays']):
        row_df = pd.DataFrame({'season':season,'game_id':game_id},index=[0])

        row_df['game_number'] = i['gameNumber']
        row_df['game_id'] = i['gameId']
        row_df['play_seq_num'] = i['playSeqno']
        row_df['narrative_formatted'] = i['narrativeFormatted']
        row_df['start_time'] = i['startTime']
        row_df['end_time'] = i['endTime']
        row_df['set_number'] = i['setNumber']
        row_df['set_status_lk'] = i['setStatusLk']
        row_df['rally_number'] = i['rallyNumber']
        row_df['play_code'] = i['playCode']
        row_df['play_text'] = i['playText']
        row_df['player_id'] = i['playerId']
        row_df['serve_ace'] = i['serveAce']
        row_df['serve_error'] = i['serveError']
        row_df['serve_continue'] = i['serveContinue']
        row_df['attack_kill'] = i['attackKill']
        row_df['attack_error'] = i['attackError']
        row_df['attack_continue'] = i['attackContinue']
        row_df['pass_good'] = i['passGood']
        row_df['pass_error'] = i['passError']
        row_df['pass_continue'] = i['passContinue']
        row_df['dig_dig'] = i['digDig']
        row_df['dig_continue'] = i['digContinue']
        row_df['block_continue'] = i['blockContinue']
        row_df['block_stuff'] = i['blockStuff']
        row_df['set_assist'] = i['setAssist']
        row_df['set_error'] = i['setError']
        row_df['set_continue'] = i['setContinue']
        row_df['home_team_id'] = i['homeTeamId']
        row_df['home_team_score'] = i['homeTeamScore']
        row_df['away_team_id'] = i['awayTeamId']
        row_df['away_team_Score'] = i['awayTeamScore']
        row_df['scoring_team_id'] = i['scoringTeamId']

        game_pbp_df = pd.concat([game_pbp_df,row_df])
        del row_df
    
    if return_participation_data == True:
        
        for i in json_data['data'][0]['competitors']:

            competitor_id = i['competitorId']
            competitor_color = i['color']
            competitor_name = i['name']
            
            for j in i['players']:
                row_df = pd.DataFrame({
                        'season':season,
                        'game_id':game_id,
                        'competitor_id':competitor_id,
                        'competitor_color':competitor_color,
                        'competitor_name':competitor_name
                    },
                    index=[0]
                )

                row_df['competitor_id'] = j['competitorId']
                row_df['player_id'] = j['playerId']
                row_df['captain_flag'] = j['captainFlg']
                row_df['display_name'] = j['displayName']
                row_df['first_name'] = j['firstName']
                row_df['last_name'] = j['lastName']
                row_df['current_roster_status_description'] = j['currentRosterStatus']['description']
                row_df['current_rosterStatus_comments'] = j['currentRosterStatus']['comments']
                row_df['current_rosterStatus_transactionType'] = j['currentRosterStatus']['transactionType']
                row_df['current_rosterStatus_rosterStatusLk'] = j['currentRosterStatus']['rosterStatusLk']
                row_df['is_voting_flg'] = j['isVotingFlg']
                row_df['can_be_voted_for_flg'] = j['canBeVotedForFlg']
                row_df['has_voted_flag'] = j['hasVotedFlg']
                row_df['uniform_number'] = str(j['uniformNumber'])
                row_df['is_nominated_flag'] = j['isNominatedFlg']
                row_df['nominated_flag'] = j['nominatedFlg']
                row_df['player_url'] = j['resourceUrl']
                row_df['image_url'] = j['imageResource']['imageUrl']

                roster_df = pd.concat([roster_df,row_df],ignore_index=True)
            del row_df

        del json_data
        return game_pbp_df,roster_df
    
    else:
        del json_data, roster_df
        return game_pbp_df

############################################################################################################################################################################################################################################################
##
## Season Functions
##
############################################################################################################################################################################################################################################################

def get_au_volleyball_season_pbp(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) volleyball season, get and parse all play-by-play (PBP) data for an AU volleyball season.
    
    Parameters
    ----------
    `season` (int, mandatory):
        The AU volleyball season you want PBP data from.

    Returns
    ----------
    A pandas DataFrame containing PBP data from a AU season.

    """
    season_pbp_df = pd.DataFrame()
    season_id = get_au_volleyball_season_id(season)
    url = "https://auprosports.com/proxy.php?request=api/seasons/volleyball/v1"
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

    response = requests.get(url,headers=headers)
    sport_json_data = json.loads(response.text)
    
    for i in sport_json_data['data']:
        #print(i)
        if i['seasonId'] == season_id:
            # len_game_ids = len(i['gameIds'])

            for j in tqdm(i['gameIds']):
                print(f'\nOn game ID {j} in {season}.')
                # try:
                #     game_df = get_volleyball_game_stats(season,j)
                # except:
                #     print(f'Couldn\'t parse game stats for game #{j}.')
                #     time.sleep(10)

                game_df = get_au_volleyball_pbp(season_id,j)

                season_pbp_df = pd.concat([season_pbp_df,game_df],ignore_index=True)
                del game_df

    return season_pbp_df

def get_au_volleyball_season_player_box(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) volleyball season, get and parse all box-score game stats for an AU volleyball season.
    This returns all player game stats, and does not return season stats or game averages.

    Parameters
    ----------
    `season` (int, mandatory):
        The AU volleyball season you want player box scores from.

    Returns
    ----------
    A pandas DataFrame containing player box score stats a AU season.

    """
    season_stats_df = pd.DataFrame()
    season_id = get_au_volleyball_season_id(season)
    url = "https://auprosports.com/proxy.php?request=api/seasons/volleyball/v1"
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

    response = requests.get(url,headers=headers)
    sport_json_data = json.loads(response.text)
    
    for i in sport_json_data['data']:
        #print(i)
        if i['seasonId'] == season_id:
            len_game_ids = len(i['gameIds'])

            for j in tqdm(range(1,len_game_ids+1)):
                print(f'\nOn game {j} of {len_game_ids+1} for {season}.')
                # try:
                #     game_df = get_volleyball_game_stats(season,j)
                # except:
                #     print(f'Couldn\'t parse game stats for game #{j}.')
                #     time.sleep(10)

                game_df = get_au_volleyball_game_stats(season_id,j)

                season_stats_df = pd.concat([season_stats_df,game_df],ignore_index=True)
                del game_df

    return season_stats_df

def get_au_volleyball_season_team_box(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) volleyball season, get and parse all box-score game stats for an AU volleyball season.
    This returns all player game stats, and does not return season stats or game averages.

    Parameters
    ----------
    `season` (int, mandatory):
        The AU volleyball season you want player box scores from.

    Returns
    ----------
    A pandas DataFrame containing player box score stats a AU season.

    """
    season_stats_df = pd.DataFrame()
    season_id = get_au_volleyball_season_id(season)
    url = "https://auprosports.com/proxy.php?request=api/seasons/volleyball/v1"
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

    response = requests.get(url,headers=headers)
    sport_json_data = json.loads(response.text)
    
    for i in sport_json_data['data']:
        #print(i)
        if i['seasonId'] == season_id:
            len_game_ids = len(i['gameIds'])

            for j in tqdm(range(1,len_game_ids+1)):
                print(f'\nOn game {j} of {len_game_ids+1} for {season}.')
                # try:
                #     game_df = get_volleyball_game_stats(season,j)
                # except:
                #     print(f'Couldn\'t parse game stats for game #{j}.')
                #     time.sleep(10)

                game_df = get_au_volleyball_game_stats(season_id,j,get_team_stats=True)

                season_stats_df = pd.concat([season_stats_df,game_df],ignore_index=True)
                del game_df

    return season_stats_df

