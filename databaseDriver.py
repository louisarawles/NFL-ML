import sqlite3

from NFLDataClasses.ballCarrier import BallCarrier


class DatabaseDriver:

    def __init__(self, sqliteFilename):
        self.cursor = None
        self.sqliteConnection = None
        self.sqliteFilename = sqliteFilename

    def connect(self):
        try:
            # Connect to SQLite Database and create a cursor
            self.sqliteConnection = sqlite3.connect(self.sqliteFilename)
            self.cursor = self.sqliteConnection.cursor()
            # print('DB Init')

        except sqlite3.Error as error:
            print('Error occurred -', error)

    def commit(self):
        self.sqliteConnection.commit()

    def rollback(self):
        self.sqliteConnection.rollback()

    def disconnect(self):
        self.cursor.close()
        self.sqliteConnection.close()

    def createDatabase(self):
        queryCreatePlayer = """CREATE TABLE IF NOT EXISTS Player
                               (
                                   esbId       VARCHAR,
                                   shortName    VARCHAR,
                                   playerName   VARCHAR,
                                   jerseyNumber INT,
                                   positionAbbr VARCHAR,
                                   teamAbbr     VARCHAR,
                                   teamId       INT,
                                   PRIMARY KEY (esbId)
                               )"""

        queryCreateTeam = """CREATE TABLE IF NOT EXISTS Team
                         (
                             teamId   INT,
                             teamAbbr VARCHAR,
                             PRIMARY KEY (teamId)
                         )"""

        # queryCreateGame = """CREATE TABLE IF NOT EXISTS Game
        #                  (
        #                      week INT,
        #                      gameDate VARCHAR,
        #                      gameId        INT,
        #                      homeTeamAbbr VARCHAR,
        #                      visitorTeamAbbr VARCHAR,
        #                      homeScore    INT,
        #                      visitorScore    INT,
        #                      winnerAbbr VARCHAR,
        #                      PRIMARY KEY (gameId),
        #                      FOREIGN KEY (homeTeamAbbr) REFERENCES Team (teamAbbr),
        #                      FOREIGN KEY (visitorTeamAbbr) REFERENCES Team (teamAbbr)
        #                  )"""

        queryCreateGameStats = """CREATE TABLE IF NOT EXISTS GameStats(
            gameStatId VARCHAR NOT NULL,
            gameId INT,
            teamAbbr VARCHAR,
            home BOOLEAN,
            outcome VARCHAR,
            QBABOVEzones INT,
            QBtotalCompletions INT,
            QBavgRating FLOAT,
            distance FLOAT,
            avgDistance FLOAT,
            avgTimeToLos FLOAT,
            blitzCount INT,
            avgSepToQB FLOAT,
            tackles INT,
            assists INT,
            sacks INT,
            forcedFumbles INT,
            recYards INT,
            avgAirYards FLOAT,
            avgSep FLOAT,
            receptions INT,
            maxSpeed FLOAT,
            timeToTackle FLOAT,
            airDistance FLOAT,
            PRIMARY KEY (gameStatId),
            FOREIGN KEY (gameId) REFERENCES Game (gameId)
                                  )"""

        queryCreatePlay = """CREATE TABLE IF NOT EXISTS Play
                         (
                             playId                     INT,
                             gameId                     INT,
                             sequence                   INT,

                             gameClock                  VARCHAR,
                             startGameClock             VARCHAR,
                             endGameClock               VARCHAR,

                             down                       INT,
                             quarter                    INT,
                             isEndQuarter               BOOLEAN,
                             timeOfDayUTC               VARCHAR,
                             homeScore                  INT,
                             visitorScore               INT,
                             possessionTeamId           INT,

                             isBigPlay                  BOOLEAN,
                             isGoalToGo                 BOOLEAN,
                             isPenalty                  BOOLEAN,
                             isSTPlayer                 BOOLEAN,
                             isScoring                  BOOLEAN,

                             playDescription            VARCHAR,
                             playState                  VARCHAR,
                             playStatsId                VARCHAR NOT NULL,

                             playType                   VARCHAR NOT NULL,

                             preSnapHomeScore           INT,
                             preSnapVisitorScore        INT,

                             yardline                   VARCHAR,
                             yardlineNumber             INT,
                             yardlineSide               VARCHAR,
                             yardsToGo                  INT,

                             absoluteYardlineNumber     INT,
                             actualYardlineForFirstDown INT,
                             actualYardsToGo            INT,

                             isChangeOfPossession       BOOLEAN,
                             playDirection              VARCHAR,
                             PRIMARY KEY (playId),
                             FOREIGN KEY (gameId) REFERENCES Game (gameId),
                             FOREIGN KEY (possessionTeamId) REFERENCES Team (teamId)
                         ) \
                      """

        queryCreatePlayStats = """CREATE TABLE IF NOT EXISTS PlayStats
                              (
                                  playStatsId VARCHAR NOT NULL,
                                  statId      INT,
                                  playId      INT,
                                  esbId      VARCHAR,
                                  health      VARCHAR,
                                  clubCode    VARCHAR,
                                  playerName  VARCHAR,
                                  yards       INT,
                                  PRIMARY KEY (playStatsId),
                                  FOREIGN KEY (esbId) REFERENCES Player (esbId)
                              ) \
                           """

        # i might want to use this instead of playType later to take up less space but tbd
        queryCreatePlayType = """CREATE TABLE IF NOT EXISTS PlayType
                             (
                                 playTypeCode INT,
                                 playType     VARCHAR NOT NULL,
                                 PRIMARY KEY (playTypeCode)
                             ) \
                          """
        queryCreateBallCarriers = """CREATE TABLE IF NOT EXISTS BallCarriers(
        bcId VARCHAR NOT NULL,
        esbId VARCHAR NOT NULL,
        playerName VARCHAR,
        teamAbbr VARCHAR,
        positionAbbr VARCHAR,
        speed FLOAT,
        week INT,
        playType VARCHAR,
        PRIMARY KEY (bcId))"""

        queryCreateLongestPlays = """CREATE TABLE IF NOT EXISTS LongestPlays(
            lpId VARCHAR NOT NULL,
            esbId VARCHAR NOT NULL,
            playerName VARCHAR,
            teamAbbr VARCHAR,
            positionAbbr VARCHAR,
            distance FLOAT,
            week INT,
            playType VARCHAR,
            PRIMARY KEY (lpId))"""
        try:
            # print("Connection established")
            self.cursor.execute(queryCreatePlayer)
            self.cursor.execute(queryCreateTeam)
            # self.cursor.execute(queryCreateGame)
            self.cursor.execute(queryCreateGameStats)
            self.cursor.execute(queryCreatePlay)
            self.cursor.execute(queryCreatePlayStats)
            self.cursor.execute(queryCreatePlayType)
            self.cursor.execute(queryCreateBallCarriers)
            self.cursor.execute(queryCreateLongestPlays)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)

    def addPlayer(self,p):
        if not p:
            return
        try:
            data = (p.esbId, p.shortName, p.playerName, p.jerseyNumber, p.positionAbbr, p.teamAbbr, p.teamId)

            insertQuery = """INSERT OR IGNORE INTO Player(esbId,shortName,playerName,jerseyNumber,positionAbbr,teamAbbr,teamId)
                                  VALUES (?,?,?,?,?,?,?)"""
            self.cursor.execute(insertQuery,data)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)

    def addPlayers(self,players):
        if not players:
            return
        try:
            data = [
                (p.esbId,
                 p.shortName,
                 p.playerName,
                 p.jerseyNumber,
                 p.positionAbbr,
                 p.teamAbbr,
                 p.teamId)
                for p in players
            ]
            insertQuery = """INSERT OR IGNORE INTO Player(esbId,shortName,playerName,jerseyNumber,positionAbbr,teamAbbr,teamId)
                                  VALUES (?,?,?,?,?,?,?)"""
            self.cursor.executemany(insertQuery,data)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)
    def addBallCarriers(self, ballCarriers):
        if not ballCarriers:
            return
        try:
            data = [
                (bc.bcId,
                bc.esbId,
                bc.playerName,
                bc.teamAbbr,
                bc.positionAbbr,
                bc.speed,
                bc.week,
                bc.playType)
                for bc in ballCarriers
            ]
            insertQuery = """INSERT OR IGNORE INTO BallCarriers(
            bcId,esbId,playerName,teamAbbr,positionAbbr,speed,week,playType) VALUES (?,?,?,?,?,?,?,?)"""
            self.cursor.executemany(insertQuery, data)

        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)

    def getBallCarriers_bySpeed(self):
        ballCarriers = []
        try:
            query = """SELECT bcId, playerName, teamAbbr, positionAbbr, speed, week, playType 
                       FROM BallCarriers
                    ORDER BY speed DESC"""
            rs = self.cursor.execute(query)
            for row in rs:
                bcId = row[0]
                esbId = row[1]
                playerName = row[2]
                teamAbbr = row[3]
                positionAbbr = row[4]
                speed = row[5]
                week = row[6]
                playType = row[7]
                bc = BallCarrier(bcId=bcId,esbId=esbId,playerName=playerName,teamAbbr=teamAbbr,positionAbbr=positionAbbr,speed=speed,week=week,playType=playType)
                #print(bc)
                ballCarriers.append(bc)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)
        else:
            return ballCarriers

    def addLongestPlays(self, plays):
        if not plays:
            return
        try:
            data = [
                (
                p.lpId,
                p.esbId,
                p.playerName,
                p.teamAbbr,
                p.positionAbbr,
                p.distance,
                p.week,
                p.playType)
                for p in plays
            ]
            insertQuery = """INSERT OR IGNORE INTO LongestPlays(lpId,esbId,playerName,teamAbbr,positionAbbr,distance,week,playType)
                          VALUES (?,?,?,?,?,?,?,?)"""
            self.cursor.executemany(insertQuery, data)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)

    def addTeams(self,teams):
        if not teams:
            return
        try:
            data = [
                (t.teamId, t.teamAbbr)
                for t in teams
            ]
            insertQuery = """INSERT OR IGNORE INTO Team(teamId, teamAbbr)
                                  VALUES (?,?)"""
            self.cursor.executemany(insertQuery, data)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)

    def addGames(self,games):
        if not games:
            return
        try:
            data = [
                (g.week,g.gameDate,g.gameId, g.homeTeamAbbr, g.visitorTeamAbbr, g.homeScore, g.visitorScore,g.winnerAbbr)
                for g in games
            ]
            insertQuery = """INSERT INTO Game(week, gameDate, gameId, homeTeamAbbr, visitorTeamAbbr, homeScore, visitorScore, winnerAbbr)
                                    VALUES (?,?,?,?,?,?,?,?)"""
            self.cursor.executemany(insertQuery, data)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)

    def addGameStats(self,gs):
        if not gs:
            return
        try:
            data = (
                gs.gameStatId,
            gs.gameId,
            gs.teamAbbr,
            gs.home,
            gs.outcome,
            gs.QBABOVEzones,
            gs.QBtotalCompletions,
            gs.QBavgRating,
            gs.distance,
            gs.avgDistance,
            gs.avgTimeToLos,
            gs.blitzCount,
            gs.avgSepToQB,
            gs.tackles,
            gs.assists,
            gs.sacks,
            gs.forcedFumbles,
            gs.recYards,
            gs.avgAirYards,
            gs.avgSep,
            gs.receptions,
            gs.maxSpeed,
            gs.timeToTackle,
            gs.airDistance
                    )

            insertQuery = """INSERT OR IGNORE INTO GameStats(
            gameStatId,
            gameId,
            teamAbbr,
            home,
            outcome,
            QBABOVEzones,
            QBtotalCompletions,
            QBavgRating,
            distance,
            avgDistance,
            avgTimeToLos,
            blitzCount,
            avgSepToQB,
            tackles,
            assists,
            sacks,
            forcedFumbles,
            recYards,
            avgAirYards,
            avgSep,
            receptions,
            maxSpeed,
            timeToTackle,
            airDistance)
                                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            self.cursor.execute(insertQuery, data)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)

    def getGameStats_ALL(self):
        try:
            query = """SELECT * FROM GameStats"""
            rs = self.cursor.execute(query)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)
        else:
            return rs

    # def getGameStats_FEATURES(self,features):
    #     try:
    #         query = f"""SELECT {features} FROM GameStats"""
    #         features_rs = self.cursor.execute(query)
    #     except sqlite3.Error as error:
    #         self.sqliteConnection.rollback()
    #         print("Error occurred: ", error)
    #     else:
    #         return features_rs
    #
    # def getGameStats_TARGET(self,target):
    #     try:
    #         query = f"""SELECT {target} FROM GameStats"""
    #         target_rs = self.cursor.execute(query)
    #     except sqlite3.Error as error:
    #         self.sqliteConnection.rollback()
    #         print("Error occurred: ", error)
    #     else:
    #         return target_rs

    def addPlays(self,plays):
        if not plays:
            return
        try:
            data = [
                (p.playId, p.gameId, p.sequence, p.gameClock, p.startGameClock, p.endGameClock, p.down,
                 p.quarter, p.isEndQuarter, p.timeOfDayUTC, p.homeScore, p.visitorScore, p.possessionTeamId,
                 p.isBigPlay, p.isGoalToGo, p.isPenalty,
                 p.isSTPlayer, p.isScoring, p.playDescription, p.playState, p.playStatsId, p.playType,
                 p.preSnapHomeScore, p.preSnapVisitorScore,
                 p.yardline, p.yardlineNumber, p.yardlineSide, p.yardsToGo, p.absoluteYardlineNumber,
                 p.actualYardlineForFirstDown,
                 p.actualYardsToGo, p.isChangeOfPossession, p.playDirection)
                for p in plays
            ]
            insertQuery = """INSERT INTO Play(playId,gameId,sequence,gameClock,startGameClock,endGameClock,down,
                quarter,isEndQuarter,timeOfDayUTC,homeScore,visitorScore,possessionTeamId,isBigPlay,isGoalToGo,isPenalty,
                isSTPlayer,isScoring,playDescription,playState,playStatsId,playType,preSnapHomeScore,preSnapVisitorScore,
                yardline,yardlineNumber,yardlineSide,yardsToGo,absoluteYardlineNumber,actualYardlineForFirstDown,
                actualYardsToGo,isChangeOfPossession,playDirection) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,?)"""
            self.cursor.executemany(insertQuery, data)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)

    def addPlayStats(self,playStats):
        if not playStats:
            return
        try:
            data = [
                (p.playStatsId,
                 p.statId,
                 p.playId,
                 p.esbId,
                 p.health,
                 p.clubCode,
                 p.playerName,
                 p.yards)
                for p in playStats
            ]
            insertQuery = """INSERT INTO PlayStats(playStatsId, statId, playId, esbId, health, clubCode, 
            playerName, yards) VALUES (?,?,?,?,?,?,?,?)"""
            self.cursor.executemany(insertQuery, data)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)