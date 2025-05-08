from datetime import datetime
from dataclasses import dataclass, field
from typing import List

from app.typo_corrector import TypoCorrector


@dataclass
class Metadata:
    participants: List[str]

    @classmethod
    def from_dict(cls, data: dict) -> "Metadata":
        return cls(
            participants=data.get("participants", [])
        )


@dataclass
class Challenges:
    kill_participation: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> "Challenges":
        return cls(
            kill_participation=data.get("killParticipation", 0.0),
        )


@dataclass
class Participant:
    puuid: str
    team_id: int
    win: bool
    game_name: str
    tag: str
    champion_name: str
    kills: int
    deaths: int
    assists: int
    lane: str
    challenges: Challenges = field(default_factory=Challenges)

    @classmethod
    def from_dict(cls, data: dict) -> "Participant":
        champion_name = TypoCorrector.correct(data["championName"])
        return cls(
            puuid=data["puuid"],
            team_id=data["teamId"],
            win=data["win"],
            game_name=data.get("riotIdGameName"),
            tag=data["riotIdTagline"],
            champion_name=champion_name,
            kills=data["kills"],
            deaths=data["deaths"],
            assists=data["assists"],
            lane=data["lane"],
            challenges=Challenges.from_dict(data.get("challenges", {}))
        )


@dataclass
class Info:
    participants: List[Participant]
    game_mode: str
    game_creation: int
    dt: datetime

    @classmethod
    def from_dict(cls, data: dict) -> "Info":
        return cls(
            participants=[Participant.from_dict(p) for p in data.get("participants", [])],
            game_mode=data.get("gameMode"),
            game_creation=data.get("gameCreation"),
            dt=datetime.fromtimestamp(data.get("gameCreation") / 1000),
        )


@dataclass
class MatchDetail:
    metadata: Metadata
    info: Info

    @classmethod
    def from_dict(cls, data: dict) -> "MatchDetail":
        return cls(
            metadata=Metadata.from_dict(data["metadata"]),
            info=Info.from_dict(data["info"])
        )

    def get_team_id_by_puuid(self, target_puuid: str) -> int:
        for participant in self.info.participants:
            if participant.puuid == target_puuid:
                return participant.team_id
        raise ValueError(f"PUUID {target_puuid} not found in match participants.")

    def get_win_by_puuid(self, target_puuid: str) -> bool:
        for participant in self.info.participants:
            if participant.puuid == target_puuid:
                return participant.win
        raise ValueError(f"PUUID {target_puuid} not found in match participants.")

    def get_team_participants_by_team_id(self, target_team_id: int) -> List[Participant]:
        participants = []
        for participant in self.info.participants:
            if participant.team_id == target_team_id:
                participants.append(participant)
        return participants

    def get_participant_by_puuid(self, target_puuid: str) -> Participant:
        for participant in self.info.participants:
            if participant.puuid == target_puuid:
                return participant
        raise ValueError(f"PUUID {target_puuid} not found in match participants.")
