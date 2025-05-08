from dataclasses import dataclass


@dataclass
class RiotAccount:
    puuid: str
    game_name: str
    tag_line: str

    @classmethod
    def from_dict(cls, data: dict) -> "RiotAccount":
        return cls(
            puuid=data["puuid"],
            game_name=data["gameName"],
            tag_line=data["tagLine"],
        )