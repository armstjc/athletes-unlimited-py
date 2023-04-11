import json
import time
#from urllib.request import urlopen

import pandas as pd
import requests
from tqdm import tqdm

from athetes_unlimited_py.utils import raise_html_status_code

############################################################################################################################################################################################################################################################
##
## Lacrosse-only utilities
##
############################################################################################################################################################################################################################################################

def get_au_lacrosse_season(season_id:int) -> int:
    """
    Given a season ID, `get_au_lacrosse_season()` returns the proper season for the corresponding Athletes Unlimited lacrosse season.

    Parameters
    ----------
    `season_id` (int, mandatory):
        The season ID you want a season for in Athletes Unlimited lacrosse. 
        If there isn't a season for the inputted `season_id`, a `ValueError()` exception will be raised.
    
    Returns
    ----------
    The proper season corresponding to an Athletes Unlimited lacrosse season ID.
    """
    season = 0
    if season_id == 5:
        season= 2021
        return season
    elif season_id == 17:
        season= 2022
        return season
    elif season_id == 105:
        season = 2023
        return season 
    else:
        raise ValueError(f'[season_id] can only be for the 2021, 2022, or 2023 lacrosse seasons at this time.\nYou entered :\n\t{season}')

def get_au_lacrosse_season_id(season:int) -> int:
    """
    Given a season, `get_au_lacrosse_season_id()` returns the proper season ID for the Athletes Unlimited lacrosse season.

    Parameters
    ----------
    `season` (int, mandatory):
        The season you want a season ID for lacrosse. 
        If there isn't a season ID for the inputted `season`, a `ValueError()` exception will be raised.
    
    Returns
    ----------
    The proper season ID corresponding to an Athletes Unlimited lacrosse season.
    """
    seasonId = 0
    
    if season == 2021:
        seasonId = 5
        return seasonId
    elif season == 2022:
        seasonId = 17
        return seasonId 
    elif season == 2023:
        seasonId = 105
        return seasonId 
    else:
        raise ValueError(f'[season] can only be 2021, 2022, or 2023 at this time for lacrosse.\nYou entered :\n\t{season}')

############################################################################################################################################################################################################################################################
##
## Game Functions
##
############################################################################################################################################################################################################################################################

