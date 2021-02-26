import logging
from typing import TYPE_CHECKING
from multiprocessing import Process

from flask import Flask
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
        self.app.run(debug=False, use_reloader=False, port=8000)

    # to stop this server, run it in a Process and call terminate()
    # there is no way to stop it if it is running in a thread


class OctogonServerProcess:
    def __init__(self, octogon: "Octogon"):

        self.octogon = octogon
        self.server = OctogonServer(octogon)

        self.process = Process(target=self.server.start)
        self.process.daemon = True

    def start(self):
        self.process.start()

    def stop(self):
        self.process.terminate()
        self.process.join()
        self.process.close()
