from flask import Flask, render_template, request

from app.app import App
from app.helpers import aggregate_win_rate


server = Flask(__name__)
app = App()

users = [
    "98man#EUW",
    "London78Man#5566",
    "LondonRoy#EUW",
    "happyhellowin#EUW",
    "yoyomimimao#EUW",
    "ThankU9527#9527",
]

game_counts = [
    10,
    20,
    50,
    100,
]


@server.route("/")
def index():
    # Get the selected user from the URL parameters, default to the first user
    selected_user = request.args.get('user', users[0])
    game_name, tag_line = selected_user.split("#")
    app.set_game_name(game_name, tag_line)

    # Get the selected game count from the URL parameters, default to the second game count
    selected_game_count = request.args.get('game_count', game_counts[1])
    app.set_count(selected_game_count)

    win_rate_map = app.get_win_rates_by_champions()
    overview_win_rate = aggregate_win_rate(win_rate_map).to_html_dict()
    matches = [win_rate.to_html_dict() for win_rate in win_rate_map.values()]

    champion_images = {
        win_rate.title: champion_to_url(win_rate.title)
        for win_rate in win_rate_map.values()
    }
    return render_template(
        "champions.html",
        users=users,
        selected_user=selected_user,
        game_counts=game_counts,
        selected_game_count=selected_game_count,
        matches=matches,
        overview_win_rate=overview_win_rate,
        champion_images=champion_images,
    )


def champion_to_url(champion):
    return f"https://opgg-static.akamaized.net/meta/images/lol/15.4.1/champion/{champion}.png"


if __name__ == "__main__":
    server.run(
        port=3000,
        debug=True,
    )
