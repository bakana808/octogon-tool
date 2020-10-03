from octogon.api.smashgg.response import SmashggResponse


class EventData(SmashggResponse):
    def __init__(self, data, api):
        super().__init__(data, "event", api)

        self.id = self["id"]

        self.entrant_ids = [i["id"] for i in self["entrants.nodes"]]

    def get_sets(self):
        """
        Return a list of all sets in this bracket.
        """
        sets = self["sets.nodes"]
        if sets is None:
            sets = []

        return sets

    def get_unfinished_sets(self):
        """
        Return a list of sets without a winner.
        """

        sets = self.get_sets()

        # only return sets without a winner
        return [s for s in sets if not s["winnerId"]]
