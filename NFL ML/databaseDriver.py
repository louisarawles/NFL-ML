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
            print('DB Init')

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
                                   gsisId       VARCHAR,
                                   shortName    VARCHAR,
                                   playerName   VARCHAR,
                                   jerseyNumber INT,
                                   positionAbbr VARCHAR,
                                   teamAbbr     VARCHAR,
                                   teamId       INT,
                                   PRIMARY KEY (gsisId)
                               )"""

        queryCreateTeam = """CREATE TABLE IF NOT EXISTS Team
                         (
                             teamId   INT,
                             teamAbbr VARCHAR,
                             PRIMARY KEY (teamId)
                         )"""

        queryCreateGame = """CREATE TABLE IF NOT EXISTS Game
                         (
                             gameId        INT,
                             homeTeamId    INT,
                             visitorTeamId INT,
                             homeScore    INT,
                             visitorScore    INT,
                             PRIMARY KEY (gameId),
                             FOREIGN KEY (homeTeamId) REFERENCES Team (teamId),
                             FOREIGN KEY (visitorTeamId) REFERENCES Team (teamId)
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
                                  gsisId      VARCHAR,
                                  health      VARCHAR,
                                  clubCode    VARCHAR,
                                  playerName  VARCHAR,
                                  yards       INT,
                                  PRIMARY KEY (playStatsId),
                                  FOREIGN KEY (gsisId) REFERENCES Player (gsisId)
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
        gsisId VARCHAR NOT NULL,
        playerName VARCHAR,
        teamAbbr VARCHAR,
        positionAbbr VARCHAR,
        speed FLOAT,
        week INT,
        playType VARCHAR,
        PRIMARY KEY (bcId))"""

        queryCreateLongestPlays = """CREATE TABLE IF NOT EXISTS LongestPlays(
            lpId VARCHAR NOT NULL,
            gsisId VARCHAR NOT NULL,
            playerName VARCHAR,
            teamAbbr VARCHAR,
            positionAbbr VARCHAR,
            distance FLOAT,
            week INT,
            playType VARCHAR,
            PRIMARY KEY (lpId))"""
        try:
            print("Connection established")
            self.cursor.execute(queryCreatePlayer)
            self.cursor.execute(queryCreateTeam)
            self.cursor.execute(queryCreateGame)
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
            data = (p.gsisId, p.shortName, p.playerName, p.jerseyNumber, p.positionAbbr, p.teamAbbr, p.teamId)

            insertQuery = """INSERT OR IGNORE INTO Player(gsisId,shortName,playerName,jerseyNumber,positionAbbr,teamAbbr,teamId)
                                  VALUES (?,?,?,?,?,?,?)"""
            self.cursor.execute(insertQuery,data)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)
        else:
            self.sqliteConnection.commit()

    def addPlayers(self,players):
        if not players:
            return
        try:
            data = [
                (p.gsisId,
                 p.shortName,
                 p.playerName,
                 p.jerseyNumber,
                 p.positionAbbr,
                 p.teamAbbr,
                 p.teamId)
                for p in players
            ]
            insertQuery = """INSERT OR IGNORE INTO Player(gsisId,shortName,playerName,jerseyNumber,positionAbbr,teamAbbr,teamId)
                                  VALUES (?,?,?,?,?,?,?)"""
            self.cursor.executemany(insertQuery,data)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)
        else:
            self.sqliteConnection.commit()

    def addBallCarriers(self, ballCarriers):
        if not ballCarriers:
            return
        try:
            # currBallCarriers = self.getBallCarriers_bySpeed()
            # if len(currBallCarriers) < 1:
            #     bcs = ballCarriers
            #     #sortedbc = sorted(ballCarriers, key=lambda bc: bc.speed, reverse=True)
            # else:
            #     for bc in ballCarriers:
            #         if bc not in currBallCarriers:
            #             currBallCarriers.append(bc)
            #     bcs = currBallCarriers
                #sortedbc = sorted(currBallCarriers, key=lambda bc: bc.speed, reverse=True)
            data = [
                (bc.bcId,
                bc.gsisId,
                bc.playerName,
                bc.teamAbbr,
                bc.positionAbbr,
                bc.speed,
                bc.week,
                bc.playType)
                for bc in ballCarriers
            ]
            insertQuery = """INSERT OR IGNORE INTO BallCarriers(
            bcId,gsisId,playerName,teamAbbr,positionAbbr,speed,week,playType) VALUES (?,?,?,?,?,?,?,?)"""
            self.cursor.executemany(insertQuery, data)

        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)
        else:
            self.sqliteConnection.commit()

    def getBallCarriers_bySpeed(self):
        ballCarriers = []
        try:
            query = """SELECT bcId, playerName, teamAbbr, positionAbbr, speed, week, playType 
                       FROM BallCarriers
                    ORDER BY speed DESC"""
            rs = self.cursor.execute(query)
            for row in rs:
                bcId = row[0]
                gsisId = row[1]
                playerName = row[2]
                teamAbbr = row[3]
                positionAbbr = row[4]
                speed = row[5]
                week = row[6]
                playType = row[7]
                bc = BallCarrier(bcId=bcId,gsisId=gsisId,playerName=playerName,teamAbbr=teamAbbr,positionAbbr=positionAbbr,speed=speed,week=week,playType=playType)
                #print(bc)
                ballCarriers.append(bc)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)
        else:
            return ballCarriers

    def addLongestPlays(self, plays):
        longestPlays = []
        if not plays:
            return
        try:
            data = [
                (
                p.lpId,
                p.gsisId,
                p.playerName,
                p.teamAbbr,
                p.positionAbbr,
                p.distance,
                p.week,
                p.playType)
                for p in plays
            ]
            insertQuery = """INSERT OR IGNORE INTO LongestPlays(lpId,gsisId,playerName,teamAbbr,positionAbbr,distance,week,playType)
                          VALUES (?,?,?,?,?,?,?,?)"""
            self.cursor.executemany(insertQuery, data)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)
        else:
            self.sqliteConnection.commit()

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
        else:
            self.sqliteConnection.commit()

    def addGames(self,game):
        if not game:
            return
        try:
            data = [
                (g.gameId, g.homeTeamId, g.visitorTeamId, g.homeScore, g.visitorScore)
                for g in game
            ]
            insertQuery = """INSERT INTO Game(gameId, homeTeamId, visitorTeamId, homeScore, visitorScore)
                                    VALUES (?,?,?,?,?)"""
            self.cursor.executemany(insertQuery, data)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)

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
        else:
            self.sqliteConnection.commit()

    def addPlayStats(self,playStats):
        if not playStats:
            return
        try:
            data = [
                (p.playStatsId,
                 p.statId,
                 p.playId,
                 p.gsisId,
                 p.health,
                 p.clubCode,
                 p.playerName,
                 p.yards)
                for p in playStats
            ]
            insertQuery = """INSERT INTO PlayStats(playStatsId, statId, playId, gsisId, health, clubCode, 
            playerName, yards) VALUES (?,?,?,?,?,?,?,?)"""
            self.cursor.executemany(insertQuery, data)
        except sqlite3.Error as error:
            self.sqliteConnection.rollback()
            print("Error occurred: ", error)
        else:
            self.sqliteConnection.commit()