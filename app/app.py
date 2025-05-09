import logging
from collections import OrderedDict

from app.helpers import update_participant_win_rate, update_champion_win_rate
from .color_output import cyan, bold, highlight
from .models.entity_type import EntityType
from .models.win_rate import WinRate
from .riot_api_client import RiotAPIClient


logger = logging.getLogger(__name__)


class App:

    def __init__(self, client=RiotAPIClient()):
        self.tag_line = None
        self.game_name = None
        self.count = None
        self.client = client

    def set_game_name(self, game_name, tag_line):
        self.game_name = game_name
        self.tag_line = tag_line

    def set_count(self, count):
        self.count = count

    def _get_match_details(self) -> []:
        riot_account = self.client.get_account_by_riot_id(self.game_name, self.tag_line)
        match_ids = self.client.get_match_ids_by_puuid(riot_account.puuid, count=self.count)
        return [self.client.get_match_detail(match_id) for match_id in match_ids]

    def _get_win_rates_by(self, func) -> dict[str, WinRate]:
        win_rate_map: dict[str, WinRate] = {}

        riot_account = self.client.get_account_by_riot_id(self.game_name, self.tag_line)
        match_ids = self.client.get_match_ids_by_puuid(riot_account.puuid, count=self.count)
        logger.info(f"{len(match_ids)} matches are fetched")

        # scan every match
        for match_id in match_ids:
            match_detail = self.client.get_match_detail(match_id)
            match_timeline = self.client.get_match_timeline(match_id)
            func(match_detail, match_timeline, riot_account.puuid, win_rate_map)

        # Sort and keep as OrderedDict (optional)
        sorted_data = OrderedDict(
            sorted(win_rate_map.items(), key=lambda item: item[1].total_count, reverse=True)
        )

        # If you want to wrap it again in WinRateMap:
        return dict(sorted_data)

    def get_win_rates_by_participants(self) -> dict[str, WinRate]:
        return self._get_win_rates_by(update_participant_win_rate)

    def get_win_rates_by_champions(self):
        return self._get_win_rates_by(update_champion_win_rate)

    def print_win_rates(self, entity_type: EntityType, win_rate_map: dict[str, WinRate], top=5):

        game_name = f"{self.game_name}#{self.tag_line}"
        output = "\n"
        if entity_type == EntityType.SUMMONERS:
            output += f"Summoners {bold(cyan(game_name))} played with in the last {self.count} matches:\n\n"
            output += f"{'Summoner Name':<20} | {'W - L':^12} | {'Win Rate':^8}\n"
            output += "-" * 45 + "\n"

        elif entity_type == EntityType.CHAMPIONS:
            output += f"Champions {bold(cyan(game_name))} played in the last {self.count} matches:\n\n"
            output += f"{'Champion Name':<16} | {'W - L':^10} | {'Win Rate':^5} | {'KDA':^6} | {'KP':^6}\n"
            output += "-" * 59 + "\n"

        for win_rate in win_rate_map.values():
            if top <= 0:
                break

            if win_rate.title == f"{self.game_name}#{self.tag_line}":
                name = "(Overall)"
                top += 1
            else:
                name = win_rate.title
            w_l = f"{win_rate.win_count}W - {win_rate.lose_count}L"

            ### highlights
            # win rate
            rate = highlight(win_rate.win_rate(), 60, 40)
            kda = highlight(win_rate.kda.avg_kda(), 5, 2)
            kp = highlight(win_rate.kda.avg_kill_participation(), 60, 40)
            win_rate_row = f"{name:<16} | {w_l:^10} | {rate:^17} | {kda:^15} | {kp:^15}\n"

            # if win_rate.win_rate() >= 60:
            #     win_rate_row = green(win_rate_row)
            # elif win_rate.win_rate() <= 40:
            #     win_rate_row = red(win_rate_row)

            output += win_rate_row
            top -= 1

        print(output)

    def get_game_dates_by_champion_role(self, champion_name, role):
        return [
            p.game_name + "#" + p.tag
            for match_detail in self._get_match_details()
            for p in match_detail.info.participants
            if p.champion_name == champion_name and p.lane == role
        ]

    def get_info_by_champion(self, champion_name):
        return [
            f"{match_detail.info.dt} {p.win}"
            for match_detail in self._get_match_details()
            for p in match_detail.info.participants
            if p.champion_name == champion_name and p.game_name == self.game_name
        ]


game_names = [
    "98man#EUW",
    "London78Man#5566",
    "LondonRoy#EUW",
    "happyhellowin#EUW",
    "yoyomimimao#EUW",
    "ThankU9527#9527",
    # "油舌夫#7725",
    # "78人#2888",
]
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = App()
    app.set_count(20)
    for name in game_names:
        game_name, tag_line = name.split("#")
        app.set_game_name(game_name, tag_line)

        # win_rate_map = app.get_win_rates_by_participants()
        # app.print_win_rates(entity_type=EntityType.SUMMONERS, win_rate_map=win_rate_map, top=5)

        win_rate_map = app.get_win_rates_by_champions()
        app.print_win_rates(entity_type=EntityType.CHAMPIONS, win_rate_map=win_rate_map, top=10)
