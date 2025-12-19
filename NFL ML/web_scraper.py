import player
import requests
from bs4 import BeautifulSoup

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

print(data.keys())

rows = data["leaders"]

players = []
for r in rows:
    #leader
    #nflId = r['leader']["nflId"]
    #esbId = r['leader']["esbId"]
    #gsis primary official identifier
    gsisId = r['leader']["gsisId"]

    #firstName = r['leader']["firstName"]
    #lastName = r['leader']["lastName"]
    shortName = r['leader']["shortName"]
    playerName = r['leader']["playerName"]

    jerseyNumber = r['leader']["jerseyNumber"]

    position = r['leader']["position"]
    positionGroup = r['leader']["positionGroup"]

    teamAbbr = r['leader']["teamAbbr"]
    teamId = r['leader']["teamId"]

    week = r['leader']["week"]

    yards = r['leader']["yards"]
    inPlayDist = r['leader']["inPlayDist"]
    maxSpeed = r['leader']["maxSpeed"]

    player = player.Player(gsisId,shortName,playerName,jerseyNumber,position,teamAbbr,teamId,week,yards,inPlayDist,maxSpeed)
    players.append(player)

    #print("Player Name:",playerName)
    #print("Team Abbr:",teamAbbr)
    #print("In Play Distance:",inPlayDist)
    #print("Max Speed:",maxSpeed)
    #play
    #gameId = r['play']['gameId']
    #print("Game ID:",gameId)
    #print(r['play'])


print(len(rows))
print(rows[0])
