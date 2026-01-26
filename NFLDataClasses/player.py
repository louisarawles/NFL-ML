class Player:
    plays = []
    topSpeeds = []
    def __init__(self,esbId,shortName,playerName,jerseyNumber,position,teamAbbr,teamId,week,yards,inPlayDist,maxSpeed):
        self.esbId = esbId
        self.shortName = shortName
        self.playerName = playerName
        self.jerseyNumber = jerseyNumber
        self.positionAbbr = position
        self.teamAbbr = teamAbbr
        self.teamId = teamId
        self.week = week
        self.yards = yards
        self.inPlayDist = inPlayDist
        self.maxSpeed = maxSpeed

    def add_plays(self, playId):
        self.plays.append(playId)