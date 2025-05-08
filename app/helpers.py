from typing import List

from .models.match_detail import MatchDetail, Participant
from .models.win_rate import WinRate


def get_game_names_from_participants(participants: List[Participant], owner_puuid: str) -> List[str]:
    return [p.game_name for p in participants if p.puuid != owner_puuid]


def _update_win_rate(title: str, win: bool, win_rate_map: dict[str, WinRate]):
    # win rate
    if title not in win_rate_map:
        win_rate_map[title] = WinRate(title=title)
    if win:
        win_rate_map[title].win_count += 1
    else:
        win_rate_map[title].lose_count += 1
    win_rate_map[title].total_count += 1


def _update_kda(title: str, participant: Participant, win_rate_map: dict[str, WinRate]):
    kda = win_rate_map[title].kda
    kda.kills += participant.kills
    kda.deaths += participant.deaths
    kda.assists += participant.assists
    kda.kill_participation += participant.challenges.kill_participation
    kda.game_count += 1


def update_participant_win_rate(match: MatchDetail, owner_puuid: str, win_rate_map: dict[str, WinRate]):
    team_id = match.get_team_id_by_puuid(owner_puuid)
    for participant in match.get_team_participants_by_team_id(team_id):
        name = f"{participant.game_name}#{participant.tag}"
        win = match.get_win_by_puuid(owner_puuid)
        _update_win_rate(title=name, win=win, win_rate_map=win_rate_map)


def update_champion_win_rate(match: MatchDetail, owner_puuid: str, win_rate_map: dict[str, WinRate]):
    participant = match.get_participant_by_puuid(owner_puuid)
    _update_win_rate(title=participant.champion_name, win=participant.win, win_rate_map=win_rate_map)
    _update_kda(title=participant.champion_name, participant=participant, win_rate_map=win_rate_map)
