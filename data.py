import json


class ScoreboardData:
    def __init__(self):
        self.load()

    def __getitem__(self, k):
        keys = k.split(".")
        ret = self.json
        for key in keys:
            ret = ret[key]
        return ret

    def __setitem__(self, k, v):
        keys = k.split(".")
        ret = self.json
        for i, key in enumerate(keys):
            if i == len(keys) - 1:  # last elm
                ret[key] = v
            else:
                ret = ret[key]

    def load(self):
        """Load the scoreboard JSON."""
        self.json = json.load(open("output/sb_data.json"))
        print("loading scoreboard JSON...")
        print(self.json)

    def save(self):
        print("saving scoreboard JSON...")
        print(self.json)
        with open("output/sb_data.json", "w") as f:
            json.dump(self.json, f, ensure_ascii=False, indent=4)


scoreboard = ScoreboardData()

