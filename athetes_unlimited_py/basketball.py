import json
import time
#from urllib.request import urlopen

import pandas as pd
import requests
from tqdm import tqdm

from athetes_unlimited_py.utils import raise_html_status_code

############################################################################################################################################################################################################################################################
##
## Basketball-only utilities
##
############################################################################################################################################################################################################################################################

def get_au_basketball_season(season_id:int) -> int:
    """
    Given a season ID, `get_au_basketball_season()` returns the proper season for the corresponding Athletes Unlimited basketball season.

    Parameters
    ----------
    `season_id` (int, mandatory):
        The season ID you want a season for in Athletes Unlimited basketball. 
        If there isn't a season for the inputted `season_id`, a `ValueError()` exception will be raised.
    
    Returns
    ----------
    The proper season corresponding to an Athletes Unlimited basketball season ID.
    """
    season = 0
    
    if season_id == 6:
        season= 2022
        return season
    elif season_id == 73:
        season = 2023
        return season 
    else:
        raise ValueError(f'[season] can only be 2022 or 2023 at this time for basketball.\nYou entered :\n\t{season}')

def get_au_basketball_season_id(season:int) -> int:
    """
    Given a season, `get_au_basketball_season_id()` returns the proper season ID for the Athletes Unlimited basketball season.

    Parameters
    ----------
    `season` (int, mandatory):
        The season you want a season ID for basketball. 
        If there isn't a season ID for the inputted `season`, a `ValueError()` exception will be raised.
    
    Returns
    ----------
    The proper season ID corresponding to an Athletes Unlimited basketball season.
    """
    seasonId = 0
    
    if season == 2022:
        seasonId = 6
        return seasonId
    elif season == 2023:
        seasonId = 73
        return seasonId 
    else:
        raise ValueError(f'[season] can only be 2022 or 2023 at this time for basketball.\nYou entered :\n\t{season}')

############################################################################################################################################################################################################################################################
##
## Game Functions
##
############################################################################################################################################################################################################################################################

