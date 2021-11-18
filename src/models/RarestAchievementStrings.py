from dataclasses import dataclass


@dataclass(frozen=True)
class RarestAchievementStrings:
    name: str
    achievement: str
    description: str
    icon: str
