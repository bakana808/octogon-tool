import os
import pathlib
import typing

from flask import send_from_directory, request
from flask_cors import cross_origin

from octogon.api.spotify import spotify_get_artist, spotify_get_song
from octogon.utils.tag import div, span
from octogon.utils.logger import get_print_fn

if typing.TYPE_CHECKING:
    from octogon import Octogon
    from octogon.server import OctogonServer

print = get_print_fn("flask")


def add_routes(server: "OctogonServer"):
    """Adds all routes to this Flask application."""

    app = server.app
    octogon: "Octogon" = server.octogon
    renderer = octogon.renderer
    config = octogon.config

    @app.route("/<path:path>", methods=["GET"])
    def _get_file(path):
        """Called when a file is requested."""
        # _, ext = os.path.splitext(path)
        # if ext == ".json":
        # return send_from_directory("../", path, mimetype="text/json")
        # print(f"cwd: {os.getcwd()}, path: {path}")

        # print("GET {}".format(path))
        # print("folder = %s" % pathlib.Path(path).parts[0])

        if (
            pathlib.Path(path).parts[0] == "assets"
            or pathlib.Path(path).parts[0] == "scripts"
            or path == "scoreboard.json"
        ):
            # looking in "assets" or "scripts"; located in the cwd
            directory = os.getcwd()
        else:
            # access other files; located in "sites"
            directory = os.path.join(os.getcwd(), "site")

        # send the requested file from the directory
        return send_from_directory(directory, path, cache_timeout=0)

    @app.route("/")
    @cross_origin
    def _index():
        return ""

    @app.route("/debug", methods=["POST"])
    def _debug():
        """
        Debug route for external scripts to communicate with this program.
        """
        data = request.get_json()

        # print messages from the data
        if "message" in data:
            print(data["message"])

        return {"success": True}

    # Scoreboard Routes
    # -----------------

    @app.route("/scoreboard")
    def _scoreboard():
        return renderer.render_scoreboard()

    @app.route("/scoreboard/data")
    def _scoreboard_data():
        flags = octogon.flags
        # print("is_modified: %s" % octogon.get_scoreboard_modified())
        if flags.get_scoreboard_modified():
            print("modification detected")
            flags.set_scoreboard_modified(False)
            return {"is_modified": True, "scoreboard": flags.get_scoreboard()}
        else:
            return {"is_modified": False, "scoreboard": flags.get_scoreboard()}

    @app.route("/background")
    def _background():
        return renderer.render_background()

    # Smash.gg Integration Routes
    # ---------------------------

    @app.route("/countdown")
    def _smashgg_countdown():
        return renderer.render_countdown(config.SMASHGG_TOURNY_SLUG)

    @app.route("/standings")
    def _smashgg_standings():
        return renderer.render_standings(config.SMASHGG_EVENT_ID)

    @app.route("/bracket")
    def _smashgg_bracket():
        return renderer.render_bracket(config.SMASHGG_EVENT_ID)

    @app.route("/test-player")
    def _test_player():
        return renderer.render_test_player()

    current = 0

    @app.route("/rotation")
    def _rotation():
        """Rotates between the standings and bracket overlays automatically."""
        nonlocal current
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
