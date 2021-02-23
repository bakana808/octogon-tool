import json
import os
import requests
from octogon.util import defaultdict
import octogon.config
from octogon.api.smashgg.tournament import TournamentData
from octogon.api.smashgg.response import SmashggResponse
from octogon.api.smashgg.player import PlayerData
from octogon.api.smashgg.event import EventData
from octogon.config import get_print_fn

print = get_print_fn("smash.gg")


class SmashAPI:

    PATH: str = "queries/"

    def __init__(self):

        config = octogon.config.config

        self.queries = {}

        files = [
            os.path.join(SmashAPI.PATH, f)
            for f in os.listdir(SmashAPI.PATH)
            if os.path.isfile(os.path.join(SmashAPI.PATH, f))
        ]

        print("loading queries...")
        for filepath in files:
            with open(filepath, "r") as f:
                name = os.path.splitext(os.path.basename(filepath))[0]
                self.queries[name] = f.read()
                print(f'loaded query "{ name }"')

        print("loading API key...")

        self.api_key = config.SMASHGG_API_KEY

        # cache mappings

        self.player_cache = defaultdict()
        self.tournament_cache = defaultdict()
        self.event_cache = defaultdict()

    def query(self, name, **kwargs):
        """
        Queries the Smash.gg API.
        Returns an object containing the data returned.
        """
        # get our query from our saved queries
        q = self.queries[name]

        print(f'querying "{name}"...')

        return self.query_raw(q, **kwargs)

    def query_raw(self, q, **kwargs):
        # the current entry URL to the API
        url = "https://api.smash.gg/gql/alpha"

        # the json containing the query and variables
        j = {"query": q, "variables": json.dumps(kwargs)}

        # the required headers to authorize the request
        headers = {"Authorization": f"Bearer {self.api_key}"}

        r = requests.post(url=url, json=j, headers=headers)
        return json.loads(r.text)

    def query_standings(self, event_id, page=1, per_page=10) -> SmashggResponse:

        res = self.query("standings", eventId=event_id, page=page, perPage=per_page)
        return SmashggResponse(res, "event", self)

    def get_player(self, player_id) -> PlayerData:
        """Get tournament data from its slug."""

        # use the cached PlayerData or call the API
        def query():
            return PlayerData(self.query("player", id=player_id), self)

        return self.player_cache.get_or_default(player_id, query)

    def get_entrant_to_player_map(self, event_id) -> dict:

        event_data = SmashggResponse(
            self.query("entrants", event_id=event_id),
            "event",
            self,
        )

        entrant_map = {}

        for entrant_data in event_data["entrants.nodes"]:

            entrant_id = entrant_data["id"]
            participants = entrant_data["participants"]
            if participants:
                entrant_map[entrant_id] = participants[0]["player.id"]
                continue

        return entrant_map

    def get_player_from_entrant(self, event_id, entrant_id) -> PlayerData:

        entrant_map = self.get_entrant_to_player_map(event_id)
        return self.get_player(entrant_map[entrant_id])

    def get_tournament(self, slug: str) -> TournamentData:
        """Get tournament data from its slug."""

        def query():
            return TournamentData(self.query("tournament", slug=slug), self)

        return self.tournament_cache.get_or_default(slug, query)

    def get_first_event(self, slug: str) -> EventData:
        """
        Get the first event of a tournament by its slug.
        This is an easy way to get event data if the tournament
        has only one event.

        If there are more than one event, call get_events() instead.
        """
        tournament = self.get_tournament(slug)
        return self.get_event(tournament.event_ids[0])

    def get_event(self, event_id) -> EventData:
        """
        Query the upcoming matches in the bracket.

        Note: if the tournament has not started or if there is no
        active bracket, the "data.event.sets.nodes" key will be None.
        """

        def query():
            return EventData(self.query("bracket", id=event_id), self)

        return query()
        # return self.event_cache.get_or_default(event_id, query)