def get_au_lacrosse_game_stats(season_id:int,game_num:int,get_team_stats=False,get_player_and_team_stats=False,rename_cols=False) -> pd.DataFrame():
    """
    Retrieves the player and/or team game stats for an Atheltes Unlimited (AU) lacrosse game.

    Parameters
    ----------
    `season_id` (int, mandatory):
        The AU lacrosse season ID you want a game from.
    
    `game_num` (int, mandatory):
        The game number you want player and/or team stats from.
        This is not the game ID!
        A `ValueError` will be raised if `game_num` is set to less than 1.
    
    `get_team_stats` (bool, optional) = False:
        Optional boolean argument. 
        If set to `True`, the pandas DataFrame returned by `get_lacrosse_game_stats()` will only return team stats for that game, 
        and will not return player stats, unless `get_player_and_team_stats` is set to `True` if `get_team_stats` is set to `True`.
    
    `get_player_and_team_stats` (bool, optional) = False:

    `rename_cols` (bool, optional) = False:
        NOT IMPLEMENTED YET!
        `get_lacrosse_game_stats()` will have no change in functionality at this time if `rename_cols` is set to `True`.
        

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
    url = f"https://auprosports.com/proxy.php?request=/api/stats/lacrosse/v1/{season_id}/by-game/{game_num}?statType=lacrosse_player%26statType=lacrosse_goalie%26k={key}"
    
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
        row_df['season'] = get_au_lacrosse_season(i['seasonId'])
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
        row_df['periodsPlayed'] = i['playerStats'][0]['periodsPlayed']
        row_df['goals'] = i['playerStats'][0]['goals']
        row_df['assists'] = i['playerStats'][0]['assists']
        row_df['points'] = i['playerStats'][0]['points']
        row_df['shots'] = i['playerStats'][0]['shots']
        row_df['turnovers'] = i['playerStats'][0]['turnovers']
        row_df['causedTurnovers'] = i['playerStats'][0]['causedTurnovers']
        row_df['groundballs'] = i['playerStats'][0]['groundballs']
        row_df['shotPct'] = i['playerStats'][0]['shotPct']
        row_df['twoPointGoals'] = i['playerStats'][0]['twoPointGoals']
        row_df['drawControls'] = i['playerStats'][0]['drawControls']
        row_df['sogPct'] = i['playerStats'][0]['sogPct']
        row_df['shotsSaved'] = i['playerStats'][0]['shotsSaved']
        row_df['shotsOnGoal'] = i['playerStats'][0]['shotsOnGoal']
        row_df['yellowCards'] = i['playerStats'][0]['yellowCards']
        row_df['redCards'] = i['playerStats'][0]['redCards']
        row_df['shotClockViolationsCommitted'] = i['playerStats'][0]['shotClockViolationsCommitted']
        row_df['shotClockViolationsDrawn'] = i['playerStats'][0]['shotClockViolationsDrawn']
        row_df['auTotalPoints'] = i['playerStats'][0]['auTotalPoints']
        row_df['weekNumber'] = i['playerStats'][0]['weekNumber']
        row_df['gameNumber'] = i['playerStats'][0]['gameNumber']
        row_df['seasonType'] = i['playerStats'][0]['seasonType']

        ##############################################################################################################################
        ## Golie stats
        ##############################################################################################################################
        row_df['goalie_gamesPlayed'] = i['goalieStats'][0]['gamesPlayed']
        row_df['goalie_gamesStarted'] = i['goalieStats'][0]['gamesStarted']
        row_df['goalie_goalsAgainst'] = i['goalieStats'][0]['goalsAgainst']
        row_df['goalie_saves'] = i['goalieStats'][0]['saves']
        row_df['goalie_savePct'] = i['goalieStats'][0]['savePct']
        row_df['goalie_shotsFaced'] = i['goalieStats'][0]['shotsFaced']
        row_df['yellowCards'] = i['goalieStats'][0]['yellowCards']
        row_df['redCards'] = i['goalieStats'][0]['redCards']
        row_df['goalie_shotClockViolationsCommitted'] = i['goalieStats'][0]['shotClockViolationsCommitted']
        row_df['goalie_shotClockViolationsDrawn'] = i['goalieStats'][0]['shotClockViolationsDrawn']

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

def get_au_lacrosse_pbp(season_id:int,game_id:int,return_participation_data=False) -> pd.DataFrame():
    """
    Retrieves the play-by-play (PBP) data for an Atheltes Unlimited (AU) lacrosse game.

    Parameters
    ----------
    `season_id` (int, mandatory):
        The AU lacrosse season ID you want a game from.
    
    `game_id` (int, mandatory):
        The AU lacrosse game ID you want PBP data from.
    
    `return_participation_data` (bool, optional) = `False`:
        Optional argument. 
        If set to `True`, `get_au_lacrosse_pbp()` will return a secondary pandas DataFrame
        containing roster information for this AU lacrosse game.

    Returns
    ----------
    A pandas DataFrame containing PBP data for a given AU game ID within a given AU season ID.
    If `return_participation_data` is set to `True`, an additional pandas DataFrame containing roster data for this game will be returned as well.
    """

    # season_id = get_au_lacrosse_season_id(season)
    season = get_au_lacrosse_season(season_id)

    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    game_pbp_df = pd.DataFrame()
    roster_df = pd.DataFrame()
    row_df = pd.DataFrame()
        
    if game_id < 1:
        raise ValueError('`game_id` cannot be less than 0.')
    
    key = int(time.time()) # Yes, the key is literaly the int of the Epoch time at the time of the GET request.
    url = f"https://auprosports.com/proxy.php?request=/api/play-by-play/lacrosse/v1/event/{season_id}/game/{game_id}?k={key}"

    response = requests.get(url,headers=headers)
    raise_html_status_code(response.status_code)
    

    json_data = json.loads(response.text)

    del headers, key
    #print(json_data)
    for i in tqdm(json_data['data'][0]['plays']):
        row_df = pd.DataFrame({'season':season,'game_id':game_id},index=[0])

        row_df['game_number'] = i['gameNumber']
        row_df['game_report_id'] = i['gameReportId']
        row_df['play_seq_num'] = i['playSeqno']
        row_df['action'] = i['action']
        row_df['play_desc'] = i['text']
        row_df['player_id'] = i['playerId']
        row_df['team_id'] = i['teamId']
        row_df['period'] = i['period']
        row_df['clock'] = i['clock']
        row_df['home_team_id'] = i['homeTeamId']
        row_df['home_team_score'] = i['homeTeamScore']
        row_df['is_a_play'] = i['isAPlay']
        row_df['narrative_formatted'] = i['narrativeFormatted']
        row_df['has_error'] = i['hasError']
        row_df['goals'] = i['goals']
        row_df['assists'] = i['assists']
        row_df['shots'] = i['shots']
        row_df['shots_on_goal'] = i['shotsOnGoal']
        row_df['assist_player_id'] = i['assistPlayerId']
        row_df['good_clear'] = i['goodClear']
        row_df['failed_clear'] = i['failedClear']
        row_df['disruptor_player_id'] = i['disruptorPlayerId']
        row_df['gw_goals'] = i['gwGoals']
        row_df['pp_goals'] = i['ppGoals']
        row_df['sh_goals'] = i['shGoals']
        row_df['ua_goals'] = i['uaGoals']
        row_df['ot_goals'] = i['otGoals']
        row_df['en_goals'] = i['enGoals']
        row_df['gt_goals'] = i['gtGoals']
        row_df['fg_goals'] = i['fgGoals']
        row_df['shootout_goals'] = i['shootoutGoals']
        row_df['penalties'] = i['penalties']
        row_df['shot_clock_violations'] = i['shotClockViolations']
        row_df['rcs'] = i['rcs']
        row_df['ycs'] = i['ycs']
        row_df['mn_penalties'] = i['mnPenalties']
        row_df['mj_penalties'] = i['mjPenalties']
        row_df['match_penalties'] = i['matchPenalties']
        row_df['fouls'] = i['fouls']
        row_df['face_won'] = i['faceWon']
        row_df['face_lost'] = i['faceLost']
        row_df['gbs'] = i['gbs']
        row_df['dc'] = i['dc']
        row_df['ct'] = i['ct']
        row_df['turnovers'] = i['turnovers']
        row_df['caused_turnover_player_id'] = i['causedTurnoverPlayerId']
        row_df['caused_turnover_team'] = i['causedTurnoverTeam']
        row_df['d_save'] = i['dsave']
        row_df['minutes'] = i['minutes']
        row_df['seconds'] = i['seconds']
        row_df['goalie_time'] = i['goalieTime']
        row_df['ga'] = i['ga']
        row_df['saves'] = i['saves']
        row_df['goalie_player_id'] = i['goaliePlayerId']
        row_df['shots_faced'] = i['shotsFaced']
        row_df['scoring_play'] = i['scoringPlay']

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

def get_au_lacrosse_season_pbp(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) lacrosse season, get and parse all play-by-play (PBP) data for an AU lacrosse season.
    
    Parameters
    ----------
    `season` (int, mandatory):
        The AU lacrosse season you want PBP data from.

    Returns
    ----------
    A pandas DataFrame containing PBP data from a AU season.

    """
    season_pbp_df = pd.DataFrame()
    season_id = get_au_lacrosse_season_id(season)
    url = "https://auprosports.com/proxy.php?request=api/seasons/lacrosse/v1"
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
                #     game_df = get_lacrosse_game_stats(season,j)
                # except:
                #     print(f'Couldn\'t parse game stats for game #{j}.')
                #     time.sleep(10)

                game_df = get_au_lacrosse_pbp(season_id,j)

                season_pbp_df = pd.concat([season_pbp_df,game_df],ignore_index=True)
                del game_df

    return season_pbp_df

