import signal

import octogon.config
import octogon.scoreboard
from octogon.api.smashgg import SmashAPI
from octogon.daemon.scss import SCSSAutoCompiler
from octogon.gui.window import OctogonWidget
from octogon.renderer import Renderer
from octogon.server import start_server_process
from octogon.utils.logger import get_print_fn

print = get_print_fn()


class Octogon:
    """Main API class to provide access to all parts of Octogon."""

    def __init__(self):

        # allows program to exit with CTRL+C
        signal.signal(signal.SIGINT, self.close_window)

        # the user config
        self.config = octogon.config.load_config()

        # the scoreboard data object
        self.scoreboard = octogon.scoreboard.init_scoreboard(self)
        self.is_scoreboard_modified = True

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

        # start the Flask server
        # thread = threading.Thread(target=start_server, args=(server,))
        self.server_process = start_server_process(self)

        # print config
        print("currently using these ids for data queries:")
        print(f"token: { self.config.SMASHGG_API_KEY }")
        print(f"tournament: { self.config.SMASHGG_TOURNY_SLUG }")
        print(f"event: { self.config.SMASHGG_EVENT_ID }")

    def start(self):
        """Start the GUI. Application will loop here."""
        self.window.start()
        self.on_close()

    def close_window(self, *args):
        self.window.close()

    def on_scoreboard_update(self):
        """Called when the scoreboard file has changed."""
        self.is_scoreboard_modified = True
        print("scoreboard has been updated")

    def on_compile(self, name: str, ext: str, outdir: str):
        """Called when a file has been compiled (usually .scss)."""
        if name == "window":
            self.window.update_css()

    def on_close(self, *args):
        """Called when the program is exited (CTRL+C or through GUI)."""

        # ensure the window is closed
        self.window.close()

        # stop the Flask server
        self.server_process.terminate()
        self.server_process.join()
        print("server has stopped.")

        # stop the SCSS watcher
        self.scss_watcher.stop()
        # watcher_thread.join()
        print("scss compiler has stopped.")
