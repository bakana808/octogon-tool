import http.server
import socketserver
import smashgg
import random
from urllib.parse import urlparse
from jinja2 import FileSystemLoader, Environment, select_autoescape

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

        else:
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
