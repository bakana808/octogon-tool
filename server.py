import http.server
import socketserver
import os
from urllib.parse import unquote
from src.html.renderer import Renderer

# tournament / event ids to use

smashgg_tournament_slug = "octo-gon-4"
smashgg_event_id = 521088  # octo-gon 4 singles
# smashgg_event_id = 519066  # octo-gon 3 singles
# smashgg_event_id = 517237  # octo-gon 2 singles

print("currently using these ids for data queries:")
print(f"tournament: { smashgg_tournament_slug }")
print(f"event: { smashgg_event_id }")

renderer = Renderer()


class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        self.path = unquote(self.path)
        print(f"requesting path: {self.path}")

        # ------------------------------------------------------------------------------
        #  Ladder Standings Overlay
        # -----------------------------------------------------------------------------

        if self.path == "/":
            # serve main HTML
            self.send_response(200)
            # self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(renderer.render_standings(smashgg_event_id))

        # ------------------------------------------------------------------------------
        #  Countdown Overlay
        # -----------------------------------------------------------------------------

        elif self.path == "/countdown":

            self.send_response(200)
            self.end_headers()

            self.wfile.write(
                renderer.render_countdown(smashgg_tournament_slug)
            )

        # ------------------------------------------------------------------------------
        #  Bracket Overlay
        # -----------------------------------------------------------------------------

        elif self.path == "/bracket":

            self.send_response(200)
            self.end_headers()

            self.wfile.write(renderer.render_bracket(smashgg_event_id))

        elif self.path == "/scoreboard":

            self.send_response(200)
            self.end_headers()

            self.wfile.write(renderer.render_scoreboard())

        else:  # attempt to serve the requested path as a file

            ext = os.path.splitext(self.path)[1]

            mimetypes = {".png": "image/png", ".css": "text/css"}

            need_bytes = {".png": True}

            mimetype = mimetypes.get(ext, "text/html")
            as_bytes = need_bytes.get(ext, False)

            try:

                if as_bytes:
                    f = open(self.path[1:], "rb")
                else:
                    f = open(self.path[1:], "rb")

                self.send_response(200)
                self.send_header("Content-type", mimetype)
                self.end_headers()

                self.wfile.write(f.read())
                f.close()

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
