from jinja2 import FileSystemLoader, Environment
from api.smashgg import SmashAPI
from pyhtml import div, span

_env = Environment(loader=FileSystemLoader("./templates/"))


class HTMLTemplate:
    """
    An HTML template used to serve a browser source.
    """

    def __init__(self, path: str):

        # the Jinja template
        self.template = _env.get_template(path)

    def render(self, **kwargs) -> bytes:
        """
        Render this template as bytes.
        Makes it simpler to write to a HTTP request handler.
        """

        output = self.template.render(**kwargs)
        print(output)
        return output
        # return bytes(self.template.render(**kwargs), "utf8")


class Renderer:
    """
    The class used to render requested information or overlays as HTML.
    """

    def __init__(self):

        print("loading HTML templates...")

        self.t_ladder = HTMLTemplate("ladder.html")
        self.t_countdown = HTMLTemplate("countdown.html")
        self.t_bracket = HTMLTemplate("bracket.html")
        self.t_scoreboard = HTMLTemplate("scoreboard.html")

        self.smashgg = SmashAPI()

        print("done!")

    def render_countdown(self, tournament_slug: str) -> bytes:

        res = self.smashgg.query("countdown", slug=tournament_slug)

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
        body = ""

        placements = res["data"]["event"]["standings"]["nodes"]

        # test for handling changing placements
        # random.shuffle(placements)

        print(res)

        placement = 1
        for place in placements:
            entrant = place["entrant"]["name"]
            # placement = int(place["placement"])

            # calculate the change in placement
            # delta = get_placement_delta(entrant, placement)
            delta = 0

            # add extra css class for top4 placements
            placement_classes = "placement"
            if placement <= 4:
                placement_classes += " top4"

            css_class = ""
            if delta > 0:
                css_class = "up"
            elif delta < 0:
                css_class = "down"
            body += f"""
                <div class="place">
                    <div class="placement-wrapper"><span class="{placement_classes}">{placement}</span></div>
                    <!--span class="delta {css_class}">{delta}</span-->
                    <span class="name">{entrant}</span>
                </div>
            """
            placement += 1

        return self.t_ladder.render(body=body)

    def render_bracket(self, event_id) -> str:

        bracket = self.smashgg.query_bracket(event_id)

        bracket_div = div(class_="standings")  # TODO: rename to bracket
        bracket_children = []
        sets = bracket.get_unfinished_sets()
        # sets = bracket.get_sets()

        if sets is None or len(sets) == 0:  # no matches were found
            bracket_div = div(class_="message")(
                "Waiting for the upcoming matches..."
            )

        else:  # go through the matches
            # for s in reversed(res["data"]["event"]["sets"]["nodes"]):

            last_round_name = None
            round_div = None
            round_children = []

            for s in sets:
                round_name = s["fullRoundText"]
                round_games = s["totalGames"]

                # skip grand final reset set
                if round_name == "Grand Final Reset":
                    continue

                # create a new round div
                if round_name != last_round_name:
                    last_round_name = round_name
                    if round_div:
                        bracket_children.append(round_div(*round_children))
                    round_div = div(class_="round")
                    round_children = [
                        span(class_="round-name")(
                            f"{round_name} · Best of {round_games}"
                        )
                    ]

                set_div = div(class_="set")
                set_children = []

                winner_id = s["winnerId"]

                # add the letter identifier for this set
                set_children.append(span(class_="set-id")(s["identifier"]))

                for i, entrant in enumerate(s["slots"]):

                    if entrant["entrant"]:
                        name = entrant["entrant"]["name"]
                        id = entrant["entrant"]["id"]
                        score = entrant["standing"]["stats"]["score"]["value"]
                    else:  # placeholder entrant
                        name = "?"
                        id = None
                        score = 0

                    # append span representing a player
                    if winner_id and id == winner_id:
                        set_children.append(
                            span(class_="player winner")(
                                span(class_="player-name")(name),
                                span(class_="player-score")(score),
                            )
                        )
                    else:
                        set_children.append(
                            span(class_="player")(
                                span(class_="player-name")(name),
                                span(class_="player-score")(score),
                            )
                        )

                    # append "vs" text
                    if i < len(s["slots"]) - 1:
                        set_children.append(span(class_="vs")(".vs"))

                round_children.append(set_div(*set_children))

        # add the last round div
        bracket_children.append(round_div)
        bracket_div = bracket_div(*bracket_children)

        print(bracket_div.render())

        return self.t_bracket.render(body=bracket_div.render())

    def render_scoreboard(self) -> bytes:

        return self.t_scoreboard.render()
