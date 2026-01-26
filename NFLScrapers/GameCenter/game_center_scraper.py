import requests
from NFLScrapers.GameCenter import encapsulate_game_stats as encaps
from NFLDataClasses.game import Game
from NFLDataClasses.gameStat import GameStat
from avg import avg

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

def get_gameTargets(gs_data):
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
    return passers, rushers, passRushers, receivers, leaders, speedLeaders, timeToSackLeaders, passDistanceLeaders

# get_gameStats violates every good principle of design but I need it out of main
# so this is what we've got for now
# fyi i dont use any of the lists of the data classes but if i wanted to later ig
def get_gameStats(gs_data, game, homeVisitor='home'):
    ##### declare variables #####
    ## game id
    g_id = game.gameId
    ## game avgs
    pr_avg = 0.0
    r_avg = 0.0
    ## QB variables declared & instantiated simultaneously
    ## rusher variables:
    distance = 0.0
    avgDistanceList = []
    avgTimeToLosList = []
    ## pass rusher variables
    blitzCount = 0
    avgSeparationToQbList = []
    tackles = 0
    assists = 0
    sacks = 0
    forcedFumbles = 0
    ## receiver variables:
    rec_yards = 0
    avgAirYardsList = []
    avgSeparationList = []
    receptions = 0
    ## leaders variables declared & instantiated simultaneously
    ##### END declare variables #####

    ##### handle invalid input errors #####
    if homeVisitor != 'home' and homeVisitor != 'visitor':
        print(f"Invalid home / visitor status for {homeVisitor}.")
        return None
    if game is None:
        print(f"Invalid game stats data for {game}.")
        return None
    err_GameStats = "Invalid game stats data."
    ##### END input error handling #####

    ##### get game targets #####
    passers, rushers, passRushers, receivers, leaders, speedLeaders, timeToSackLeaders, passDistanceLeaders = get_gameTargets(gs_data)
    # game avgs
    pr_avg = passRushers.get('avg')
    r_avg = receivers.get('avg')
    ##### END get game targets #####

    ##### handle game target errors #####
    if passers is None or rushers is None or passRushers is None or receivers is None or leaders is None or speedLeaders is None or timeToSackLeaders is None or passDistanceLeaders is None:
        print(err_GameStats)
        return None
    ##### END handle game target errors #####

    ##### home or visitor #####
    home = True
    team = game.homeTeamAbbr
    if homeVisitor == 'visitor':
        team = game.visitorTeamAbbr
        home = False
    ##### home or visitor #####

    ##### meta game data #####
    gs_id = f"{g_id}-{team}"
    outcome = "LOSS"
    if team == game.winnerAbbr:
        outcome = "WIN"
    ##### END meta game data #####

    ##### encaps QB #####
    QB = passers.get(homeVisitor)
    QB = encaps.encapsulate_passerZoneStats(QB)
    zones = QB.zones
    ABOVE = 0
    for zone in zones:
        if zone.get('qbRatingSuccessLevel') == 'ABOVE':
            ABOVE += 1
    totalCompletions = QB.total_completions
    QBavgRating = QB.avg_qbRating
    ##### END encaps QB #####

    ##### encaps team_rushers #####
    team_rushers = rushers.get(homeVisitor)
    rs = []
    for r in team_rushers:
        rusher = encaps.encapsulate_rusherZoneStats(g_id, r)
        rs.append(rusher)
        if not type(rusher) is str:
            distance += int(rusher.distance)
            avgDistanceList.append(rusher.avgDistance)
            avgTimeToLosList.append(rusher.avgTimeToLos)
    ## get avgs
    avgDistance = avg(avgDistanceList)
    avgTimeToLos = avg(avgTimeToLosList)
    ##### END encaps team_rushers #####

    ##### encaps pass rushers #####
    pass_rushers = passRushers.get(f"{homeVisitor}")
    prs = []
    for pr in pass_rushers:
        prusher = encaps.encapsulate_passRusherZoneStats(g_id, pr)
        prs.append(prusher)
        blitzCount += prusher.blitzCount
        avgSeparationToQbList.append(prusher.avgSeparationToQb)
        tackles += prusher.tackles
        assists += prusher.assists
        sacks += prusher.sacks
        forcedFumbles += prusher.forcedFumbles
    ## get avg
    avgSepToQB = avg(avgSeparationToQbList)
    ##### END encaps pass rushers #####

    ##### encaps receivers #####
    receivers = receivers.get(homeVisitor)
    recs = []
    for rec in receivers:
        receiver = encaps.encapsulate_receiverZoneStats(g_id, rec)
        recs.append(receiver)
    ## get avgs
    avgAirYards = avg(avgAirYardsList)
    avgSep = avg(avgSeparationList)
    ##### END encaps receivers #####

    ##### encaps leaders #####
    spl = speedLeaders.get(homeVisitor)
    if spl is not None:
        speedLeader = encaps.encapsulate_speedLeader(g_id, spl)
        if speedLeader is not None:
            maxSpeed = speedLeader.get('maxSpeed')
        else:
            maxSpeed = 0
    else:
        maxSpeed = 0

    tsl = timeToSackLeaders.get(homeVisitor)
    if tsl is not None:
        timeToSackLeader = encaps.encapsulate_timeToSackLeader(g_id, tsl)
        if timeToSackLeader is not None:
            timeToTackle = timeToSackLeader.get('timeToTackle')
        else:
            timeToTackle = 0
    else:
        timeToTackle = 0
    pdl = passDistanceLeaders.get(homeVisitor)
    passDistanceLeader = encaps.encapsulate_passDistanceLeader(g_id, pdl)
    if pdl is not None:
        if passDistanceLeader is not None:
            airDistance = passDistanceLeader.get('airDistance')
        else:
            airDistance = 0
    else:
        airDistance = 0
    ##### END encaps leaders #####

    ##### print section #####
    # for each in rs:
    #     print(f"{team} team_rushers: ", each)
    # for each in prs:
    #     print(f"{team} passRusher: ", each)
    # for each in recs:
    #     print(f"{team} receiver: ", each)
    # print(f"{team} speed leader: ", speedLeader)
    # print(f"{team} time-to-sack leader: ", timeToSackLeader)
    # print(f"{team} pass distance leader: ", passDistanceLeader)
    ##### END print section #####

    gameStat = GameStat(gameStatId=gs_id,gameId=g_id,teamAbbr=team,
                        home=home,outcome=outcome,QBABOVEzones=ABOVE,QBtotalCompletions=totalCompletions,
                        QBavgRating=QBavgRating,distance=distance,avgDistance=avgDistance,avgTimeToLos=avgTimeToLos,
                        blitzCount=blitzCount,avgSepToQB=avgSepToQB,tackles=tackles,assists=assists,sacks=sacks,forcedFumbles=forcedFumbles,
                        recYards=rec_yards,avgAirYards=avgAirYards,avgSep=avgSep,receptions=receptions,
                        maxSpeed=maxSpeed,timeToTackle=timeToTackle,airDistance=airDistance)
    return gameStat