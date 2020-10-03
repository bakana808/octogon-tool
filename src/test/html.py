# %%

# import autoreload
# ?autoreload
from web.tag import div, span

# elm = div()("test")
elm = div(".class")(div(".nest")("test"), "test", "test2")
# elm = div("#test.test2.test3")("content")
print(elm)

# %%

elm = span(".class")("content")
print(elm)
