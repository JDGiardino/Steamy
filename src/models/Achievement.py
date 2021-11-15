from dataclasses import dataclass


@dataclass(frozen=True)
class Achievement:
    name: str
    percent: float
