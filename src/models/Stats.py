from dataclasses import dataclass
from dataclasses import field
from typing import Optional


@dataclass(frozen=True)
class Stats:
    name: str
    description1: str
    description2: Optional[str] = field(default=None)
    icon: Optional[str] = field(default=None)
