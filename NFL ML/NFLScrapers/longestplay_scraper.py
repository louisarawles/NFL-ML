from NFLDataClasses.ballCarrier import BallCarrier
from NFLDataClasses.longestPlay import DistancePlay
from NFLDataClasses.player import Player
from NFLLoaders import NFLLoader
from NFLScrapers import web_scraper as ws

def scrape_leaders(leaders):
    players = []
    longestPlays = []
    for l in leaders:
        leader = l.get('leader', {})
        #gsis primary official identifier
        gsisId = leader.get("gsisId")
        shortName = leader.get("shortName")
        playerName = leader.get("playerName")
        jerseyNumber = leader.get("jerseyNumber")
        position = leader.get("position")
        teamAbbr = leader.get("teamAbbr")
        teamId = leader.get("teamId")
        week = leader.get("week")
        yards = leader.get('yards')
        inPlayDist = leader.get("inPlayDist")
        speed = leader.get("maxSpeed")
        play = l.get('play', {})
        playType_raw = play.get('playType')
        playType_raw = playType_raw.replace("play_type_","")
        playType_raw = playType_raw.replace("_"," ")
        yardstr = f"{yards} YD "
        lpId = f"{inPlayDist}-{gsisId}-{week}"
        #print(yardstr)
        playType = yardstr + playType_raw

        player = Player(gsisId,shortName,playerName,jerseyNumber,position,teamAbbr,teamId,week,yards,inPlayDist,speed)
        play = DistancePlay(distance=inPlayDist,playType=playType,lpId=lpId,gsisId=gsisId,playerName=playerName,teamAbbr=teamAbbr,positionAbbr=position,week=week)
        players.append(player)
        longestPlays.append(play)
    return players, longestPlays

if __name__ == '__main__':
    url = 'https://nextgenstats.nfl.com/api/leaders/distance/ballCarrier'
    currWeek = 16
    for i in range(currWeek):
        params = ws.get_params("2025","REG",i+1)
        data = ws.get_data(url,params)
        leaders = ws.get_leaders(data)
        players, longestPlays = scrape_leaders(leaders)
        NFLLoader.load_players(players)
        NFLLoader.load_longestPlays(longestPlays)