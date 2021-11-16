from dataclasses import dataclass


@dataclass(frozen=True)
class AchievementPercent:
    name: str
    percent: float