def get_au_basketball_game_stats(season:int,game_num:int,get_team_stats=False,get_player_and_team_stats=False,rename_cols=False) -> pd.DataFrame():
    """
    Retrieves the player and/or team game stats for an Atheltes Unlimited (AU) basketball game.

    Parameters
    ----------
    `season` (int, mandatory):
        The AU basketball season you want a game from.
    
    `game_num` (int, mandatory):
        The game number you want player and/or team stats from.
        This is not the game ID!
        A `ValueError` will be raised if `game_num` is set to less than 1.
    
    `get_team_stats` (bool, optional) = False:
        Optional boolean argument. 
        If set to `True`, the pandas DataFrame returned by `get_basketball_game_stats()` will only return team stats for that game, 
        and will not return player stats, unless `get_player_and_team_stats` is set to `True` if `get_team_stats` is set to `True`.
    
    `get_player_and_team_stats` (bool, optional) = False:

    `rename_cols` (bool, optional) = False:
        NOT IMPLEMENTED YET!
        `get_basketball_game_stats()` will have no change in functionality at this time if `rename_cols` is set to `True`.

    Returns
    ----------
    A pandas DataFrame containing player and/or team stats for a given AU game within a given AU season.
    """
    #

    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    player_stats_df = pd.DataFrame()
    team_stats_df = pd.DataFrame()
    row_df = pd.DataFrame()
    
    season_id = get_au_basketball_season_id(season)
    
    if game_num < 1:
        raise ValueError('`game_num` cannot be less than 0.')
    
    key = int(time.time()) # Yes, the key is literaly the int of the Epoch time at the time of the GET request.
    
    url = f"https://auprosports.com/proxy.php?request=/api/stats/basketball/v1/{season_id}/by-game/{game_num}?statType=basketball%26k={key}"
    
    response = requests.get(url,headers=headers)
    raise_html_status_code(response.status_code)
    
    json_data = json.loads(response.text)
    time.sleep(0.5)

    sport = json_data['metaSport']['sport']
    api_version = json_data['metaSport']['version']

    for i in json_data['data']:
        #print(i)
        row_df = pd.DataFrame({'sport':sport,'api_version':api_version},index=[0])
        row_df['type'] = i['type']
        row_df['teamId'] = i['teamId']

        if i['homeTeamFlg'] == True:
            row_df['homeTeamFlg'] = 1
        else:
            row_df['homeTeamFlg'] = 0

        ##############################################################################################################################
        ## Player/Team info
        ##############################################################################################################################
        row_df['season'] = get_au_basketball_season(i['seasonId'])
        row_df['seasonId'] = i['seasonId']
        row_df['weekNumber'] = i['stats'][0]['weekNumber']
        row_df['gameNumber'] = i['stats'][0]['gameNumber']
        row_df['seasonType'] = i['stats'][0]['seasonType']

        row_df['playerId'] = i['playerId']
        row_df['uniformNumber'] = i['uniformNumber']
        row_df['uniformNumberDisplay'] = str(i['uniformNumberDisplay'])
        
        row_df['primaryPositionLk'] = i['primaryPositionLk']
        row_df['secondaryPositionLk'] = i['secondaryPositionLk']
        row_df['first_name'] = str(i['firstName']).replace('\u2019','\'')
        row_df['last_name'] = str(i['lastName']).replace('\u2019','\'')
        row_df['full_name'] = f"{i['firstName']} {i['lastName']}".replace('\u2019','\'')

        ##############################################################################################################################
        ## Game Stats
        ##############################################################################################################################
        
        row_df['G'] = i['stats'][0]['gamesPlayed']
        row_df['MIN'] = i['stats'][0]['minutesPlayed']

        row_df['FGM'] = i['stats'][0]['fieldGoalsMade']
        row_df['FGA'] = i['stats'][0]['fieldGoalsAttempted']
        row_df['FG%'] = row_df['FGM'] /row_df['FGA']
        row_df['FG%'] = row_df['FG%'].round(3)

        row_df['3PM'] = i['stats'][0]['made3Pointers']
        row_df['3PA'] = i['stats'][0]['attempted3Pointers']
        row_df['3P%'] = row_df['3PM'] /row_df['3PA']
        row_df['3P%'] = row_df['3P%'].round(3)

        row_df['2PM'] = i['stats'][0]['made2Pointers']
        row_df['2PA'] = i['stats'][0]['missed2Pointers'] + i['stats'][0]['made2Pointers']
        row_df['2P%'] = row_df['2PM'] /row_df['2PA']
        row_df['2P%'] = row_df['2P%'].round(3)

        row_df['FTM'] = i['stats'][0]['madeFreeThrows']
        row_df['FTA'] = i['stats'][0]['freeThrowsAttempted']
        row_df['FT%'] = row_df['FTM'] / row_df['FTA']
        row_df['FT%'] = row_df['FT%'].round(3)

        row_df['ORB'] = i['stats'][0]['offensiveRebounds']
        row_df['DRB'] = i['stats'][0]['defensiveRebounds']
        row_df['TRB'] = i['stats'][0]['rebounds']

        row_df['AST'] = i['stats'][0]['assists']
        row_df['STL'] = i['stats'][0]['steals']
        row_df['BLK'] = i['stats'][0]['blocks']

        row_df['TOV'] = i['stats'][0]['turnovers']
        row_df['PTS'] = i['stats'][0]['points']

        row_df['AU_PTS'] = i['stats'][0]['auTotalPoints']

        row_df['eFG%'] = (row_df['FGM'] + (0.5 * row_df['3PM'])) / row_df['FGA']
        row_df['eFG%'] = row_df['eFG%'].round(3)

        row_df['TS%'] = row_df['PTS'] / (2 * ((row_df['FGA']) + (0.44 * row_df['FTA'])))
        row_df['TS%'] = row_df['TS%'].round(3)
        row_df['shootingFoulsCommitted'] = i['stats'][0]['shootingFoulsCommitted']
        row_df['shootingFoulsDrawn'] = i['stats'][0]['shootingFoulsDrawn']
        row_df['personalFoulsCommitted'] = i['stats'][0]['personalFoulsCommitted']
        row_df['personalFoulsDrawn'] = i['stats'][0]['personalFoulsDrawn']
        row_df['offensiveFoulsCommitted'] = i['stats'][0]['offensiveFoulsCommitted']
        row_df['offensiveFoulsDrawn'] = i['stats'][0]['offensiveFoulsDrawn']
        row_df['doubleDoubles'] = i['stats'][0]['doubleDoubles']
        row_df['tripleDoubles'] = i['stats'][0]['tripleDoubles']

        row_df['GmSc'] = row_df['PTS'] + (0.4 * row_df['FGM']) + (0.7 * row_df['ORB']) + (0.3 * row_df['DRB']) + row_df['STL'] + (0.7 * row_df['AST']) + (0.7 * row_df['BLK']) * (0.7 * row_df['FGA']) - (0.4 * (row_df['FTA'] - row_df['FTM'])) - (0.4 * row_df['personalFoulsCommitted']) - row_df['TOV']
        
        ##############################################################################################################################
        ## Save the data to the correct DataFrame
        ##############################################################################################################################

        if i['type'] == "Team":
            team_stats_df = pd.concat([team_stats_df,row_df],ignore_index=True)
        else:
            player_stats_df = pd.concat([player_stats_df,row_df],ignore_index=True)

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

