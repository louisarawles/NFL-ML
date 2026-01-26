from dataclasses import dataclass

@dataclass (order=True)
class Game:
    week: int
    seasonType: str
    gameDate: str
    gameId: int
    homeTeamAbbr: str
    visitorTeamAbbr: str
    homeScore: int
    visitorScore: int
    winnerAbbr: str