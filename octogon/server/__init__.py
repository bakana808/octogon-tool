import logging
from multiprocessing import Process

from flask import Flask, request

from octogon.utils.logger import get_print_fn
import octogon.server.router as router

print = get_print_fn("flask")


class OctogonServer:
    def __init__(self, octogon):

        self.app = Flask("Octogon")
        self.app.config["CACHE_TYPE"] = "null"
        self.app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

        # disable info logging for flask
        logging.getLogger("werkzeug").setLevel(logging.WARNING)

        self.octogon = octogon

        router.add_routes(self)

    def start(self):

        self.app.run(debug=True, use_reloader=False, port=8000)

    def stop(self):
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


def start_server_process(octogon) -> Process:
    """Start the Flask server in a new Process."""

    def _start_server():
        server = OctogonServer(octogon)
        server.start()

    process = Process(target=_start_server, args=())
    process.daemon = True
    process.start()
    return process
