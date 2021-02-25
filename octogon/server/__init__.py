import logging
import sys
from threading import Thread
from typing import TYPE_CHECKING

from flask import Flask, request
from flask_cors import CORS

from octogon.utils.logger import get_print_fn
import octogon.server.router as router

if TYPE_CHECKING:
    from octogon import Octogon

print = get_print_fn("flask")


class OctogonServer:
    def __init__(self, octogon: "Octogon"):

        self.octogon = octogon

        self.app = Flask("Octogon")
        self.cors = CORS(self.app)
        self.app.config["CACHE_TYPE"] = "null"
        self.app.config["CORS_HEADERS"] = "Content-Type"
        self.app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

        # disable info logging for flask
        logging.getLogger("werkzeug").setLevel(logging.WARNING)

        router.add_routes(self)

    def start(self):
        try:
            self.app.run(debug=False, use_reloader=False, port=8000)
        except RuntimeError:
            sys.exit(0)

    def stop(self):
        raise RuntimeError("Server shutting down")


def start_server_process(octogon: "Octogon") -> Thread:
    """Start the Flask server in a new Process."""

    def _start_server():
        server = OctogonServer(octogon)
        server.start()

    thread = Thread(target=_start_server, args=())
    thread.daemon = True
    thread.start()
    return thread
