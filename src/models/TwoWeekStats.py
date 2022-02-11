from dataclasses import dataclass


@dataclass(frozen=True)
class TwoWeekStats:
    two_week_playtime: float
    two_week_games: list
