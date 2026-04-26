import logging
from mkdocs.makehtml import build_html
from mkdocs.parser import GTag, parse_tree
import logging
import os

# TODO add different processors

def process_file(input: str, output: str):
    logging.info(f"(process_file) processing file: {input}")
    with open(input, "r", encoding="utf-8") as infile:
        tree: list[GTag] = parse_tree(infile.readlines())
        html: str = build_html(tree)
    
    logging.info(f"(process_file) saving compiled output to: {output}")
    with open(output, "w", encoding="utf-8") as outfile:
        outfile.write(html)


def process_directory(indirpath: str, outdirpath: str, override=False):
    if os.path.exists(outdirpath):
        if override:
            logging.warning(f"(process_directory) {outdirpath} already exists, but override set to 1")
            os.rmdir(outdirpath)
        else:
            raise ValueError(f"(process_directory) {outdirpath} exists, and override set to 0")
    logging.log(f"(process_directory) creating directory {outdirpath}")

    os.mkdir(outdirpath)
    dir: list[str] = os.listdir(indirpath)
    for i in dir:
        ipath: str = os.path.join(indirpath, i)
        ioutpath: str = os.path.join(outdirpath, i)
        if os.path.isdir(ipath):
            process_directory(ipath, ioutpath)
        elif ipath.endswith(".doc"):
            process_file(ipath, ioutpath.removesuffix(".doc")+".html")