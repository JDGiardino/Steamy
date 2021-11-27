from dataclasses import dataclass


@dataclass(frozen=True)
class Stats:
    name: str
    description1: str
    description2: str
    icon: str
