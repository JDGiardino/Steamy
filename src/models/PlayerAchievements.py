from dataclasses import dataclass
from dataclasses import field
from typing import Optional


@dataclass(frozen=True)
class PlayerAchievements:
    unlocked: int
    total: int
    game_name: Optional[str] = field(default=None)
    status: Optional[str] = field(default=None)
