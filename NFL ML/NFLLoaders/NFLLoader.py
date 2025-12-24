from databaseDriver import DatabaseDriver

def get_file():
    file = "../NFL_stats.sqlite"
    return file

def load_players(players):
    file = get_file()
    db = DatabaseDriver(file)
    db.connect()
    db.createDatabase()
    db.addPlayers(players)
    db.disconnect()

def load_ballCarriers(ballCarriers):
    file = get_file()
    db = DatabaseDriver(file)
    db.connect()
    db.createDatabase()
    db.addBallCarriers(ballCarriers)
    db.disconnect()

def load_longestPlays(longestPlays):
    file = get_file()
    db = DatabaseDriver(file)
    db.connect()
    db.createDatabase()
    db.addLongestPlays(longestPlays)
    db.disconnect()