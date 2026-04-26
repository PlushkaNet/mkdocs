# TESTS file

from typing import Any, Optional
from mkdocs.parser import (parse_tree,
                        parse_eq_parts,
                        triangle_parse,
                        GTag, Tag, LTag,
                        OrderedDict)


tests: dict[str, Any] = {}


# decorator for registering test functions
def basic_test(test_name: str):
    def callback_handler(callback):
        def wrapper() -> None:
            print(f"Begin of testing {test_name}")
            callback()
            print(f"{test_name} has been tested successfully!")

        # registers this test in tests
        global tests
        tests[test_name] = wrapper

        return wrapper
    return callback_handler


# couple of tests for parse_eq_parts
@basic_test("parse_eq_parts")
def parse_eq_parts_test():
    assert parse_eq_parts("arg = value secarg = secvalue posarg1 posarg2 newarg = newvalue") == {"arg":"value", "secarg":"secvalue", "posarg1":None, "posarg2":None, "newarg":"newvalue"}
    assert parse_eq_parts("'custom arg'  = 2 'hello world!' 'hi' arg =  'value with spaces'") == {"custom arg":"2", "hello world!":None, "hi":None, "arg":"value with spaces"}


@basic_test("triangle_parse")
def triangle_parse_test():
    assert triangle_parse("<hello>") == "hello"
    assert triangle_parse("<world is huge>") == "world is huge"
    assert triangle_parse("world>") == None


@basic_test("parse_tree")
def parse_tree_test(): 
    assert parse_tree([
        "<title>",
        "Ordinary title",
        "\n",
        "<desc end=!end>",
        "Beggining of the desc",
        "End of the desc",
        "!end"
    ]) == [
        GTag(Tag("title", None, "\n", OrderedDict()), "Ordinary title", []),
        GTag(Tag("desc", None, "!end", OrderedDict()), "Beggining of the descEnd of the desc", [])]

    assert parse_tree(
        ["<title small end=!>\n",
        "Small title!\n",
        "!\n",
        "sub title end=!\n",
        "subtitletext1\n",
        "substitletext2\n",
        "!\n",
        "\n", "\n\t"]) == [
            GTag(
                Tag("title", None, "!", {"small":None}),
                "Small title!\n",
                ltags=[
                    LTag(
                        Tag("sub", None, "!", {"title":None}),
                        "subtitletext1\nsubstitletext2\n")
                ]
            )
        ]


def main(test_name: Optional[str] = None):
    if test_name:
        tests.get(test_name, lambda: print("no test with the following name was found"))()
    else:
        print("Running all tests")
        for f in tests.values():
            f()
        print("All tests has been successfully completed!")