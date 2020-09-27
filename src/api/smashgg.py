import json
import os
import requests

# functions for querying smash.gg API


class SmashggResponse:
    def __init__(self, res):
        self.res = res


class SmashggBracket(SmashggResponse):
    def get_sets(self):
        """
        Return a list of all sets in this bracket.
        """
        sets = self.res["data"]["event"]["sets"]["nodes"]
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


class SmashAPI:

    PATH: str = "queries/"

    def __init__(self):

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

        with open("dev-key.txt", "r") as f:
            self.api_key = f.read().strip()

    def query(self, name, **kwargs):
        """
        Queries the Smash.gg API.
        Returns an object containing the data returned.
        """
        # get our query from our saved queries
        q = self.queries[name]

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

    def query_standings(self, event_id, page=1, per_page=10):

        res = self.query(
            "standings", eventId=event_id, page=page, perPage=per_page
        )
        return res

    def query_bracket(self, event_id) -> SmashggBracket:
        """
        Query the upcoming matches in the bracket.

        Note: if the tournament has not started or if there is no
        active bracket, the "data.event.sets.nodes" key will be None.
        """
        res = self.query("bracket", id=event_id)
        return SmashggBracket(res)

