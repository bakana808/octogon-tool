"""
Octogon Panel Constants
"""
import json


CONFIG_PATH = "config.json"


class Config:
    def __init__(self, data: dict):
        self.data = data

        # location of .scss files
        self.STYLE_PATH = data["style_path"]
        # location of jinja2 templates
        self.TEMPLATE_PATH = data["template_path"]
        # location of scoreboard data
        self.SB_DATA_PATH = data["sb_path"]

        self.SMASHGG_API_KEY = data["smashgg_api_key"]
        self.SMASHGG_TOURNY_SLUG = data["smashgg_tourny_slug"]
        self.SMASHGG_EVENT_ID = data["smashgg_event_id"]


def load_config() -> Config:
    """Load constants from the config file."""

    print("loading config...")
    try:
        conf = json.load(open(CONFIG_PATH))
    except FileNotFoundError:
        # write a default config
        conf = {
            "style_path": "templates/scss/",
            "template_path": "templates/html",
            "sb_path": "scoreboard.json",
            "smashgg_api_key": "",
            "smashgg_tourny_slug": "",
            "smashgg_event_id": "",
        }
        with open(CONFIG_PATH, "w") as f:
            json.dump(conf, f, ensure_ascii=False, indent=4)
            print("created default config")

    # conf["sb_path"] = "site/scoreboard.json"

    print("config loaded!")

    return Config(conf)
