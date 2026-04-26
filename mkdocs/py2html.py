from typing import Optional

def make_tag(name: str, non_closing=False):
    def tag(content: Optional[str]=None, **kwargs) -> str:
        otag = f"<{name}"
        for k, v in kwargs.items():
            otag += f' {k}="{v}"'
        return f"{otag}>" + (content if content else "") + (f"</{name}>" if (not non_closing) else "")
    return tag


def multiple_tag(name: str):
    def tag(*args):
        compl = f"<{name}>"
        for i in args:
            compl += i
        return compl + f"</{name}>"

    return tag


def multiple(*tags):
    compl = ""
    for i in tags:
        compl += i
    return compl


def spacing(num: int):
    return "&nbsp;"*num


HTMLIFY_TRANSTABLE = str.maketrans(
    {"<":"&lt;", ">":"&gt;", " ":"&nbsp;"}
)


def htmlify(text: str) -> str:
    return text.translate(HTMLIFY_TRANSTABLE)


def pwrap(text: str):
    compl: str = "<p>"
    isnew: bool = True
    for i in text:
        if i == "\n":
            if isnew:
                compl = compl.removesuffix("<p>")
                compl += "<br>"
            else:
                compl += "</p>"
                isnew = True
            compl += "<p>"
        else:
            isnew = False
            compl += i

    if isnew:
        compl = compl.removesuffix("<p>")
    else:
        compl += "</p>"

    return compl


meta = make_tag("meta", True)
hr = make_tag("hr", True)
br = make_tag("br", True)
head = multiple_tag("head")
center = make_tag("center")
title = make_tag("title")
html = multiple_tag("html")
body = multiple_tag("body")
h1 = make_tag("h1")
h2 = make_tag("h2")
h3 = make_tag("h3")
h4 = make_tag("h4")
h5 = make_tag("h5")
h6 = make_tag("h6")
a = make_tag("a")
p = make_tag("p")
b = make_tag("b")
em = make_tag("em")
u = make_tag("u")
code = make_tag("code")
xmp = make_tag("xmp")