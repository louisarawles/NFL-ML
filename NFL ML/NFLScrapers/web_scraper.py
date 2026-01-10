import requests
from NFLDataClasses.player import Player

def get_params(season,seasonType,week):
    params = {
        "season":season,
        "seasonType":seasonType,
        "week":week
    }
    return params

def get_headers_playerStats():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://nextgenstats.nfl.com",
    }
    return headers

def get_headers_gameCenter():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://nextgenstats.nfl.com/stats/game-center-index",
    }
    return headers

def get_data(url,headers,params=None):
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    # print(data.keys())
    return data

def get_leaders(data):
    leaders = data["leaders"]
    return leaders


def scrape_players(leaders):
    players = []
    for l in leaders:
        leader = l.get('leader', {})
        esbId = leader.get("esbId")
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

        player = Player(esbId, shortName, playerName, jerseyNumber, position, teamAbbr, teamId, week, yards,
                        inPlayDist, speed)
        players.append(player)
    return players


def scrape_plays(leaders):
    plays = []
    for l in leaders:
        p = l.get('play',{})
        gameId = p.get('gameId')


        playId = p.get('playId')
        sequence = p.get('sequence')
        down = p.get('down')
        gameClock = p.get('gameClock')
        gameKey = p.get('gameKey')
        health = p.get('health')
        homeScore = p.get('homeScore')
        isBigPlay = p.get('isBigPlay')
        isEndQuarter = p.get('isEndQuarter')
        isGoalToGo = p.get('isGoalToGo')
        isPenalty = p.get('isPenalty')
        isSTPlay = p.get('isSTPlay')
        isScoring = p.get('isScoring')
        playDescription = p.get('playDescription')
        playState = p.get('playState')
        playStats = p.get('playStats')
        playType = p.get('playType')
        playTypeCode = p.get('playTypeCode')
        possessionTeamId = p.get('possessionTeamId')
        preSnapHomeScore = p.get('preSnapHomeScore')
        preSnapVisitorScore = p.get('preSnapVisitorScore')
        quarter = p.get('quarter')
        #timeOfDayUTC =p.get('timeOfDayUTC')
        visitorScore = p.get('visitorScore')
        yardline = p.get('yardline')
        yardlineNumber = p.get('yardlineNumber')
        yardlineSide = p.get('yardlineSide')
        yardsToGo = p.get('yardsToGo')
        absoluteYardlineNumber = p.get('absoluteYardlineNumber')
        actualYardlineForFirstDown = p.get('actualYardlineForFirstDown')
        actualYardsToGo = p.get('actualYardsToGo')
        endGameClock = p.get('endGameClock')
        isChangeOfPossession = p.get('isChangeOfPossession')
        playDirection = p.get('playDirection')
        startGameClock = p.get('startGameClock')