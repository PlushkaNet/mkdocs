from mkdocs.makehtml import build_html
from mkdocs.parser import GTag, parse_tree
import os

# TODO add different processors

def process_file(input: str, output: str):
    with open(input, "r", encoding="utf-8") as infile:
        tree: list[GTag] = parse_tree(infile.readlines())
        html: str = build_html(tree)
    
    with open(output, "w", encoding="utf-8") as outfile:
        outfile.write(html)


def process_directory(indirpath: str, outdirpath: str):
    os.mkdir(outdirpath)
    dir: list[str] = os.listdir(indirpath)
    for i in dir:
        ipath = os.path.join(indirpath, i)
        ioutpath = os.path.join(outdirpath, i)
        if os.path.isdir(ipath):
            process_directory(ipath, ioutpath)
        elif ipath.endswith(".doc"):
            process_file(ipath, ioutpath.removesuffix(".doc")+".html")