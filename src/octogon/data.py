import json


# OUTPUT_FILE = "output/sb_data.json"
OUTPUT_FILE = "output/sb_data_new.json"


class JsonData:
    """A JSON object returned by a web API."""

    def __init__(self, json: dict, is_writable=False):

        self._json = json

        # if False, deny editing this json object
        self.is_writable = is_writable

    def __getitem__(self, k: str):
        """
        Get a value from the json object.

        The key is formatted as a period-separated list of keys.
        For example:

            data["a.b.c"]

        is equivalent to:

            data["a"]["b"]["c"]

        If the value is an instance of dict, then another instance of
        JsonData is returned.
        """

        keys = k.split(".")
        value = self._json
        for key in keys:
            value = value[key]

        return self._convert_value(value)

    def _convert_value(self, value):
        if isinstance(value, dict):
            return JsonData(value, self.is_writable)
        elif isinstance(value, list):
            return [self._convert_value(i) for i in value]
        else:
            return value

    def __setitem__(self, k, v):
        """Set a value in the json object"""

        if not self.is_writable:
            raise RuntimeError("cannot modify this data, it is non-writable")

        keys = k.split(".")
        ret = self._json
        for i, key in enumerate(keys):
            if i == len(keys) - 1:  # last elm
                ret[key] = v
            else:
                ret = ret[key]


class ScoreboardData(JsonData):
    def __init__(self):
        json = ScoreboardData.load()
        super().__init__(json, True)

    @staticmethod
    def load() -> dict:
        """Load the scoreboard JSON."""
        print("loading scoreboard JSON...")
        return json.load(open(OUTPUT_FILE))

    def save(self):
        print("saving scoreboard JSON...")
        print(self._json)
        with open(OUTPUT_FILE, "w") as f:
            json.dump(self._json, f, ensure_ascii=False, indent=4)


scoreboard = ScoreboardData()
