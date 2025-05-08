from dataclasses import dataclass, field
from typing import Dict

from .kda import Kda


@dataclass
class WinRate:
    title: str
    kda: Kda = field(default_factory=Kda)
    win_count: int = 0
    lose_count: int = 0
    total_count: int = 0

    def win_rate(self):
        return int(self.win_count * 100 / self.total_count)

    def to_html_dict(self):
        return {
            "name": self.title,
            "w": self.win_count,
            "l": self.lose_count,
            "games": self.total_count,
            "win_rate": self.win_rate(),
            "kda": self.kda.avg_kda(),
            "kp": self.kda.avg_kill_participation(),
        }


@dataclass
class WinRateMap:
    data: Dict[str, WinRate]
