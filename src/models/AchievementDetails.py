from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class AchievementDetails:
    name: str
    defaultvalue: int
    displayName: str
    hidden: int
    icon: str
    icongray: str
    description: Optional[str] = field(default=None)
