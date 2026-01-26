from dataclasses import dataclass

@dataclass (order=True)
class PassRusher:
    gameId: int
    esbId: str
    playerName: str
    blitzCount: int
    avgSeparationToQb: float
    tackles: int
    assists: int
    sacks: int
    forcedFumbles: int