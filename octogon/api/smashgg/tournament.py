from octogon.api.smashgg.response import SmashggResponse


class TournamentData(SmashggResponse):
    """A tournament."""

    def __init__(self, data, api):
        super().__init__(data, "tournament", api)

        self.name = self["name"]
        self.url = "smash.gg/" + self["slug"]

        # the starting time of the tournament in UNIX
        self.start_time = int(self["startAt"])

        # the IDs of all events in this tournament
        self.event_ids = [i["id"] for i in self["events"]]