def get_au_basketball_pbp(season:int,game_id:int,return_participation_data=False):
    """
    Retrieves the play-by-play (PBP) data for an Atheltes Unlimited (AU) basketball game.

    Parameters
    ----------
    `season` (int, mandatory):
        The AU basketball season you want a game from.
    
    `game_id` (int, mandatory):
        The AU basketball game ID you want PBP data from.
    
    `return_participation_data` (bool, optional) = `False`:
        Optional argument. 
        If set to `True`, `get_au_basketball_pbp()` will return a secondary pandas DataFrame
        containing roster information for this AU basketball game.

    Returns
    ----------
    A pandas DataFrame containing PBP data for a given AU game ID within a given AU season.
    If `return_participation_data` is set to `True`, an additional pandas DataFrame containing roster data for this game will be returned as well.
    """

    season_id = get_au_basketball_season_id(season)

    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    season_pbp_df = pd.DataFrame()
    game_pbp_df = pd.DataFrame()
    roster_df = pd.DataFrame()
    row_df = pd.DataFrame()
        
    if game_id < 1:
        raise ValueError('`game_id` cannot be less than 0.')
    
    key = int(time.time()) # Yes, the key is literaly the int of the Epoch time at the time of the GET request.
    url = f"https://auprosports.com/proxy.php?request=/api/play-by-play/basketball/v1/event/{season_id}/game/{game_id}?k={key}"

    response = requests.get(url,headers=headers)
    raise_html_status_code(response.status_code)
    
    del headers, key

    json_data = json.loads(response.text)
    time.sleep(0.5)

    for i in json_data['data'][0]['plays']:
        row_df = pd.DataFrame({'season':season,'game_id':game_id},index=[0])
        row_df['gameNumber'] = i['gameNumber']
        row_df['playSeqno'] = i['playSeqno']
        row_df['narrative'] = i['narrative']
        row_df['narrativeFormatted'] = i['narrativeFormatted']
        row_df['homeTeamId'] = i['homeTeamId']
        row_df['homeTeamScore'] = i['homeTeamScore']
        row_df['awayTeamId'] = i['awayTeamId']
        row_df['awayTeamScore'] = i['awayTeamScore']
        row_df['isAPlay'] = i['isAPlay']
        row_df['generatesPointAuditFlg'] = i['generatesPointAuditFlg']
        row_df['hasError'] = i['hasError']
        row_df['playerId'] = i['playerId']
        row_df['teamId'] = i['teamId']
        row_df['action'] = i['action']
        row_df['type'] = i['type']
        row_df['quarter'] = i['quarter']
        row_df['clock'] = i['clock']
        row_df['assist'] = i['assist']
        row_df['steal'] = i['steal']
        row_df['block'] = i['block']
        row_df['turnover'] = i['turnover']
        row_df['jumper'] = i['jumper']
        row_df['dunk'] = i['dunk']
        row_df['tipIn'] = i['tipIn']
        row_df['timeout'] = i['timeout']
        row_df['inThePaint'] = i['inThePaint']
        row_df['onFastBreak'] = i['onFastBreak']
        row_df['missedThreePointer'] = i['missedThreePointer']
        row_df['madeThreePointer'] = i['madeThreePointer']
        row_df['missedTwoPointer'] = i['missedTwoPointer']
        row_df['madeTwoPointer'] = i['madeTwoPointer']
        row_df['missedFreeThrow'] = i['missedFreeThrow']
        row_df['madeFreeThrow'] = i['madeFreeThrow']
        row_df['offensiveRebound'] = i['offensiveRebound']
        row_df['defensiveRebound'] = i['defensiveRebound']
        row_df['shootingFoulCommitted'] = i['shootingFoulCommitted']
        row_df['shootingFoulDrawn'] = i['shootingFoulDrawn']
        row_df['shootingFoulDrawnByPlayerId'] = i['shootingFoulDrawnByPlayerId']
        row_df['personalFoulCommitted'] = i['personalFoulCommitted']
        row_df['personalFoulDrawn'] = i['personalFoulDrawn']
        row_df['personalFoulDrawnByPlayerId'] = i['personalFoulDrawnByPlayerId']
        row_df['offensiveFoulCommitted'] = i['offensiveFoulCommitted']
        row_df['offensiveFoulDrawn'] = i['offensiveFoulDrawn']
        row_df['offensiveFoulDrawnByPlayerId'] = i['offensiveFoulDrawnByPlayerId']
        row_df['otherFoulCommitted'] = i['otherFoulCommitted']
        row_df['otherFoulDrawn'] = i['otherFoulDrawn']
        row_df['otherFoulDrawnByPlayerId'] = i['otherFoulDrawnByPlayerId']
        row_df['scoringPlay'] = i['scoringPlay']


        season_pbp_df = pd.concat([season_pbp_df,row_df])
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

                row_df['competitorId'] = j['competitorId']
                row_df['playerId'] = j['playerId']
                row_df['captainFlg'] = j['captainFlg']
                row_df['displayName'] = j['displayName']
                row_df['firstName'] = j['firstName']
                row_df['lastName'] = j['lastName']
                row_df['currentRosterStatus_description'] = j['currentRosterStatus']['description']
                row_df['currentRosterStatus_comments'] = j['currentRosterStatus']['comments']
                row_df['currentRosterStatus_transactionType'] = j['currentRosterStatus']['transactionType']
                row_df['currentRosterStatus_rosterStatusLk'] = j['currentRosterStatus']['rosterStatusLk']
                row_df['isVotingFlg'] = j['isVotingFlg']
                row_df['canBeVotedForFlg'] = j['canBeVotedForFlg']
                row_df['hasVotedFlg'] = j['hasVotedFlg']
                row_df['uniformNumber'] = str(j['uniformNumber'])
                row_df['isNominatedFlg'] = j['isNominatedFlg']
                row_df['nominatedFlg'] = j['nominatedFlg']
                row_df['resourceUrl'] = j['resourceUrl']
                row_df['imageUrl'] = j['imageResource']['imageUrl']

                roster_df = pd.concat([roster_df,row_df],ignore_index=True)
            del row_df

        del json_data
        return season_pbp_df,roster_df
    
    else:
        del json_data, roster_df
        return season_pbp_df

