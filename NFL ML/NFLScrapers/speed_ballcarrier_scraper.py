from NFLDataClasses.ballCarrier import BallCarrier
from NFLDataClasses.player import Player
from NFLLoaders import NFLLoader
from NFLScrapers import web_scraper as ws

def scrape_leaders(leaders):
    players = []
    ballCarriers = []
    for l in leaders:
        leader = l.get('leader', {})
        #gsis primary official identifier
        gsisId = leader.get("gsisId")
        #print(gsisId)
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
        bcId = f"{speed}-{gsisId}-{week}"
        playType = yardstr + playType_raw

        player = Player(gsisId,shortName,playerName,jerseyNumber,position,teamAbbr,teamId,week,yards,inPlayDist,speed)
        ballCarrier = BallCarrier(bcId=bcId,gsisId=gsisId,playerName=playerName,teamAbbr=teamAbbr,
                                  positionAbbr=position,speed=speed,
                                  week=week,playType=playType,)
        players.append(player)
        ballCarriers.append(ballCarrier)
    #print(len(players))
    # p = players[0]
    # WK = p.week
    # print(f"Week: {WK}")
    # print("Loading players...")
    # load_players(players)
    # print("Loading ballCarriers...")
    # load_ballCarriers(ballCarriers)
    # print(f"Players and ballCarriers loaded for week {WK}")
    return players,ballCarriers

if __name__ == '__main__':
    #inputs = input_params(sys.argv[1],sys.argv[2],sys.argv[3])
    # print(data.keys())
    url = 'https://nextgenstats.nfl.com/api/leaders/speed/ballCarrier'
    currWeek = 16
    for i in range(currWeek):
        params = ws.get_params("2025","REG",i+1)
        data = ws.get_data(url,params)
        leaders = ws.get_leaders(data)
        players, ballCarriers = scrape_leaders(leaders)
        NFLLoader.load_players(players)
        NFLLoader.load_ballCarriers(ballCarriers)
