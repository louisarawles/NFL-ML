from databaseDriver import DatabaseDriver

def get_file():
    file = "/Users/louisarawles/Desktop/Software Projects/NFL ML/NFL_stats.sqlite"
    return file

def load_players(players):
    file = get_file()
    db = DatabaseDriver(file)
    db.connect()
    db.createDatabase()
    db.addPlayers(players)
    db.commit()
    db.disconnect()

def load_ballCarriers(ballCarriers):
    file = get_file()
    db = DatabaseDriver(file)
    db.connect()
    db.createDatabase()
    db.addBallCarriers(ballCarriers)
    db.commit()
    db.disconnect()

def load_longestPlays(longestPlays):
    file = get_file()
    db = DatabaseDriver(file)
    db.connect()
    db.createDatabase()
    db.addLongestPlays(longestPlays)
    db.commit()
    db.disconnect()

def load_games(games):
    file = get_file()
    db = DatabaseDriver(file)
    db.connect()
    db.createDatabase()
    db.addGames(games)
    db.commit()
    db.disconnect()

def load_gameStats(gameStats):
    file = get_file()
    db = DatabaseDriver(file)
    db.connect()
    db.createDatabase()
    db.addGameStats(gameStats)
    db.commit()
    db.disconnect()