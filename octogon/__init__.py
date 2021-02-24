from octogon.main import start_gui_loop
import signal
import octogon.data
from octogon.renderer.renderer import Renderer
from octogon.api.smashgg import SmashAPI
import octogon.config
from octogon.daemon.scss import SCSSAutoCompiler
from octogon.daemon.server import start_server_process

print = octogon.config.get_print_fn()


class Octogon:
    """Main API class to provide access to all parts of Octogon."""

    def __init__(self):

        # allows program to exit with CTRL+C
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # the user config
        self.config = octogon.config.load_config()

        # the scoreboard data object
        self.scoreboard = octogon.data.init_scoreboard(self)

        # the smash.gg object to use for API integration
        self.api_smashgg = SmashAPI(self)

        # the HTML renderer
        self.renderer = Renderer(self)

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
        start_gui_loop(self)

    def on_close(self):
        """Called when the program is exited (CTRL+C or through GUI)."""

        # stop the Flask server
        self.server_process.terminate()
        self.server_process.join()
        print("server has stopped.")

        # stop the SCSS watcher
        self.scss_watcher.stop()
        # watcher_thread.join()
        print("scss compiler has stopped.")
