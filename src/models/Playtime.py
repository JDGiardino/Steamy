from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Playtime:
    appid: int
    playtime_forever: int
    playtime_windows_forever: int
    playtime_mac_forever: int
    playtime_linux_forever: int
    playtime_2weeks: Optional[int] = field(default=None)
