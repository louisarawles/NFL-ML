# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from NFLDataClasses.ballCarrier import BallCarrier
from NFLDataClasses.longestPlay import LongestPlay
from NFLDataClasses.player import Player

from NFLLoaders import NFLLoader

from NFLScrapers import web_scraper as ws
from NFLScrapers import longestplay_scraper as lsp
from NFLScrapers import speed_ballcarrier_scraper as bc
from NFLScrapers import game_center_scraper as gc

from typing import Any

LeaderItem = dict[str,dict[str,Any]]

# encapsulate code to load each table into separate methods to make main less confusing
# lol.
def lsp_caller(params):
    url = lsp.get_url()
    headers = ws.get_headers_playerStats()
    data = ws.get_data(url,headers,params)
    leaders = ws.get_leaders(data)
    # leaders is a list of lists of dictionaries fyi
    # to see the keys:
    # l = leader[0]
    # print(l.keys())
    # keys: 'leader', 'play'
    # keys lead to dictionaries
    longPlays = lsp.scrape_longestPlays(leaders)
    NFLLoader.load_longestPlays(longPlays)
    return leaders

def bc_caller(params):
    url = bc.get_url()
    headers = ws.get_headers_playerStats()
    data = ws.get_data(url,headers,params)
    leaders = ws.get_leaders(data)
    speedBallCarriers = bc.scrape_ballCarriers(leaders)
    NFLLoader.load_ballCarriers(speedBallCarriers)
    return leaders

def gameCenter_caller():
    url = gc.get_url()
    headers = ws.get_headers_gameCenter()
    data = gc.get_data(url,headers)
    games, unfinished_games = gc.get_games(data)
    NFLLoader.load_games(games)
    print(f"Incomplete games: {unfinished_games} were not loaded into the database.")
    return games, unfinished_games

if __name__ == '__main__':
    currWeek = 18

    leaders = []
    players = []
    bcs = []

    games, unfinished_games = gameCenter_caller()

    params = ws.get_params("2025","REG",1)

    lsp_leaders = lsp_caller(params)
    l = lsp_leaders[0]
    print(l.keys())
    lead = l.get('leader',{})
    print("leader: ",lead)
    play = l.get('play', {})
    print("play: ",play)
    playstats = play.get('playStats',{})
    # print(len(playstats))
    p_playstat = playstats[0]
    print(p_playstat.keys())
    # p_playstat2 = playstats[1]
    # print(p_playstat2.keys())
    # p_playstat3 = playstats[2]
    # print(p_playstat3.keys())
    # for i in range(currWeek):
    #     params = ws.get_params("2025","REG",i+1)
    #     # parse and load player stats by invoking callers defined above
    #     # lsp
    #     lsp_leaders = lsp_caller(params)
    #     # bc
    #     bc_leaders = bc_caller(params)
    #
    #     #update leaders list from all stat categories
    #     leaders.extend(lsp_leaders)
    #     leaders.extend(bc_leaders)
    #
    #     #update players list for all new leaders
    #     players.extend(ws.scrape_players(leaders))
    #
    # #load players
    # NFLLoader.load_players(players)


    #load specific stats

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
