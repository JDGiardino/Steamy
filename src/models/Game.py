from dataclasses import dataclass


@dataclass(frozen=True)
class Game:
    name: str
    appid: int
