from typing import List

from app.models.match_detail import Participant, MatchDetail
from app.models.match_timeline import TimelineParticipant, MatchTimeline


def get_participant(match_detail: MatchDetail, puuid) -> Participant:
    for p in match_detail.info.participants:
        if p.puuid == puuid:
            return p


def get_enemy_laner(match_detail: MatchDetail, me: Participant) -> Participant:
    for p in match_detail.info.participants:
        if p.individual_position == me.individual_position and p.puuid != me.puuid:
            return p


def get_early_gold_diff(match_detail: MatchDetail, match_timeline: MatchTimeline, puuid) -> int:
    frame_index = 13  # 14 minutes
    if frame_index >= len(match_timeline.info.frames):
        return 0
    me = get_participant(match_detail, puuid)
    opponent = get_enemy_laner(match_detail, me)
    if opponent is not None:
        my_gold = _get_gold_by_participant(match_timeline, frame_index, me)
        opponent_gold = _get_gold_by_participant(match_timeline, frame_index, opponent)
        return my_gold - opponent_gold
    return 0


def _get_gold_by_participant(match_timeline: MatchTimeline, frame_index: int, p: Participant) -> int:
    pid = _get_participant_id(match_timeline.info.participants, p)
    participant_frames = match_timeline.info.frames[frame_index].participant_frames
    return participant_frames.get(pid).total_gold


def _get_participant_id(participants: List[TimelineParticipant], target: Participant) -> str:
    return str(next(p.participant_id for p in participants if p.puuid == target.puuid))
