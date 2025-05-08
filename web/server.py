from flask import Flask, render_template, request

from app.app import App


DEFAULT_GAME_COUNTS = 20
server = Flask(__name__)
app = App()
app.set_count(DEFAULT_GAME_COUNTS)

users = [
    "98man#EUW",
    "London78Man#5566",
    "LondonRoy#EUW",
    "happyhellowin#EUW",
    "yoyomimimao#EUW",
    "ThankU9527#9527",
]


@server.route("/")
def index():
    # Get the selected user from the URL parameters, default to the first user
    selected_user = request.args.get('user', users[0])

    # Get the matches for the selected user
    game_name, tag_line = selected_user.split("#")
    app.set_game_name(game_name, tag_line)

    win_rate_map = app.get_win_rates_by_champions()

    matches = [win_rate.to_html_dict() for win_rate in win_rate_map.values()]

    champion_images = {
        win_rate.title: champion_to_url(win_rate.title)
        for win_rate in win_rate_map.values()
    }
    return render_template(
        "champions.html",
        users=users,
        selected_user=selected_user,
        matches=matches,
        champion_images=champion_images,
    )


def champion_to_url(champion):
    return f"https://opgg-static.akamaized.net/meta/images/lol/15.4.1/champion/{champion}.png"


if __name__ == "__main__":
    server.run(
        port=3000,
        debug=True,
    )
