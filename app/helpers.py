from typing import List

from .models.match_detail import MatchDetail, Participant
from .models.match_timeline import MatchTimeline
from .models.win_rate import WinRate
from .timeline_helper import get_early_gold_diff


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


def _update_others(title: str, early_gold_diff: int, win_rate_map: dict[str, WinRate]):
    win_rate_map[title].early_gold_diff += early_gold_diff


def update_participant_win_rate(match: MatchDetail, owner_puuid: str, win_rate_map: dict[str, WinRate]):
    team_id = match.get_team_id_by_puuid(owner_puuid)
    for participant in match.get_team_participants_by_team_id(team_id):
        name = f"{participant.game_name}#{participant.tag}"
        win = match.get_win_by_puuid(owner_puuid)
        _update_win_rate(title=name, win=win, win_rate_map=win_rate_map)


def update_champion_win_rate(match: MatchDetail, match_timeline: MatchTimeline, owner_puuid: str,
                             win_rate_map: dict[str, WinRate]):
    participant = match.get_participant_by_puuid(owner_puuid)
    early_gold_diff = get_early_gold_diff(match, match_timeline, owner_puuid)

    title = f"{participant.champion_name}#{participant.individual_position}"
    _update_win_rate(title=title, win=participant.win, win_rate_map=win_rate_map)
    _update_kda(title=title, participant=participant, win_rate_map=win_rate_map)
    _update_others(title=title, early_gold_diff=early_gold_diff, win_rate_map=win_rate_map)


def aggregate_win_rate(win_rate_map: dict[str, WinRate]) -> WinRate:
    overview = WinRate(title="Overview Stats")
    overview.kda.game_count = sum(win_rate.kda.game_count for win_rate in win_rate_map.values())
    overview.kda.kills = sum(win_rate.kda.kills for win_rate in win_rate_map.values())
    overview.kda.deaths = sum(win_rate.kda.deaths for win_rate in win_rate_map.values())
    overview.kda.assists = sum(win_rate.kda.assists for win_rate in win_rate_map.values())
    overview.kda.kill_participation = sum(win_rate.kda.kill_participation for win_rate in win_rate_map.values())

    overview.win_count = sum(win_rate.win_count for win_rate in win_rate_map.values())
    overview.lose_count = sum(win_rate.lose_count for win_rate in win_rate_map.values())
    overview.total_count = sum(win_rate.total_count for win_rate in win_rate_map.values())

    overview.early_gold_diff = sum(win_rate.early_gold_diff for win_rate in win_rate_map.values())
    return overview
