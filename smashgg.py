import json
import requests

# functions for querying smash.gg API


def query(q, **kwargs):
    """
    Queries the Smash.gg API.
    Returns an object containing the data returned.
    """
    # the current entry URL to the API
    url = "https://api.smash.gg/gql/alpha"
    # the json containing the query and variables
    j = {"query": q, "variables": json.dumps(kwargs)}
    # the API token to use
    api_token = open("dev-key.txt", "r").read().strip()
    # the required headers to authorize the request
    headers = {"Authorization": f"Bearer {api_token}"}

    r = requests.post(url=url, json=j, headers=headers)
    return json.loads(r.text)


def query_standings(event_id):
    """
    Returns the standings of the event with the given ID.
    """
    res = query("""
        query EventStandings($eventId: ID!, $page: Int!, $perPage: Int!) {
            event(id: $eventId) {
                id
                name
                standings(query: {
                    perPage: $perPage,
                    page: $page
                }){
                    nodes {
                        placement
                        entrant {
                            id
                            name
                        }
                    }
                }
            }
        }
    """,
                eventId=event_id,
                page=1,
                perPage=10)

    return res
