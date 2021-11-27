from dataclasses import dataclass


@dataclass(frozen=True)
class RarestAchievement:
    name: str
    achievement: str
    description: str
    icon: str
