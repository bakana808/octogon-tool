import json

from octogon.utils.data import NestedDict
from octogon.utils.logger import get_print_fn

print = get_print_fn("scoreboard")


class ScoreboardData(NestedDict):
    """
    A reference to the JSON file containing
    scoreboard data.
    """

    DEFAULT = {
        "round_title": "Round 1",
        "round_games": "3",
        "p1": {
            "tag": "",
            "name": "Player 1",
            "color": 0,
            "wins": 0,
            "character": "Captain Falcon",
            "skin": 0,
            "port": 0,
        },
        "p2": {
            "tag": "",
            "name": "Player 2",
            "color": 0,
            "wins": 0,
            "character": "Fox",
            "skin": 0,
            "port": 1,
        },
    }

    def __init__(self, octogon):
        self.octogon = octogon
        super().__init__(self.load(), True)

    def load(self) -> dict:
        """Load the scoreboard JSON."""
        print("loading scoreboard JSON...")
        config = self.octogon.config

        # try to read the scoreboard file or create a new one
        try:
            data = json.load(open(config.SB_DATA_PATH))
        except FileNotFoundError:
            print("loading default SB data")
            data = ScoreboardData.DEFAULT
            # write the default scoreboard data
            with open(config.SB_DATA_PATH, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        print("loaded scoreboard data!")

        return data

    def save(self):
        config = self.octogon.config

        with open(config.SB_DATA_PATH, "w") as f:
            json.dump(self.dictionary, f, ensure_ascii=False, indent=4)
            print("committed scoreboard changes")

    def on_data_changed(self, k, v):
        print("scoreboard has been updated")


def init_scoreboard(octogon):
    return ScoreboardData(octogon)
