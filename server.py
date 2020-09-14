import http.server
import socketserver
import smashgg
from jinja2 import FileSystemLoader, Environment

entrants = dict()

# tournament / event ids to use
smashgg_tournament_slug = "octo-gon-2"
smashgg_event_id = 517237

print("currently using these ids for data queries:")
print(f"tournament: { smashgg_tournament_slug }")
print(f"event: { smashgg_event_id }")


def get_placement_delta(entrant, placement):

    if entrant not in entrants:
        entrants[entrant] = placement

    last_placement = entrants[entrant]
    entrants[entrant] = placement

    return last_placement - placement


# read HTML template


class Templates:

    env = Environment(loader=FileSystemLoader("./"))
    ladder = env.get_template("templates/ladder.html")
    countdown = env.get_template("templates/countdown.html")
    bracket = env.get_template("templates/bracket.html")
    scoreboard = env.get_template("templates/scoreboard.html")


# HTML server


class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        print(f"requesting file: {self.path}")

        # ------------------------------------------------------------------------------
        #  Ladder Standings Overlay
        # -----------------------------------------------------------------------------

        if self.path == "/":
            # serve main HTML
            self.send_response(200)
            # self.send_header("Content-type", "text/html")
            self.end_headers()
            res = smashgg.query_standings(smashgg_event_id)
            body = ""

            placements = res["data"]["event"]["standings"]["nodes"]

            # test for handling changing placements
            # random.shuffle(placements)

            print(res)

            placement = 1
            for place in placements:
                entrant = place["entrant"]["name"]
                # placement = int(place["placement"])
                delta = get_placement_delta(entrant, placement)

                # add extra class for top4 placements
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

            self.wfile.write(bytes(Templates.ladder.render(body=body), "utf8"))

        # ------------------------------------------------------------------------------
        #  Countdown Overlay
        # -----------------------------------------------------------------------------

        elif self.path == "/countdown":

            self.send_response(200)
            self.end_headers()

            res = smashgg.query(
                """
                query TournamentQuery($slug: String) {
                    tournament(slug: $slug) {
                        startAt
                    }
                }
            """,
                slug=smashgg_tournament_slug,
            )

            timestamp = res["data"]["tournament"]["startAt"]

            print(f"tournament starts at {timestamp}")

            self.wfile.write(
                bytes(Templates.countdown.render(timestamp=timestamp), "utf8")
            )

        # ------------------------------------------------------------------------------
        #  Bracket Overlay
        # -----------------------------------------------------------------------------

        elif self.path == "/bracket":

            self.send_response(200)
            self.end_headers()

            res = smashgg.query(
                """
                query BracketQuery($id: ID!) {
                    event(id: $id) {
                        sets(page: 1, perPage: 10, sortType: CALL_ORDER) {
                            nodes {
                                winnerId
                                fullRoundText
                                setGamesType
                                totalGames
                                slots(includeByes: false) {
                                    entrant {
                                        id
                                        name
                                    }
                                }
                            }
                        }
                    }
                }
            """,
                id=smashgg_event_id,
            )

            body = ""
            for s in reversed(res["data"]["event"]["sets"]["nodes"]):
                body += f"""
                    <div class="match">
                        <div class="round-name">{ s["fullRoundText"] } · Best of { s["totalGames"] }</div>
                """
                winner_id = s["winnerId"]
                for i, entrant in enumerate(s["slots"]):
                    # append span representing a player
                    if entrant["entrant"]["id"] == winner_id:
                        body += f"""<span class="player winner">{ entrant["entrant"]["name"] }</span>"""
                    else:
                        body += f"""<span class="player">{ entrant["entrant"]["name"] }</span>"""

                    # append "vs" text
                    if i < len(s["slots"]) - 1:
                        body += """<span class="vs">vs.</span>"""

                body += "</div>"

                print(s)

            self.wfile.write(
                bytes(Templates.bracket.render(body=body), "utf8")
            )

        elif self.path == "/scoreboard":

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(Templates.scoreboard.render(), "utf8"))

        else:  # attempt to serve the requested path as a file
            try:
                f = open(self.path[1:], "r")

                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()

                self.wfile.write(bytes(f.read(), "utf8"))
            except FileNotFoundError:
                self.send_error(404, f"File Not Found: {self.path}")


# window = pyglet.window.Window(width=800, height=600)

# @window.event
# def on_draw():
#     window.clear(

# pyglet.app.run()


def start_server(server):
    print(f"starting server on port { server.server_address[1] }...")
    server.allow_reuse_address = True
    server.serve_forever()


def create_server(port=8000) -> socketserver.TCPServer:
    """
    Start the server that serves overlays.
    """
    # prevents a "port already binded" error when restarting program
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("", port), HTTPHandler)
    return server


# open("output.html", "w").write(html)
