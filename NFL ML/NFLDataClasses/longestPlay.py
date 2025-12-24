from dataclasses import dataclass

@dataclass(order=True)
class DistancePlay:
    distance: float
    playType: str
    lpId: str
    gsisId: str
    playerName: str
    teamAbbr: str
    positionAbbr: str
    week: int
