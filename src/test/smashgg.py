import sys

sys.path.append("./src/")

from octogon.api.smashgg import SmashAPI

api = SmashAPI()

# %% player tests

player_id = 8024  # firefly

player = api.get_player(player_id)

print(player.name)
print(player.get_character_distribution())
print(player.get_last_character())

# %% event tests

tournament_slug = "octo-gon-3"

tourny = api.get_tournament(tournament_slug)

print(tourny.name)
print(tourny.url)
print(tourny.event_ids)