############################################################################################################################################################################################################################################################
##
## Season Functions
##
############################################################################################################################################################################################################################################################


def get_au_basketball_season_pbp(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) basketball season, get and parse all play-by-play (PBP) data for an AU basketball season.
    
    Parameters
    ----------
    `season` (int, mandatory):
        The AU basketball season you want PBP data from.

    Returns
    ----------
    A pandas DataFrame containing PBP data from a AU season.

    """
    season_pbp_df = pd.DataFrame()
    seasonId = get_au_basketball_season_id(season)
    url = "https://auprosports.com/proxy.php?request=api/seasons/basketball/v1"
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

    response = requests.get(url,headers=headers)
    sport_json_data = json.loads(response.text)
    
    for i in sport_json_data['data']:
        #print(i)
        if i['seasonId'] == seasonId:
            len_game_ids = len(i['gameIds'])

            for j in tqdm(range(1,len_game_ids+1)):
                print(f'\nOn game {j} of {len_game_ids+1} for {season}.')
                # try:
                #     game_df = get_basketball_game_stats(season,j)
                # except:
                #     print(f'Couldn\'t parse game stats for game #{j}.')
                #     time.sleep(10)

                game_df = get_au_basketball_game_stats(season,j,get_team_stats=True)

                season_pbp_df = pd.concat([season_pbp_df,game_df],ignore_index=True)
                del game_df

    return season_pbp_df

def get_au_basketball_season_player_box(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) basketball season, get and parse all box-score game stats for an AU basketball season.
    This returns all player game stats, and does not return season stats or game averages.

    Parameters
    ----------
    `season` (int, mandatory):
        The AU basketball season you want player box scores from.

    Returns
    ----------
    A pandas DataFrame containing player box score stats a AU season.

    """
    season_stats_df = pd.DataFrame()
    seasonId = get_au_basketball_season_id(season)
    url = "https://auprosports.com/proxy.php?request=api/seasons/basketball/v1"
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

    response = requests.get(url,headers=headers)
    sport_json_data = json.loads(response.text)
    
    for i in sport_json_data['data']:
        #print(i)
        if i['seasonId'] == seasonId:
            len_game_ids = len(i['gameIds'])

            for j in len_game_ids:
                print(f'\nOn game {j} of {len_game_ids+1} for {season}.')
                # try:
                #     game_df = get_basketball_game_stats(season,j)
                # except:
                #     print(f'Couldn\'t parse game stats for game #{j}.')
                #     time.sleep(10)

                game_df = get_au_basketball_pbp(season,j)

                season_stats_df = pd.concat([season_stats_df,game_df],ignore_index=True)
                del game_df

    return season_stats_df

def get_au_basketball_season_team_box(season:int) -> pd.DataFrame():
    """
    Given an Atheltes Unlimited (AU) basketball season, get and parse all box-score game stats for an AU basketball season.
    This returns all player game stats, and does not return season stats or game averages.

    Parameters
    ----------
    `season` (int, mandatory):
        The AU basketball season you want player box scores from.

    Returns
    ----------
    A pandas DataFrame containing player box score stats a AU season.

    """
    season_stats_df = pd.DataFrame()
    seasonId = get_au_basketball_season_id(season)
    url = "https://auprosports.com/proxy.php?request=api/seasons/basketball/v1"
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
                #     game_df = get_basketball_game_stats(season,j)
                # except:
                #     print(f'Couldn\'t parse game stats for game #{j}.')
                #     time.sleep(10)

                game_df = get_au_basketball_game_stats(season,j,get_team_stats=True)

                season_stats_df = pd.concat([season_stats_df,game_df],ignore_index=True)
                del game_df

    return season_stats_df

