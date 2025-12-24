from dataclasses import dataclass

@dataclass(order=True)
class BallCarrier:
    speed: float
    playType: str
    bcId: str
    gsisId: str
    playerName: str
    teamAbbr: str
    positionAbbr: str
    week: int
