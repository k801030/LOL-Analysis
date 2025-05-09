from flask import Flask, render_template, request, make_response

from app.app import App
from app.helpers import aggregate_win_rate, aggregate_win_rate_by_role


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
    user_cookie = request.cookies.get("user", users[0])
    selected_user = request.args.get('user', user_cookie)
    game_name, tag_line = selected_user.split("#")
    app.set_game_name(game_name, tag_line)

    # Get the selected game count from the URL parameters, default to the second game count
    game_count_cookie = request.cookies.get("game_count", game_counts[1])
    selected_game_count = request.args.get('game_count', game_count_cookie)
    app.set_count(int(selected_game_count))

    win_rate_map = app.get_win_rates_by_champions()
    overview_win_rate = aggregate_win_rate(win_rate_map).to_html_dict()
    role_win_rate = [win_rate.to_html_dict() for win_rate in aggregate_win_rate_by_role(win_rate_map).values()]
    matches = [win_rate.to_html_dict() for win_rate in win_rate_map.values()]


    champion_images = {
        # champion name is win_rate.title.split("#")[0]
        win_rate.title.split("#")[0]: champion_to_url(win_rate.title.split("#")[0])
        for win_rate in win_rate_map.values()
    }

    resp = make_response(
        render_template(
            "champions.html",
            users=users,
            selected_user=selected_user,
            game_counts=game_counts,
            selected_game_count=selected_game_count,
            matches=matches,
            overview_win_rate=overview_win_rate,
            role_win_rate=role_win_rate,
            champion_images=champion_images,

        )
    )
    resp.set_cookie("user", selected_user)
    resp.set_cookie("game_count", str(selected_game_count))
    return resp


def champion_to_url(champion):
    return f"https://opgg-static.akamaized.net/meta/images/lol/15.4.1/champion/{champion}.png"


if __name__ == "__main__":
    server.run(port=3000, debug=True)
