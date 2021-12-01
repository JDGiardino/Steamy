from dataclasses import dataclass


@dataclass(frozen=True)
class GameDetails:
    appid: int
    name: str
    developer: str
    publisher: str
    score_rank: int
    positive: int
    negative: int
    userscore: int
    owners: int
    average_forever: int
    average_2weeks: int
    median_forever: int
    median_2weeks: int
    price: int
    initialprice: int
    discount: int
    ccu: int
    languages: str
    genre: str
    tags: str
