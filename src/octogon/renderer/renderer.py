import os
import random
from jinja2 import FileSystemLoader, Environment

from octogon.config import get_print_fn, TEMPLATE_PATH
from octogon.api.smashgg import SmashAPI
from octogon.api.smashgg.player import PlayerData
from octogon.lookup import get_portrait_url
from octogon.web.tag import div, span

_env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
print = get_print_fn("web")


class HTMLTemplate:
    """
    An HTML template used to serve a browser source.
    """

    def __init__(self, path: str):

        # the Jinja template
        self.template = _env.get_template(path)

    def render(self, **kwargs) -> str:
        """
        Render this template as bytes.
        Makes it simpler to write to a HTTP request handler.
        """

        output = self.template.render(**kwargs)
        # print(output)
        return output
        # return bytes(self.template.render(**kwargs), "utf8")


class Renderer:
    """
    The class used to render requested information or overlays as HTML.
    """

    def __init__(self):

        print("loading HTML templates...")

        self.templates = {}

        files = [
            f
            for f in os.listdir(TEMPLATE_PATH)
            if os.path.isfile(os.path.join(TEMPLATE_PATH, f))
        ]

        for filepath in files:
            name = os.path.splitext(os.path.basename(filepath))[0]
            template = HTMLTemplate(filepath)
            self.templates[name] = template
            print(f"loaded template '{ name }' ({filepath})")

        self.t_ladder = HTMLTemplate("ladder.html")
        self.t_countdown = HTMLTemplate("countdown.html")
        self.t_bracket = HTMLTemplate("bracket.html")
        self.t_scoreboard = HTMLTemplate("scoreboard.html")
        self.t_mask = HTMLTemplate("mask.svg")
        self.t_background = HTMLTemplate("background.html")

        self.smashgg = SmashAPI()

        print("done!")

    def render(self, template_name: str, **kwargs) -> str:
        """
        Render a template by its name.
        """

        return self.templates[template_name].render(**kwargs)

    def render_countdown(self, tournament_slug: str) -> bytes:

        res = self.smashgg.query("tournament", slug=tournament_slug)

        timestamp = res["data"]["tournament"]["startAt"]

        print(f"tournament starts at {timestamp}")

        return self.t_countdown.render(timestamp=timestamp)

    def render_standings(self, event_id) -> bytes:

        # XXX: below code used to calculate diff in placement
        # from the last time this function was called

        # entrants = dict()
        # def get_placement_delta(entrant, placement):

        #     if entrant not in entrants:
        #         entrants[entrant] = placement

        #     last_placement = entrants[entrant]
        #     entrants[entrant] = placement

        #     return last_placement - placement

        res = self.smashgg.query(
            "standings", eventId=event_id, page=1, perPage=10
        )

        placements = res["data"]["event"]["standings"]["nodes"]
        if not placements:
            placements = []

        # test for handling changing placements
        # random.shuffle(placements)

        print(res)

        elm = div(".standings")

        placement = 1
        for place in placements:
            entrant = place["entrant"]["name"]
            # placement = int(place["placement"])

            # calculate the change in placement
            # delta = get_placement_delta(entrant, placement)
            delta = 0

            # add extra css class for top4 placements
            placement_classes = ".placement"
            if placement <= 4:
                placement_classes += ".top4"

            css_class = ""
            if delta > 0:
                css_class = "up"
            elif delta < 0:
                css_class = "down"

            elm.add_child(
                div(".place")(
                    div(".placement-wrapper")(
                        span(placement_classes)(placement)
                    ),
                    # div(class_=f"delta {css_class}")(delta)
                    span(".name")(entrant),
                )
            )

            placement += 1

        print(elm)

        return self.t_ladder.render(body=str(elm))

    def render_player(
        self,
        side: int,
        player: PlayerData,
        score: int = 0,
        is_winner: bool = False,
    ) -> tuple:

        print(f"rendering {player.name}")

        character_url = get_portrait_url(player.get_last_character())

        if is_winner:
            classes = f"#player{side}.player.winner"
        else:
            classes = f"#player{side}.player"

        player_div = span(classes)(
            span(".player-name")(player.name),
            span(".player-score")(score),
        )

        return player_div, character_url

    def render_test_player(self):
        tournament_id = "octo-gon-3"
        event = self.smashgg.get_first_event(tournament_id)

        entrant_id = random.choice(event.entrant_ids)
        player = self.smashgg.get_player_from_entrant(event.id, entrant_id)

        entrant_tup = self.render_player(0, player)

        return self.render(
            "player", body=entrant_tup[0], p0_bg=entrant_tup[1], p1_bg=""
        )

    def render_bracket(self, event_id) -> str:

        bracket = self.smashgg.get_event(event_id)

        elm = div(".standings")  # TODO: rename to bracket
        # sets = bracket.get_unfinished_sets()
        sets = bracket.get_sets()

        if sets is None or len(sets) == 0:  # no matches were found
            elm.add_child(
                div(".message")("Waiting for the upcoming matches...")
            )
            print("rendering entrant")

        else:  # go through the matches
            # for s in reversed(res["data"]["event"]["sets"]["nodes"]):

            last_round_name = None
            round_div = None

            for s in sets:
                round_name = s["fullRoundText"]
                round_games = s["totalGames"]

                # skip grand final reset set
                if round_name == "Grand Final Reset":
                    continue

                print(round_name)

                # create a new round div
                if round_name != last_round_name:
                    last_round_name = round_name
                    if round_div:
                        elm.add_child(round_div)

                    round_div = div(".round")
                    round_div.add_child(
                        # round_children.append(
                        span(".round-name")(
                            f"{round_name} · Best of {round_games}"
                        )
                    )

                set_div = div(".set")
                # set_children = []

                winner_id = s["winnerId"]

                # add the letter identifier for this set
                set_letter = s["identifier"]
                if set_letter:
                    set_div.add_child(span(".set-id")(set_letter))

                for i, entrant in enumerate(s["slots"]):

                    if entrant["entrant"]:
                        name = entrant["entrant"]["name"]
                        id = entrant["entrant"]["id"]
                        score = (
                            entrant["standing"]["stats"]["score"]["value"] or 0
                        )
                    else:  # placeholder entrant
                        name = "?"
                        id = None
                        score = 0

                    is_winner = id == winner_id

                    # append "vs" text
                    if i < len(s["slots"]) - 1:
                        set_div.add_child(span(".vs")(".vs"))
                        # set_children.append(span(class_="vs")(".vs"))

                # round_children.append(div(class_="set")(set_children))
                round_div.add_child(set_div)
                # print(set_div)

            # add the last round div
            # elm.add_child(div(".round")(round_children))
            elm.add_child(round_div)

        # print(elm)
        # print("test")

        return self.t_bracket.render(body=str(elm))

    def render_scoreboard(self) -> bytes:

        return self.t_scoreboard.render()

    def render_background(self) -> str:

        bg_path = "assets/bgs/1.png"

        mask_src = self.render_mask()

        with open("output/mask.svg", "w") as f:
            f.write(mask_src)

        return self.t_background.render(bg_path=bg_path)

    def render_mask(self) -> str:
        """
        Renders a 73:60 ratio mask for use in the background source.
        """

        # TODO: be able to configure mask size
        # TODO: be able to configure aspect ratio
        # TODO: be able to offset position

        mask_size = 0.956  # the size of the view area (percentage)

        res = 1920, 1080  # the resolution of the canvas area

        # origin pos and size of the center view area
        height = int(1080 * mask_size)
        width = int(1080 * 73 / 60 * mask_size)
        x = int((res[0] - width) / 2)
        y = int(0)

        # instead of making one rectangle to mask out view area from
        # the background, we have to make four for the area
        # around the view area...
        # this is because the browser source in OBS doesn't support
        # mask-mode: luminance

        # left letterbox pos/size
        inv_x = 0
        inv_y = 0
        inv_w = (res[0] - width) // 2
        inv_h = res[0]

        # right letterbox pos (same size as left letterbox)
        inv_x2 = inv_x + inv_w + width
        inv_y2 = inv_y

        # top letterbox pos/size
        inv_x3 = inv_x + inv_w
        inv_y3 = 0
        inv_w3 = width
        inv_h3 = (res[1] - height) // 2

        # bottom letterbox
        inv_x4 = inv_x3
        inv_y4 = inv_h3 + height

        # render the mask SVG
        return self.t_mask.render(
            mask_h=inv_h,
            mask_w=inv_w,
            mask_x=inv_x,
            mask_y=inv_y,
            mask_x2=inv_x2,
            mask_y2=inv_y2,
            mask_x3=inv_x3,
            mask_y3=inv_y3,
            mask_h3=inv_h3,
            mask_w3=inv_w3,
            mask_x4=inv_x4,
            mask_y4=inv_y4,
        )
