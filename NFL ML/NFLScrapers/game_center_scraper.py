import requests
import numpy as np

from NFLDataClasses.game import Game
from NFLDataClasses.passRusher import PassRusher
from NFLDataClasses.passer import Passer
from NFLDataClasses.receiver import Receiver
from NFLDataClasses.rusher import Rusher


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
                game = Game(week=week,gameDate=gameDate,gameId=gameId,homeTeamAbbr=homeTeamAbbr,
                            visitorTeamAbbr=visitorTeamAbbr,homeScore=homePointTotal,visitorScore=visitorPointTotal,winnerAbbr=winnerAbbr)
                games.append(game)
        else:
            game = Game(week=week,gameDate=gameDate,gameId=gameId,homeTeamAbbr=homeTeamAbbr,
                        visitorTeamAbbr=visitorTeamAbbr,homeScore=-1,visitorScore=-1,winnerAbbr='N/A')
            unfinished_games.append(game)
    return games, unfinished_games

def get_url_gameStats(gameId):
    url = f'https://nextgenstats.nfl.com/api/gamecenter/overview?gameId={gameId}'
    return url

def encapsulate_passerZoneStats(gameId,passer):
    playerName = passer.get('playerName')
    esbId = passer.get('esbId')
    # zones
    zones = passer.get('zones')
    # there are max 12 zones
    # len of zones for a player depends on where they attempted a pass
    completionPcts = []
    total_attempts = 0
    total_completions = 0
    qbRatings = []
    list_yds = []
    total_tds = 0
    total_yds = 0
    total_interceptions = 0
    dict_qbRatingSuccessLevel = {
        'BELOW': 0,
        'AVERAGE': 0,
        'ABOVE': 0
    }
    for z in zones:
        completionPcts.append(z.get('completionPct'))
        total_completions += z.get('completions')
        total_attempts += z.get('attempts')
        yds = z.get('yards')
        list_yds.append(yds)
        total_yds += yds
        total_tds += z.get('touchdowns')
        total_interceptions += z.get('interceptions')
        qbRatings.append(z.get('qbRating'))
        lvl = z.get('qbRatingSuccessLevel')
        dict_qbRatingSuccessLevel[lvl] += 1

    avg_completion_pct = float(np.average(completionPcts))
    avg_yds = float(np.average(list_yds))
    avg_qbRating = float(np.average(qbRatings))
    mode_lvl = max(dict_qbRatingSuccessLevel, key=dict_qbRatingSuccessLevel.get)

    passer = Passer(gameId=gameId,esbId=esbId,playerName=playerName,avg_completion_pct=avg_completion_pct,
                    avg_yds=avg_yds,avg_qbRating=avg_qbRating,mode_lvl=mode_lvl,total_attempts=total_attempts,
                    total_completions=total_completions,total_tds=total_tds,total_yds=total_yds,
                    total_interceptions=total_interceptions,zones=zones)
    # plot players full passing zone performance
    # show_zone_performance(playerName, zones)
    return passer

def encapsulate_rusherZoneStats(gameId,rusher):
    playerName = rusher.get('playerName')
    esbId = rusher.get('esbId')
    rushYards = rusher.get('rushYards')
    rushInfo = rusher.get('rushInfo')
    touchdowns = rushInfo.get('touchdowns')
    distance = rushInfo.get('distance')
    avgYards= rushInfo.get('avgYards')
    avgDistance = rushInfo.get('avgDistance')
    avgTimeToLos = rushInfo.get('avgTimeToLos')

    rushLocationMap = rushInfo.get('rushLocationMap')
    rusher = Rusher(gameId=gameId, esbId=esbId, playerName=playerName,
                    rushYards=rushYards,touchdowns=touchdowns,distance=distance,
                    avgYards=avgYards,avgDistance=avgDistance,
                    avgTimeToLos=avgTimeToLos,rushLocationMap=rushLocationMap)
    return rusher

def encapsulate_passRusherZoneStats(gameId,passRusher):
    playerName = passRusher.get('playerName')
    esbId = passRusher.get('esbId')
    blitzCount = passRusher.get('blitzCount')
    avgSeparationToQb = passRusher.get('avgSeparationToQb')
    tackles = passRusher.get('tackles')
    assists = passRusher.get('assists')
    sacks = passRusher.get('sacks')
    forcedFumbles = passRusher.get('forcedFumbles')

    passRusher = PassRusher(gameId=gameId, esbId=esbId,playerName=playerName,
                            blitzCount=blitzCount,avgSeparationToQb=avgSeparationToQb,
                            tackles=tackles,assists=assists,sacks=sacks,
                            forcedFumbles=forcedFumbles)
    return passRusher

