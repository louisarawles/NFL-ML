import player
import requests
from bs4 import BeautifulSoup
from player import Player
from databaseDriver import DatabaseDriver

url = 'https://nextgenstats.nfl.com/api/leaders/speed/ballCarrier'
params = {
    "limit":20,
    "season":2025,
    "seasonType":"REG"
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://nextgenstats.nfl.com",
}

response = requests.get(url, params=params, headers=headers)
response.raise_for_status()
data = response.json()
file = "NFL_stats.sqlite"
#dict_keys: (['season', 'seasonType', 'leaders'])
leaders = data["leaders"]
def scrape_leaders(leaders):
    players = []
    for l in leaders:
        #leader
        #nflId = r['leader']["nflId"]
        #esbId = r['leader']["esbId"]
        #gsis primary official identifier
        gsisId = l['leader']["gsisId"]

        #firstName = r['leader']["firstName"]
        #lastName = r['leader']["lastName"]
        shortName = l['leader']["shortName"]
        playerName = l['leader']["playerName"]

        jerseyNumber = l['leader']["jerseyNumber"]

        position = l['leader']["position"]
        #positionGroup = l['leader']["positionGroup"]

        teamAbbr = l['leader']["teamAbbr"]
        teamId = l['leader']["teamId"]

        week = l['leader']["week"]

        yards = l['leader']["yards"]
        inPlayDist = l['leader']["inPlayDist"]
        maxSpeed = l['leader']["maxSpeed"]

        player = Player(gsisId,shortName,playerName,jerseyNumber,position,teamAbbr,teamId,week,yards,inPlayDist,maxSpeed)
        players.append(player)
        #print("Player Name:",playerName)
        #print("Team Abbr:",teamAbbr)
        #print("In Play Distance:",inPlayDist)
        #print("Max Speed:",maxSpeed)
        #play
        #gameId = r['play']['gameId']
        #print("Game ID:",gameId)
        #print(r['play'])
def load_leaders(players):
    db = DatabaseDriver(file)
    db.connect()
    db.createDatabase()
    db.addPlayer(players)
    db.disconnect()
