from pyhtml import div as py_div
from pyhtml import span as py_span


def create_elm_class(handle_class):
    class element:
        def __init__(self, *, class_=""):

            self.handle = handle_class(class_=class_)
            self.children = []

        def add_child(self, *children):
            self.children += children
            self.handle = self.handle(*self.children)

        def render(self) -> str:
            return self.handle.render()

        def __str__(self) -> str:
            return self.render()

        def __call__(self, *args):
            self.children = list(args)
            return self.handle(*args)

    return element


div = create_elm_class(py_div)
span = create_elm_class(py_span)

