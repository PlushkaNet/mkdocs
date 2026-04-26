from mkdocs.py2html import *


def main():
    print(
        html(
            head(
                meta(None, charset="utf-8"),
                title("Hello from py2html!")
            ),
            body(
                h1("Hi!")
            )
        )
    )
