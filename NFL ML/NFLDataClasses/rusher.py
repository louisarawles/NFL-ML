from dataclasses import dataclass

@dataclass (order=True)
class Rusher:
    gameId: int
    esbId: str
    playerName: str
    rushYards: int
    touchdowns: int
    distance: float
    avgYards: float
    avgDistance: float
    avgTimeToLos: float
    rushLocationMap: object