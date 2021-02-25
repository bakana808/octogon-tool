import signal
from threading import Thread
from multiprocessing import Process
from multiprocessing.managers import BaseManager

import octogon.config
import octogon.scoreboard
from octogon.server import OctogonServer
from octogon.api.smashgg import SmashAPI
from octogon.daemon.scss import SCSSAutoCompiler
from octogon.gui.window import OctogonWidget
from octogon.renderer import Renderer
from octogon.server import start_server_process
from octogon.utils.logger import get_print_fn

print = get_print_fn()


class Flags:
    """
    A container of objects that need to be shared
    between multiple processes.
    """

    def __init__(self):
        self.scoreboard = None
        self.is_scoreboard_modified = True

    def set_scoreboard_modified(self, value):
        self.is_scoreboard_modified = value

    def get_scoreboard_modified(self):
        return self.is_scoreboard_modified

    def set_scoreboard(self, value):
        self.scoreboard = value

    def get_scoreboard(self):
        return self.scoreboard


class Octogon:
    """Main API class to provide access to all parts of Octogon."""

    def __init__(self):

        # allows program to exit with CTRL+C
        signal.signal(signal.SIGINT, self.close_window)

        # the user config
        self.config = octogon.config.load_config()

        # the scoreboard data object
        self.scoreboard = octogon.scoreboard.init_scoreboard(self)

        # the smash.gg object to use for API integration
        self.api_smashgg = SmashAPI(self)

        # the HTML renderer
        self.renderer = Renderer(self)

        # the QT window
        self.window = OctogonWidget(self)

        # start the SCSS watcher
        # watcher_thread = threading.Thread(target=observer.start)
        # watcher_thread.daemon = True
        # watcher_thread.start()
        self.scss_watcher = SCSSAutoCompiler(self)
        self.scss_watcher.start()

        # this manager is needed to share the flags object
        # with the server process
        BaseManager.register("Flags", Flags)
        self.process_manager = BaseManager()
        self.process_manager.start()

        self.flags = self.process_manager.Flags()
        self.flags.set_scoreboard(self.scoreboard.dictionary)

        # start the Flask server
        self.server = OctogonServer(self)
        self.server_process = self.create_server_process()
        self.server_process.start()

        # print config
        print("currently using these ids for data queries:")
        print(f"token: { self.config.SMASHGG_API_KEY }")
        print(f"tournament: { self.config.SMASHGG_TOURNY_SLUG }")
        print(f"event: { self.config.SMASHGG_EVENT_ID }")

    def start(self):
        """Start the GUI. Application will loop here."""
        self.window.start()
        self.on_close()

    def create_server_process(self) -> Process:
        thread = Process(target=self.server.start)
        thread.daemon = True
        return thread

    def close_window(self, *args):
        self.window.close()

    def on_scoreboard_update(self):
        """Called when the scoreboard file has changed."""
        self.flags.set_scoreboard(self.scoreboard.dictionary)
        self.flags.set_scoreboard_modified(True)
        print("scoreboard has been updated")

    def on_compile(self, name: str, ext: str, outdir: str):
        """Called when a file has been compiled (usually .scss)."""
        if name == "window":
            self.window.update_css()

    def on_close(self, *args):
        """Called when the program is exited (CTRL+C or through GUI)."""

        # stop the SCSS watcher
        self.scss_watcher.stop()
        # watcher_thread.join()
        print("scss compiler has stopped.")

        # stop the Flask server
        self.server_thread.terminate()
        self.server_thread.join()
        print("server has stopped.")
