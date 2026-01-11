import requests

import NFLDataVis.zone_plots
from NFLScrapers.GameCenter import encapsulate_game_stats as encaps
from NFLDataClasses.game import Game


def get_url_games():
    url = 'https://nextgenstats.nfl.com/api/league/schedule?season=2025'
    return url

def get_params(season,seasonType,week):
    params = {
        "season":season,
        "seasonType":seasonType,
        "week":week
    }
    return params

def get_data(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    # the keys for each game in data are different depending on the week
    # or whether the game has happened etc
    return data

def get_games(data):
    games = []
    unfinished_games = []
    for game in data:
        gameId = game.get('gameId')
        seasonType = game.get('seasonType')
        # home = game.get('homeDisplayName')
        # visitor = game.get('visitorDisplayName')
        homeTeamAbbr = game.get('homeTeamAbbr')
        visitorTeamAbbr = game.get('visitorTeamAbbr')
        week = game.get('week')
        gameDate = game.get('gameDate')
        if 'score' in game:
            score = game.get('score')
            phase = score.get('phase')
            if phase == 'FINAL':
                visitorTeamScores = score.get('visitorTeamScore')
                visitorPointTotal = visitorTeamScores.get('pointTotal')
                homeTeamScores = score.get('homeTeamScore')
                homePointTotal = homeTeamScores.get('pointTotal')
                if visitorPointTotal > homePointTotal:
                    winnerAbbr = visitorTeamAbbr
                elif homePointTotal > visitorPointTotal:
                    winnerAbbr = homeTeamAbbr
                else:
                    winnerAbbr = 'TIE'
                game = Game(week=week,seasonType=seasonType,gameDate=gameDate,gameId=gameId,homeTeamAbbr=homeTeamAbbr,
                            visitorTeamAbbr=visitorTeamAbbr,homeScore=homePointTotal,visitorScore=visitorPointTotal,winnerAbbr=winnerAbbr)
                games.append(game)
        else:
            game = Game(week=week,seasonType=seasonType,gameDate=gameDate,gameId=gameId,homeTeamAbbr=homeTeamAbbr,
                        visitorTeamAbbr=visitorTeamAbbr,homeScore=-1,visitorScore=-1,winnerAbbr='N/A')
            unfinished_games.append(game)
    return games, unfinished_games

def get_url_gameStats(gameId):
    url = f'https://nextgenstats.nfl.com/api/gamecenter/overview?gameId={gameId}'
    return url

# get_gameStats violates every good principle of design but I need it out of main
# so this is what we've got for now
def get_gameStats(gs_data, game):
    # game id
    g_id = game.gameId

    # passers
    passers = gs_data.get('passers')
    # rushers
    rushers = gs_data.get('rushers')
    # pass rushers
    passRushers = gs_data.get('passRushers')
    pr_avg = passRushers.get('avg')
    # receivers
    receivers = gs_data.get('receivers')
    r_avg = receivers.get('avg')
    # leaders
    leaders = gs_data.get('leaders')
    # speed leaders
    speedLeaders = leaders.get('speedLeaders')
    # time to sack leaders
    timeToSackLeaders = leaders.get('timeToSackLeaders')
    # pass distance leaders
    passDistanceLeaders = leaders.get('passDistanceLeaders')

    # home game stats
    ht = game.homeTeamAbbr
    home_passer = passers.get('home')
    print(f"{ht} passer (QB): ", home_passer)
    h_passer = encaps.encapsulate_passerZoneStats(home_passer)

    home_rushers = rushers.get('home')
    hrs = []
    for hr in home_rushers:
        h_rusher = encaps.encapsulate_rusherZoneStats(g_id, hr)
        hrs.append(h_rusher)
    for each in hrs:
        print(f"{ht} rusher: ", each)

    home_passRushers = passRushers.get('home')
    hprs = []
    for hpr in home_passRushers:
        hp_rusher = encaps.encapsulate_passRusherZoneStats(g_id, hpr)
        hprs.append(hp_rusher)
    for each in hprs:
        print(f"{ht} passRusher: ", each)

    home_receivers = receivers.get('home')
    hrecs = []
    for hrec in home_receivers:
        h_receiver = encaps.encapsulate_receiverZoneStats(g_id, hrec)
        hrecs.append(h_receiver)
    for each in hrecs:
        print(f"{ht} receiver: ", each)

    home_speedLeader = encaps.encapsulate_speedLeader(g_id, speedLeaders.get('home'))
    print(f"{ht} speed leader: ", home_speedLeader)
    home_timeToSackLeader = encaps.encapsulate_timeToSackLeader(g_id, timeToSackLeaders.get('home'))
    print(f"{ht} time-to-sack leader: ", home_timeToSackLeader)
    home_passDistanceLeader = encaps.encapsulate_passDistanceLeader(g_id, passDistanceLeaders.get('home'))
    print(f"{ht} pass distance leader: ", home_passDistanceLeader)

    # visitor game stats
    vt = game.visitorTeamAbbr

    visitor_passer = passers.get('visitor')
    print(f"{vt} passer (QB): ", visitor_passer)
    v_passer = encaps.encapsulate_passerZoneStats(visitor_passer)

    visitor_rushers = rushers.get('visitor')
    vrs = []
    for vr in visitor_rushers:
        v_rusher = encaps.encapsulate_rusherZoneStats(g_id, vr)
        vrs.append(v_rusher)
    for each in vrs:
        print(f"{vt} rusher: ", each)

    visitor_passRushers = passRushers.get('visitor')
    vprs = []
    for vpr in visitor_passRushers:
        vp_rusher = encaps.encapsulate_passRusherZoneStats(g_id, vpr)
        vprs.append(vp_rusher)
    for each in vprs:
        print(f"{vt} passRusher: ", each)

    visitor_receivers = receivers.get('visitor')
    vrecs = []
    for vrec in visitor_receivers:
        v_receiver = encaps.encapsulate_receiverZoneStats(g_id, vrec)
        vrecs.append(v_receiver)
    for each in vrecs:
        print(f"{vt} receiver: ", each)

    visitor_speedLeader = encaps.encapsulate_speedLeader(g_id, speedLeaders.get('visitor'))
    print(f"{vt} speed leader: ", visitor_speedLeader)
    visitor_timeToSackLeader = encaps.encapsulate_timeToSackLeader(g_id, timeToSackLeaders.get('visitor'))
    print(f"{vt} time-to-sack leader: ", visitor_timeToSackLeader)
    visitor_passDistanceLeader = encaps.encapsulate_passDistanceLeader(g_id, passDistanceLeaders.get('visitor'))
    print(f"{vt} pass distance leader: ", visitor_passDistanceLeader)

def get_zonePlots(gs_data,game):
    passers = gs_data.get('passers')
    # home QB
    home_passer = passers.get('home')
    print(f"{game.homeTeamAbbr} passer (QB): ", home_passer)
    h_passer = encaps.encapsulate_passerZoneStats(home_passer)
    # visitor QB
    visitor_passer = passers.get('visitor')
    print(f"{game.visitorTeamAbbr} passer (QB): ", visitor_passer)
    v_passer = encaps.encapsulate_passerZoneStats(visitor_passer)
    # show zone plot for QBs
    h_zones = h_passer.zones
    NFLDataVis.zone_plots.show_zone_performance(game, h_passer)
    v_zones = v_passer.zones
    NFLDataVis.zone_plots.show_zone_performance(game, v_passer)

# if __name__ == '__main__':
#     games_url = get_url_games()
#     headers = {
#         "User-Agent": "Mozilla/5.0",
#         "Accept": "application/json, text/plain, */*",
#         "Referer": "https://nextgenstats.nfl.com/stats/game-center-index",
#     }
#     # params = get_params(20,2,1)
#     # idk how to use params yet so this just loads er up
#     # tbh would only need params if i wanted previous seasons
#
#     data_games = get_data(games_url,headers)
#     games, unfinished_games = get_games(data_games)
#
#     # im just using this specific game for testing purposes
#     # and because go Bears and go comeback season baby
#
#     bears_packers = gf.findGames(games,'CHI','GB')
#
#     for game in bears_packers:
#         print(game)
#         g_id = game.gameId
#         gs_url = get_url_gameStats(g_id)
#         gs_data = get_data(gs_url, headers)
#
#         print("Home Team: ", game.homeTeamAbbr)
#         print("Visitor Team: ", game.visitorTeamAbbr)
#         print(f"Score: {game.homeTeamAbbr}: {game.homeScore} - {game.visitorTeamAbbr}: {game.visitorScore}")
#
#         get_gameStats(gs_data)
#         get_zonePlots(gs_data)