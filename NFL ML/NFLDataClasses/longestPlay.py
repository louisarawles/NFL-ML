from dataclasses import dataclass

@dataclass(order=True)
class LongestPlay:
    distance: float
    playType: str
    lpId: str
    esbId: str
    playerName: str
    teamAbbr: str
    positionAbbr: str
    week: int
