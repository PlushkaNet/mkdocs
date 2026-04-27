from typing import Callable, Union

def make_tag(name: str, non_closing=False) -> Callable[[tuple[str], dict[str, Union[str, int, float]]], str]:
    def tag(*args, **kwargs) -> str:
        compl: str = f"<{name}"
        for k, v in kwargs.items():
            compl += f' {k}="{v}"'
        return compl + ">" + "".join(args) + (f"</{name}>" if (not non_closing) else "")
    return tag


# deprecated; use standart make_tag instead
def multiple_tag(name: str):
    def tag(*args) -> str:
        return f"<{name}>" + "".join(args) + f"</{name}>"

    return tag


# deprecated; use make_tag instead
def multiple(*tags) -> str:
    return "".join(tags)


def spacing(num: int):
    return "&nbsp;"*num


HTMLIFY_TRANSTABLE = str.maketrans(
    {"<":"&lt;", ">":"&gt;", " ":"&nbsp;"}
)


def htmlify(text: str) -> str:
    return text.translate(HTMLIFY_TRANSTABLE)


class insert:
    def __init__(self, *args):
        self._content = "".join(args)

    def If(self, eval_bool) -> str:
        if eval_bool:
            return self._content
        return ""

    def Repeat(self, times: int) -> str:
        single: str = self._content
        for i in range(times):
            self._content += single
        return self._content

    def Htmlify(self) -> str: return htmlify(self._content)
    
    def __str__(self) -> str: return self._content

    def html(self) -> str: return self.__str__()


def pwrap(text: str) -> str:
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
head = make_tag("head")
center = make_tag("center")
title = make_tag("title")
html = make_tag("html")
body = make_tag("body")
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