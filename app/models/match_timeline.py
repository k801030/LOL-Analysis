from dataclasses import dataclass
from typing import List

from app.models.match_detail import Metadata


@dataclass
class ParticipantFrame:
    total_gold: int

    @classmethod
    def from_dict(cls, data: dict) -> "ParticipantFrame":
        return cls(
            total_gold=data.get("totalGold")
        )


@dataclass
class Frame:
    participant_frames: dict[str, ParticipantFrame]

    @classmethod
    def from_dict(cls, data: dict) -> "Frame":
        return cls(
            participant_frames={pid: ParticipantFrame.from_dict(participant_frame) for pid, participant_frame in
                                data.get("participantFrames", {}).items()}
        )


@dataclass
class TimelineParticipant:
    participant_id: int
    puuid: str

    @classmethod
    def from_dict(cls, data: dict) -> "TimelineParticipant":
        return cls(
            participant_id=data.get("participantId"),
            puuid=data.get("puuid")
        )


@dataclass
class Info:
    frames: List[Frame]
    participants: List[TimelineParticipant]

    @classmethod
    def from_dict(cls, data: dict) -> "Info":
        return cls(
            frames=[Frame.from_dict(p) for p in data.get("frames", [])],
            participants=[TimelineParticipant.from_dict(p) for p in data.get("participants", [])],
        )


@dataclass
class MatchTimeline:
    metadata: Metadata
    info: Info

    @classmethod
    def from_dict(cls, data: dict) -> "MatchTimeline":
        return cls(
            metadata=Metadata.from_dict(data["metadata"]),
            info=Info.from_dict(data["info"]),
        )
