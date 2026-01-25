from dataclasses import dataclass

@dataclass(order=True)
class GameStat:
    gameStatId: str
    gameId: int
    teamAbbr: str
    home: bool
    outcome: str
    QBABOVEzones: int
    QBtotalCompletions: int
    QBavgRating: float
    distance: float
    avgDistance: float
    avgTimeToLos: float
    blitzCount: int
    avgSepToQB: float
    tackles: int
    assists: int
    sacks: int
    forcedFumbles: int
    recYards: int
    avgAirYards: float
    avgSep: float
    receptions: int
    maxSpeed: float
    timeToTackle: float
    airDistance: float