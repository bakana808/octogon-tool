import http.server
import socketserver
import smashgg
from jinja2 import FileSystemLoader, Environment

entrants = dict()


def get_placement_delta(entrant, placement):

    if entrant not in entrants:
        entrants[entrant] = placement

    last_placement = entrants[entrant]
    entrants[entrant] = placement

    return last_placement - placement


# read HTML template

env = Environment(loader=FileSystemLoader("./"))
template = env.get_template('template.html')
temp_countdown = env.get_template('countdown.html')

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
            res = smashgg.query_standings(517237)
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
                css_class = ""
                if delta > 0:
                    css_class = "up"
                elif delta < 0:
                    css_class = "down"
                body += f"""
                    <div class="place">
                        <div class="placement-wrapper"><span class="placement">{placement}</span></div>
                        <!--span class="delta {css_class}">{delta}</span-->
                        <span class="name">{entrant}</span>
                    </div>
                """
                placement += 1

            self.wfile.write(bytes(template.render(body=body), "utf8"))

        # ------------------------------------------------------------------------------
        #  Countdown Overlay
        # -----------------------------------------------------------------------------

        elif self.path == "/countdown":

            self.send_response(200)
            self.end_headers()

            res = smashgg.query("""
                query TournamentQuery($slug: String) {
                    tournament(slug: $slug) {
                        startAt
                    }
                }
            """,
                                slug="octo-gon-2")

            timestamp = res["data"]["tournament"]["startAt"]

            print(f"tournament starts at {timestamp}")

            self.wfile.write(
                bytes(temp_countdown.render(timestamp=timestamp), "utf8"))

        # ------------------------------------------------------------------------------
        #  Bracket Overlay
        # -----------------------------------------------------------------------------

        elif self.path == "/bracket":

            self.send_response(200)
            self.end_headers()

            res = smashgg.query("""
                query BracketQuery($id: ID!) {
                    event(id: $id) {
                        sets(page: 1, perPage: 10, sortType: CALL_ORDER) {
                            nodes {
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
                                id=517237)

            body = ""
            for s in res["data"]["event"]["sets"]["nodes"]:
                body += f"""
                    <div class="match">
                        <div class="round-name">{ s["fullRoundText"] } · Best of { s["totalGames"] }</div>
                        <span class="player">{ s["slots"][0]["entrant"]["name"] }</span>
                        <span class="vs">vs.</span>
                        <span class="player">{ s["slots"][1]["entrant"]["name"] }</span>
                    </div>
                """
                print(s)

            self.wfile.write(bytes(template.render(body=body), "utf8"))

        else:  # attempt to serve the requested path as a file
            try:
                f = open(self.path[1:], "r")

                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()

                self.wfile.write(bytes(f.read(), "utf8"))
            except FileNotFoundError:
                self.send_error(404, f"File Not Found: {self.path}")


port = 8000
socketserver.TCPServer.allow_reuse_address = True
server = socketserver.TCPServer(("", port), HTTPHandler)
server.serve_forever()

# open("output.html", "w").write(html)
