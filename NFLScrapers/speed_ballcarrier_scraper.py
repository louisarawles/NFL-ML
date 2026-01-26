from NFLDataClasses.ballCarrier import BallCarrier
from NFLLoaders import NFLLoader
from NFLScrapers import web_scraper as ws

def scrape_ballCarriers(leaders):
    ballCarriers = []
    for l in leaders:
        leader = l.get('leader', {})
        #esb id data scraping id
        esbId = leader.get("esbId")
        playerName = leader.get("playerName")
        position = leader.get("position")
        teamAbbr = leader.get("teamAbbr")
        week = leader.get("week")
        yards = leader.get('yards')
        speed = leader.get("maxSpeed")

        play = l.get('play', {})
        playType_raw = play.get('playType')
        playType_raw = playType_raw.replace("play_type_","")
        playType_raw = playType_raw.replace("_"," ")
        yardstr = f"{yards} YD "
        bcId = f"{speed}-{esbId}-{week}"
        playType = yardstr + playType_raw

        ballCarrier = BallCarrier(bcId=bcId,esbId=esbId,playerName=playerName,teamAbbr=teamAbbr,
                                  positionAbbr=position,speed=speed,
                                  week=week,playType=playType,)
        ballCarriers.append(ballCarrier)
    return ballCarriers

def get_url():
    url = 'https://nextgenstats.nfl.com/api/leaders/speed/ballCarrier'
    return url
