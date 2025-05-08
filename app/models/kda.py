from dataclasses import dataclass
from typing import Dict


@dataclass
class Kda:
    game_count: int = 0
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    kill_participation: float = 0.0

    def avg_kills(self):
        return int(self.kills / self.game_count)

    def avg_deaths(self):
        return int(self.deaths / self.game_count)

    def avg_assists(self):
        return int(self.assists / self.game_count)

    def avg_kda(self):
        return round((self.kills + self.assists) / max(self.deaths, 1), 1)

    def avg_kill_participation(self):
        return int(self.kill_participation * 100 / self.game_count)
