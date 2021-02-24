from octogon.data import JsonData
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from octogon.api.smashgg import SmashAPI


class SmashggResponse(JsonData):
    """
    A response from Smash.gg's API
    """

    def __init__(self, data, key: str, api):
        try:
            super().__init__(data["data"][key])

            self.res = data  # full response object
            self.api: "SmashAPI" = api

        except Exception:

            if "success" in data and data["success"] is False:
                raise RuntimeError("Smash.gg query unsuccessful: " + data["message"])

            if not type(data) is dict:
                raise RuntimeError("unable to parse response data: \n" + str(data))

            if "data" not in data:
                raise RuntimeError("No data returned from this query.\n" + str(data))

            if data["data"][key] is None:
                raise RuntimeError("data is empty")

    def print_data(self):
        print(self._json)
