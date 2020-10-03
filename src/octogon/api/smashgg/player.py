from collections import Counter
from octogon.api.smashgg.response import SmashggResponse
from octogon.lookup import characters
from typing import Optional, Dict


class PlayerData(SmashggResponse):
    """A Smashgg Player."""

    def __init__(self, data, api):
        super().__init__(data, "player", api)

        self.id = self["id"]
        self.prefix = self["prefix"]
        self.name = self["gamerTag"]

        # mapping of event ids to entrant id
        self._entrant_cache: Dict[int, Optional[str]] = {}

    def get_entrant_id(self, event_id) -> Optional[str]:
        """
        Get the entrant ID of this player at the given event.

        If this player did not enter that event, None is returned.
        """
        if event_id in self._entrant_cache:
            return self._entrant_cache[event_id]
        else:
            data = SmashggResponse(
                self.api.query("entrants", event_id=event_id),
                "event",
                self.api,
            )

            # print(data._json)

            # nested function to return out of
            def _entrant_loop():
                for entrant_data in data["entrants.nodes"]:
                    for participant_data in entrant_data["participants"]:
                        if participant_data["player.id"] == self.id:
                            return entrant_data["id"]
                return None

            entrant_id = _entrant_loop()
            self._entrant_cache[event_id] = entrant_id
            return entrant_id

    def get_last_character(self) -> Optional[str]:
        """
        Get the last character this player has selected
        in their most recent set.

        If no character selections can be found, None
        is returned.
        """

        for set_ in self["sets.nodes"]:
            if not set_["games"]:
                continue

            entrant_id = self.get_entrant_id(set_["event.id"])

            # reverse games so that the last one
            # is processed first
            for game in reversed(set_["games"]):
                if not game["selections"]:
                    continue

                for selection in game["selections"]:
                    if selection["entrant.id"] == entrant_id:
                        return characters[int(selection["selectionValue"])]

        return None

    def get_character_distribution(self) -> dict:
        """
        Get the character distribution of this player by their
        most recent sets.

        Returns a map of character slugs to percentages.
        """

        selected_chars = []
        for set_ in self["sets.nodes"]:

            # get this player's entrant ID for this event
            entrant_id = self.get_entrant_id(set_["event.id"])

            if not set_["games"]:  # could be None if set is DQ'd
                continue

            for game in set_["games"]:

                if not game["selections"]:
                    continue

                for selection in game["selections"]:
                    if selection["entrant.id"] == entrant_id:
                        # append the selected character ID
                        selected_chars.append(int(selection["selectionValue"]))

        # map of IDs to occurances
        character_counts = Counter(selected_chars)

        # map of slugs to percentages
        character_dist = {}

        for char_id, count in character_counts.items():
            slug = characters.get(char_id, "?")
            character_dist[slug] = count / len(selected_chars)

        return character_dist
