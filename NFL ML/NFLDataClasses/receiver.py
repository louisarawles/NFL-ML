from dataclasses import dataclass

@dataclass (order=True)
class Receiver:
    gameId: int
    esbId: str
    playerName: str
    recYards: int
    avgAirYards: float
    avgCushion: float
    avgSeparation: float
    targets: int
    receptions: int
    touchdowns: int