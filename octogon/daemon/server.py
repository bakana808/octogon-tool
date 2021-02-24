import logging
import os
import pathlib

from flask import Flask, request, send_from_directory

import octogon.config
from octogon.api.spotify import spotify_get_artist, spotify_get_song
from octogon.renderer.renderer import Renderer
from octogon.web.tag import div, span

print = octogon.config.get_print_fn("flask")

# disable info logging for flask
logging.getLogger("werkzeug").setLevel(logging.WARNING)

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
renderer = None


def start_server():
    config = octogon.config.config

    print("currently using these ids for data queries:")
    print(f"tournament: { config.SMASHGG_TOURNY_SLUG }")
    print(f"event: { config.SMASHGG_EVENT_ID }")

    global renderer
    renderer = Renderer()
    app.run(debug=True, use_reloader=False, port=8000)


def stop_server():
    """
    Stop the Flask server.
    Provided by:
    https://stackoverflow.com/a/17053522/2886326
    """

    try:
        fn = request.environ.get("werkzeug.server.shutdown")
        fn()

    except Exception:
        pass


@app.route("/<path:path>", methods=["GET"])
def _get_file(path):
    """Called when a file is requested."""
    # _, ext = os.path.splitext(path)
    # if ext == ".json":
    # return send_from_directory("../", path, mimetype="text/json")
    # print(f"cwd: {os.getcwd()}, path: {path}")

    # print("GET {}".format(path))
    # print("folder = %s" % pathlib.Path(path).parts[0])

    if pathlib.Path(path).parts[0] == "assets":
        # looking in "assets"; located in the cwd
        directory = os.getcwd()
    else:
        # looking in "scripts" or "style"; located in "sites"
        directory = os.path.join(os.getcwd(), "site")

    # send the requested file from the directory
    return send_from_directory(directory, path, cache_timeout=0)


# Scoreboard Routes
# -----------------


@app.route("/scoreboard")
def _scoreboard():
    return renderer.render_scoreboard()


@app.route("/background")
def _background():
    return renderer.render_background()


# Smash.gg Integration Routes
# ---------------------------


@app.route("/countdown")
def _smashgg_countdown():
    return renderer.render_countdown(octogon.config.config.SMASHGG_TOURNY_SLUG)


@app.route("/standings")
def _smashgg_standings():
    return renderer.render_standings(octogon.config.config.SMASHGG_EVENT_ID)


@app.route("/bracket")
def _smashgg_bracket():
    return renderer.render_bracket(octogon.config.config.SMASHGG_EVENT_ID)


@app.route("/test-player")
def _test_player():
    return renderer.render_test_player()


current = 0


@app.route("/rotation")
def _rotation():
    """Rotates between the standings and bracket overlays automatically."""
    global current
    config = octogon.config.config
    auto_refresh = 20
    if current == 0:
        current += 1
        return renderer.render_bracket(
            config.SMASHGG_EVENT_ID, auto_refresh=auto_refresh
        )
    elif current == 1:
        current = 0
        return renderer.render_standings(
            config.SMASHGG_EVENT_ID, auto_refresh=auto_refresh
        )


# Spotify Integration Routes
# --------------------------


@app.route("/spotify")
def _spotify():
    name, artist = spotify_get_song(), spotify_get_artist()
    body = div("#spotify")(
        span(".sp_icon")("🎵"), span(".sp_title")(f"{artist} - {name}")
    )
    return renderer.render("default", body=body, auto_refresh=5)
