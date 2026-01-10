from NFLDataClasses.ballCarrier import BallCarrier
from NFLDataClasses.longestPlay import LongestPlay
from NFLDataClasses.player import Player
from NFLLoaders import NFLLoader
from NFLScrapers import web_scraper as ws

def scrape_longestPlays(leaders):
    longestPlays = []
    for l in leaders:
        leader = l.get('leader', {})
        esbId = leader.get("esbId")
        playerName = leader.get("playerName")
        position = leader.get("position")
        teamAbbr = leader.get("teamAbbr")
        week = leader.get("week")
        yards = leader.get('yards')
        inPlayDist = leader.get("inPlayDist")
        play = l.get('play', {})
        playType_raw = play.get('playType')
        playType_raw = playType_raw.replace("play_type_","")
        playType_raw = playType_raw.replace("_"," ")
        yardstr = f"{yards} YD "
        lpId = f"{inPlayDist}-{esbId}-{week}"
        playType = yardstr + playType_raw

        play = LongestPlay(distance=inPlayDist,playType=playType,lpId=lpId,esbId=esbId,playerName=playerName,teamAbbr=teamAbbr,positionAbbr=position,week=week)
        longestPlays.append(play)
    return longestPlays

def get_url():
    url = 'https://nextgenstats.nfl.com/api/leaders/distance/ballCarrier'
    return url