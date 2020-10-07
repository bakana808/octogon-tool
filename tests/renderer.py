# %%
# import autoreload
# ?autoreload
import sys

sys.path.append("./src/")

from octogon.renderer.renderer import Renderer

renderer = Renderer()

event_id = 522705  # octo-gon 5

render = renderer.render_bracket(event_id)
# render = renderer.render_entrant(entrant_id, 2)

# %%

print(renderer.smashgg.query_bracket(event_id).res)

