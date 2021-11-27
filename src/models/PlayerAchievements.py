from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerAchievements:
    unlocked: int
    total: int
