import numpy as np

from NFLDataClasses.passRusher import PassRusher
from NFLDataClasses.passer import Passer
from NFLDataClasses.rusher import Rusher
from NFLDataClasses.receiver import Receiver
from NFLDataClasses.game import Game


def encapsulate_passerZoneStats(passer):
    gameId = passer.get('gameId')
    playerName = passer.get('playerName')
    teamAbbr = passer.get('teamAbbr')
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

    passer = Passer(gameId=gameId,esbId=esbId,playerName=playerName,teamAbbr=teamAbbr,avg_completion_pct=avg_completion_pct,
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
    if rushInfo is None:
        err = f"No rush information found for player {playerName}."
        return err

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
    if receptionInfo is None:
        err = f"No reception information found for player {playerName}."
        return err

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
    if sack_leader is None:
        print(f"No sack leader found for gameId {gameId}.")
        return None
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