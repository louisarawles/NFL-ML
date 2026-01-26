#****************************** GAME FINDER ******************************#
# This file contains functions that take arguments to filter a list of games
# ONLY until I input the games into a table the way I want to
# and then will add these to database driver in SQLite form
# it will probably still be useful though even at that point (ie testing?)
# so it may stick around


# caller function
def findGames(games,teamAbbr1=None,teamAbbr2=None,seasonType=None,week=None):
    if teamAbbr1:
        if seasonType is None and week is None:
            return findGames_teams(games,teamAbbr1,teamAbbr2)
        elif seasonType is not None and week is None:
            return findGames_teams_seasonType(games,teamAbbr1,seasonType,teamAbbr2)
        elif seasonType is not None and week is not None:
            return findGames_teams_seasonType_week(games,teamAbbr1,seasonType,week,teamAbbr2)
        else:
            return findGames_teams_week(games,teamAbbr1,week,teamAbbr2)
    elif seasonType:
        if week is None:
            return findGames_seasonType(games,seasonType)
        else:
            return findGames_seasonType_week(games,seasonType,week)
    else:
        return findGames_week(games,week)

# find games by one or two teams
def findGames_teams(games,teamAbbr1, teamAbbr2=None):
    found_games = []
    if teamAbbr2 is None:
        for g in games:
            if g.homeTeamAbbr == teamAbbr1 or g.visitorTeamAbbr == teamAbbr1:
                found_games.append(g)
        if len(found_games) <= 0:
            return f"No games found for team {teamAbbr1}."
    else:
        for g in games:
            if (g.homeTeamAbbr == teamAbbr1 or g.visitorTeamAbbr == teamAbbr1) and (
                    g.homeTeamAbbr == teamAbbr2 or g.visitorTeamAbbr == teamAbbr2):
                found_games.append(g)
        if len(found_games) <= 0:
            return f"No games found with teams {teamAbbr1} and {teamAbbr2}."
    return found_games

# find games by season type
def findGames_seasonType(games,seasonType):
    if (seasonType != 'REG') and (seasonType != 'PRE') and (seasonType != 'POST'):
        return f"Invalid seasonType: {seasonType}. Valid seasonTypes: REG, PRE, POST."
    found_games = []
    for g in games:
        if g.seasonType == seasonType:
            found_games.append(g)
    if len(found_games) <= 0:
        return f"No games found for season type: {seasonType}."
    return found_games

# find games by week
def findGames_week(games,week):
    found_games = []
    for g in games:
        if g.week == week:
            found_games.append(g)
    if len(found_games) <= 0:
        return f"No games found for week {week}."
    return found_games

# find games by team(s) and season type
def findGames_teams_seasonType(games,teamAbbr1,seasonType,teamAbbr2):
    if (seasonType != 'REG') and (seasonType != 'PRE') and (seasonType != 'POST'):
        return f"Invalid seasonType: {seasonType}. Valid seasonTypes: REG, PRE, POST."
    found_games = []
    if teamAbbr2 is None:
        for g in games:
            if (g.homeTeamAbbr == teamAbbr1 or g.visitorTeamAbbr == teamAbbr1) and (g.seasonType == seasonType):
                found_games.append(g)
        if len(found_games) <= 0:
            return f"No games found for team {teamAbbr1} and season type {seasonType}."
    else:
        for g in games:
            if (g.homeTeamAbbr == teamAbbr1 or g.visitorTeamAbbr == teamAbbr1) and (
                    g.homeTeamAbbr == teamAbbr2 or g.visitorTeamAbbr == teamAbbr2) and (g.seasonType == seasonType):
                found_games.append(g)
        if len(found_games) <= 0:
            return f"No games found for teams {teamAbbr1} and {teamAbbr2} and season type {seasonType}."
    return found_games

# find games by team(s) and week
def findGames_teams_week(games,teamAbbr1,week,teamAbbr2=None):
    found_games = []
    if teamAbbr2 is None:
        for g in games:
            if (g.homeTeamAbbr == teamAbbr1 or g.visitorTeamAbbr == teamAbbr1) and (g.week == week):
                found_games.append(g)
        if len(found_games) <= 0:
            return f"No games found for team {teamAbbr1} and week {week}."
    else:
        for g in games:
            if (g.homeTeamAbbr == teamAbbr1 or g.visitorTeamAbbr == teamAbbr1) and (
                    g.homeTeamAbbr == teamAbbr2 or g.visitorTeamAbbr == teamAbbr2) and (g.week == week):
                found_games.append(g)
        if len(found_games) <= 0:
            return f"No games found for teams {teamAbbr1} and {teamAbbr2} and week {week}."
    return found_games

# find games by season type and week
def findGames_seasonType_week(games,seasonType,week,):
    found_games = []
    for g in games:
        if g.seasonType == seasonType and g.week == week:
            found_games.append(g)
    if len(found_games) <= 0:
        return f"No games found for season type {seasonType} and week {week}."
    return found_games

# find games by team(s), season type, and week
def findGames_teams_seasonType_week(games,teamAbbr1,seasonType,week,teamAbbr2=None):
    found_games = []
    if teamAbbr2 is None:
        for g in games:
            if ((g.homeTeamAbbr == teamAbbr1 or g.visitorTeamAbbr == teamAbbr1) and
                    (g.seasonType == seasonType) and (g.week == week)):
                found_games.append(g)
        if len(found_games) <= 0:
            return f"No games found for team {teamAbbr1}, season type {seasonType}, and week {week}."
    else:
        for g in games:
            if ((g.homeTeamAbbr == teamAbbr1 or g.visitorTeamAbbr == teamAbbr1) and (
                    g.homeTeamAbbr == teamAbbr2 or g.visitorTeamAbbr == teamAbbr2) and
                    (g.seasonType == seasonType) and (g.week == week)):
                found_games.append(g)
        if len(found_games) <= 0:
            return f"No games found for teams {teamAbbr1} and {teamAbbr2}, season type {seasonType}, and week {week}."
    return found_games