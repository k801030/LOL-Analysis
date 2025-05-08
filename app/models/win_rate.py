from dataclasses import dataclass, field
from typing import Dict

from models.kda import Kda


@dataclass
class WinRate:
    title: str
    kda: Kda = field(default_factory=Kda)
    win_count: int = 0
    lose_count: int = 0
    total_count: int = 0

    def win_rate(self):
        return int(self.win_count * 100 / self.total_count)


@dataclass
class WinRateMap:
    data: Dict[str, WinRate]
