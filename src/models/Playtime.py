from dataclasses import dataclass


@dataclass(frozen=True)
class Playtime:
    name: str
    description: str
    icon: str
