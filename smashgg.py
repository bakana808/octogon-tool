import json
import os
import requests

# functions for querying smash.gg API


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

