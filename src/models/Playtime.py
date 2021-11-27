from dataclasses import dataclass


@dataclass(frozen=True)
class Playtime:
    appid: int
    playtime_2weeks: int
    playtime_forever: int
    playtime_windows_forever: int
    playtime_mac_forever: int
    playtime_linux_forever: int
