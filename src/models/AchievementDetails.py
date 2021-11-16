from dataclasses import dataclass


@dataclass(frozen=True)
class AchievementDetails:
    name: str
    defaultvalue: int
    displayName: str
    hidden: int
    description: str
    icon: str
    icongray: str