def encapsulate_receiverZoneStats(g_id,rec):
    playerName = rec.get('playerName')
    esbId = rec.get('esbId')

    recYards = rec.get('recYards')
    receptionInfo = rec.get('receptionInfo')

    avgAirYards = receptionInfo.get('avgAirYards')
    avgCushion = receptionInfo.get('avgCushion')
    avgSeparation = receptionInfo.get('avgSeparation')
    targets = rec.get('targets')
    receptions = rec.get('receptions')
    touchdowns = rec.get('touchdowns')

    receiver = Receiver(gameId=g_id,esbId=esbId,playerName=playerName,recYards=recYards,avgAirYards=avgAirYards,avgCushion=avgCushion,avgSeparation=avgSeparation,targets=targets,receptions=receptions,touchdowns=touchdowns)
    return receiver

def encapsulate_speedLeader(gameId,speed_leader):
    esbId = speed_leader.get('esbId')
    playerName = speed_leader.get('playerName')
    maxSpeed = speed_leader.get('maxSpeed')
    speedLeader = {
        'gameId': gameId,
        'esbId': esbId,
        'playerName': playerName,
        'maxSpeed': maxSpeed,
    }
    return speedLeader

def encapsulate_timeToSackLeader(gameId,sack_leader):
    esbId = sack_leader.get('esbId')
    playerName = sack_leader.get('playerName')
    timeToTackle = sack_leader.get('tackleInfo').get('timeToTackle')
    sackLeader = {
        'gameId': gameId,
        'esbId': esbId,
        'playerName': playerName,
        'timeToTackle': timeToTackle,
    }
    return sackLeader

def encapsulate_passDistanceLeader(gameId,passDistance_Leader):
    esbId = passDistance_Leader.get('esbId')
    playerName = passDistance_Leader.get('playerName')
    airDistance = passDistance_Leader.get('passInfo').get('airDistance')
    passDistanceLeader = {
        'gameId': gameId,
        'esbId': esbId,
        'playerName': playerName,
        'airDistance': airDistance,
    }
    return passDistanceLeader

if __name__ == '__main__':
    games_url = get_url_games()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://nextgenstats.nfl.com/stats/game-center-index",
    }
    # params = get_params(20,2,1)
    # idk how to use params yet so this just loads er up
    # tbh would only need params if i wanted previous seasons
    data_games = get_data(games_url,headers)
    games, unfinished_games = get_games(data_games)

    # im just using this specific game to make this easy
    g = games[50]
    print(g)
    g_id = g.gameId
    gs_url = get_url_gameStats(g_id)
    gs_data = get_data(gs_url,headers)

    #passers
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
    home_passer = passers.get('home')
    h_passer = encapsulate_passerZoneStats(g_id,home_passer)

    home_rushers = rushers.get('home')
    hrs = []
    for hr in home_rushers:
        h_rusher = encapsulate_rusherZoneStats(g_id, hr)
        hrs.append(h_rusher)
    for each in hrs:
        print("Home rusher: ", each)

    home_passRushers = passRushers.get('home')
    hprs = []
    for hpr in home_passRushers:
        hp_rusher = encapsulate_passRusherZoneStats(g_id, hpr)
        hprs.append(hp_rusher)
    for each in hprs:
        print("Home passRusher: ", each)

    home_receivers = receivers.get('home')
    hrecs = []
    for hrec in home_receivers:
        h_receiver = encapsulate_receiverZoneStats(g_id, hrec)
        hrecs.append(h_receiver)
    for each in hrecs:
        print("Home receiver: ", each)

    home_speedLeader = encapsulate_speedLeader(g_id, speedLeaders.get('home'))
    home_timeToSackLeader = encapsulate_timeToSackLeader(g_id, timeToSackLeaders.get('home'))
    home_passDistanceLeader = encapsulate_passDistanceLeader(g_id, passDistanceLeaders.get('home'))

    # visitor game stats
    visitor_passer = passers.get('visitor')
    v_passer = encapsulate_passerZoneStats(g_id,visitor_passer)

    visitor_rushers = rushers.get('visitor')
    vrs = []
    for vr in visitor_rushers:
        v_rusher = encapsulate_rusherZoneStats(g_id,vr)
        vrs.append(v_rusher)
    for each in vrs:
        print("Visitor rusher: ", each)

    visitor_passRushers = passRushers.get('visitor')
    vprs = []
    for vpr in visitor_passRushers:
        vp_rusher = encapsulate_passRusherZoneStats(g_id,vpr)
        vprs.append(vp_rusher)
    for each in vprs:
        print("Visitor passRusher: ", each)

    visitor_receivers = receivers.get('visitor')
    vrecs = []
    for vrec in visitor_receivers:
        v_receiver = encapsulate_receiverZoneStats(g_id,vrec)
        vrecs.append(v_receiver)
    for each in vrecs:
        print("Visitor receiver: ", each)

    visitor_speedLeader = encapsulate_speedLeader(g_id, speedLeaders.get('visitor'))
    visitor_timeToSackLeader = encapsulate_timeToSackLeader(g_id, timeToSackLeaders.get('visitor'))
    visitor_passDistanceLeader = encapsulate_passDistanceLeader(g_id, passDistanceLeaders.get('visitor'))