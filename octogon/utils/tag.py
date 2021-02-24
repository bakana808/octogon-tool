import re
from bs4 import BeautifulSoup as bs


def create_tag(tag: str):
    class Tag:

        TAG = tag

        def __init__(self, selectors: str = ""):

            ids = re.findall(r"\#([\w-]+)", selectors)
            classes = re.findall(r"\.([\w-]+)", selectors)
            # print(f"ids: {ids}")
            # print(f"classes: {classes}")

            if len(ids):
                self.id = ids[0]
            else:
                self.id = None

            self.classes = classes
            self.children = []

        def add_child(self, *children):

            self.children.extend(children)

        def __call__(self, *children):

            self.add_child(*children)
            return self

        def render_meta(self) -> str:

            meta = ""

            if self.id:
                meta += f' id="{self.id}"'

            if len(self.classes) > 0:
                meta += f" class=\"{' '.join(self.classes)}\""

            return meta

        @staticmethod
        def _fast_render(tag) -> str:
            """Render an arbitrary object without prettifying it."""

            try:
                meta = tag.render_meta()
                child_renders = [
                    Tag._fast_render(child) for child in tag.children
                ]

                elms = [f"<{tag.TAG}{meta}>", *child_renders, f"</{tag.TAG}>"]

                src = "".join(elms)
                return src
            except Exception:
                return str(tag)

        def __str__(self):

            # prettify the render
            soup = bs(Tag._fast_render(self), "html.parser")
            return soup.prettify()

    return Tag


div = create_tag("div")
span = create_tag("span")