def get_au_lacrosse_season_player_box(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) lacrosse season, get and parse all box-score game stats for an AU lacrosse season.
    This returns all player game stats, and does not return season stats or game averages.

    Parameters
    ----------
    `season` (int, mandatory):
        The AU lacrosse season you want player box scores from.

    Returns
    ----------
    A pandas DataFrame containing player box score stats a AU season.

    """
    season_stats_df = pd.DataFrame()
    season_id = get_au_lacrosse_season_id(season)
    url = "https://auprosports.com/proxy.php?request=api/seasons/lacrosse/v1"
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
                #     game_df = get_lacrosse_game_stats(season,j)
                # except:
                #     print(f'Couldn\'t parse game stats for game #{j}.')
                #     time.sleep(10)

                game_df = get_au_lacrosse_game_stats(season_id,j)

                season_stats_df = pd.concat([season_stats_df,game_df],ignore_index=True)
                del game_df

    return season_stats_df

def get_au_lacrosse_season_team_box(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) lacrosse season, get and parse all box-score game stats for an AU lacrosse season.
    This returns all player game stats, and does not return season stats or game averages.

    Parameters
    ----------
    `season` (int, mandatory):
        The AU lacrosse season you want player box scores from.

    Returns
    ----------
    A pandas DataFrame containing player box score stats a AU season.

    """
    season_stats_df = pd.DataFrame()
    season_id = get_au_lacrosse_season_id(season)
    url = "https://auprosports.com/proxy.php?request=api/seasons/lacrosse/v1"
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
                #     game_df = get_lacrosse_game_stats(season,j)
                # except:
                #     print(f'Couldn\'t parse game stats for game #{j}.')
                #     time.sleep(10)

                game_df = get_au_lacrosse_game_stats(season_id,j,get_team_stats=True)

                season_stats_df = pd.concat([season_stats_df,game_df],ignore_index=True)
                del game_df

    return season_stats_df

