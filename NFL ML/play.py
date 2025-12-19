class Play:
    def __init__(self,playId,gameId,sequence,gameClock,startGameClock,endGameClock,down,
                quarter,isEndQuarter,timeOfDayUTC,homeScore,visitorScore,possessionTeamId,isBigPlay,isGoalToGo,isPenalty,
                isSTPlayer,isScoring,playDescription,playState,playStatsId,playType,preSnapHomeScore,preSnapVisitorScore,
                yardline,yardlineNumber,yardlineSide,yardsToGo,absoluteYardlineNumber,actualYardlineForFirstDown,
                actualYardsToGo,isChangeOfPossession,playDirection):
        self.playId = playId
        self.gameId = gameId
        self.sequence = sequence
        self.gameClock = gameClock
        self.startGameClock = startGameClock
        self.endGameClock = endGameClock
        self.down = down
        self.quarter = quarter
        self.isEndQuarter = isEndQuarter
        self.timeOfDayUTC = timeOfDayUTC
        self.homeScore = homeScore
        self.visitorScore = visitorScore
        self.possessionTeamId = possessionTeamId
        self.isBigPlay = isBigPlay
        self.isGoalToGo = isGoalToGo
        self.isPenalty = isPenalty
        self.isSTPlayer = isSTPlayer
        self.isScoring = isScoring
        self.playDescription = playDescription
        self.playState = playState
        self.playStatsId = playStatsId
        self.playType = playType
        self.preSnapHomeScore = preSnapHomeScore
        self.preSnapVisitorScore = preSnapVisitorScore
        self.yardline = yardline
        self.yardlineNumber = yardlineNumber
        self.yardlineSide = yardlineSide
        self.yardsToGo = yardsToGo
        self.absoluteYardlineNumber = absoluteYardlineNumber
        self.actualYardlineForFirstDown = actualYardlineForFirstDown
        self.actualYardsToGo = actualYardsToGo
        self.isChangeOfPossession = isChangeOfPossession
        self.playDirection = playDirection
