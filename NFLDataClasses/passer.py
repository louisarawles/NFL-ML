from dataclasses import dataclass

@dataclass (order=True)
class Passer:
    gameId: int
    esbId: str
    playerName: str
    teamAbbr: str
    avg_completion_pct: float
    avg_yds: float
    avg_qbRating: float
    mode_lvl: str
    total_attempts: int
    total_completions: int
    total_tds: int
    total_yds: int
    total_interceptions: int
    zones: object
