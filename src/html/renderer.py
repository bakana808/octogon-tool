from jinja2 import FileSystemLoader, Environment

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

        return bytes(self.template.render(**kwargs), "utf8")
