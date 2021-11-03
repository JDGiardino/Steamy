from dataclasses import dataclass


@dataclass(frozen=True)
class Players:
    player_count: int
    result: int
