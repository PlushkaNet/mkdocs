from typing import Iterable, Union, Generator, Optional
from collections import OrderedDict


class Tag:
    def __init__(self, name: str, value: Optional[str]=None, end:str="\n", subtags: dict[str, str] = {}):
        self.name = name
        self.value = value
        self.end = end
        self.subtags = subtags


    def __eq__(self, other: Tag) -> bool:
        return (self.name == other.name and self.value == other.value and self.end == other.end and self.subtags == other.subtags)
    

    def __repr__(self) -> str:
        return f"Tag(name: {self.name}, value: {self.value}, end: {self.end}, subtags: {self.subtags})"


class LTag:
    def __init__(self, tag: Tag, child: Optional[str]=None):
        self.tag: Tag = tag
        self.child = child

    
    def __eq__(self, other: LTag) -> bool:
        return (self.tag == other.tag and self.child == other.child)


    def __repr__(self) -> str:
        return f"LTag(tag: {self.tag}, child: {self.child})"


class GTag:
    def __init__(self, tag: Tag, child: Optional[str]=None, ltags: Optional[list[LTag]]=None):
        self.tag: Tag = tag
        self.child = child
        self.ltags = ltags or []

    
    def add_ltag(self, tag: LTag):
        self.ltags.append(tag)


    def __eq__(self, other: GTag) -> bool:
        return (self.tag == other.tag and self.child == other.child and self.ltags == other.ltags)
    

    def __repr__(self) -> str:
        return f"GTag(tag: {self.tag}, child: {self.child}, ltags: {self.ltags})"


def load_file(filename: str) -> Generator[str]:
    with open(filename, "r", encoding="utf-8") as file:
        # delegates line parsing
        for i in file: yield i


# basic function to parse CMD args (unused)
def parse_args(line: str, quotes: list[str] = ['"', "'"]) -> list[str]:
    args: list[str] = []

    buffer: str = ""
    qo: bool = False # quotes opened
    q: str = '' # quote that has been opened
    for i in line:
        if qo:
            if i == q:
                qo = False
                args.append(buffer)
                buffer = ""
            else:
                buffer += i # DUPLICATE
        elif i in quotes:
            qo = True
            q = i
        elif i.isspace() and buffer:
            args.append(buffer)
            buffer = ""
        else:
            buffer += i # DUPLICATE
    
    # post check
    if buffer:
        if qo: raise ValueError(f"{q} was never closed")
        else: args.append(buffer)

    return args


# parses key-value args like:
# arg = value secarg = secvalue posarg1 posarg2 newarg = newvalue
# will return {"arg":"value", "secarg":"secvalue", "posarg1":None, "posarg2":None, "newarg":"newvalue"}
def parse_eq_parts(line: str, quotes: list[str] = ['"', "'"]) -> OrderedDict[str, Optional[str]]:
    args: OrderedDict[str, Optional[str]] = OrderedDict()

    k: str = "" # key buffer
    ws: bool = False # whitespace was found before
    eq: bool = False # equal (=) found
    buffer: str = "" # common buffer
    qo: bool = False # quotes opened
    q: str = "" # quote that has been opened

    for i in line:
        if qo:
            if i == q:
                qo = False
            else:
                buffer += i
        elif i in quotes:
            # quotes opening scenario
            if buffer and ws: # DUBLICATE
                args[buffer] = None
                buffer = ""
            qo = True
            q = i
        elif i == "=":
            if eq == True:
                raise ValueError('"=" dublicate')
            if not buffer:
                raise ValueError("no key for the value found")
            eq = True
            k = buffer
            buffer = ""
        elif not i.isspace():
            if buffer and ws: # DUBLICATE
                args[buffer] = None
                buffer = ""
            buffer += i
            ws = False
        else:
            ws = True
            # if character is space, do check
            if eq and buffer:
                args[k] = buffer
                eq = False
                buffer = ""

    if qo: raise ValueError(f"{q} was never closed")
    if eq and not buffer: raise ValueError(f'no declaration after "="')
    if buffer:
        if eq: args[k] = buffer
        else: args[buffer] = None

    return args


def triangle_parse(line: str) -> Optional[str]:
    istart: int = 0
    iend: int = 0
    # searching opening "<" (if exists)
    for i in range(0, len(line)):
        # check for other symbols before searched
        if line[i] == "<":
            istart = i+1
            break
        elif not line[i].isspace(): # DUBLICATE
            return None
    # searching closing ">" (reversally)
    for i in range(len(line)-1, 0, -1):
        if line[i] == ">":
            iend = i
            break
        elif not line[i].isspace(): # DUBLICATE
            return None
    # exiting on empty string
    if iend == 0: return None
    # returning only triangle content with leading and trailing <> removed
    return line[istart:iend]


# parses tag body
def parse_tagbody(line: str) -> Tag:
    args: OrderedDict[str, Optional[str]] = parse_eq_parts(line)
    k, v = list(args.items())[0]
    args.pop(k) # removes first as it will passed directly to Tag
    end: Optional[str] = args.pop("end", default="\n")
    return Tag(k, v, end, args)


# parses global tag
def parse_gtag(line: str) -> Optional[GTag]:
    # trying to parse triangle
    tbody: Optional[str] = triangle_parse(line)
    if tbody == None: return None
    
    # parsing triangle tag body
    return GTag(parse_tagbody(tbody))


# parses local tag
def parse_ltag(line: str) -> LTag:
    return LTag(parse_tagbody(line))


# removes whitespaces and compares left and right values
# 10 - "\n" (ASCII), 9 - "\t" (ASCII), 32 - " " (ASCII)
def no_ws_compare(l: str, r: str, transtable: dict[int, str] = {10:"", 9:"", 32:""}) -> bool:
    return l.translate(transtable) == r.translate(transtable)


# {gtag: {child: str, ltags: [ltag, ltag, ltag, ltag]}}
# UNDONE
def parse_tree(content: Union[Iterable[str], Generator[str]]) -> list[GTag]:
    # iterates by lines
    gtags: list[GTag] = []
    # runtime variables
    gtag: Optional[GTag] = None # global tag
    ltag: Optional[LTag] = None # buffer local tag
    child: str = ""
    parsing_child_for: str = "gtag" # "gtag" | "ltag"
    parsing_child_end: str = "\n"
    parsing_child: bool = False
    for line in content:
        if not parsing_child:
            if line and not line.isspace():
                # trying to parse GTag first
                try:
                    new_gtag: Optional[GTag] = parse_gtag(line)
                except ValueError as e:
                    raise ValueError(f"error while parsing GTag in the following line:\n   {line}\nexception:\n{e}")
                if new_gtag:
                    if gtag: gtags.append(gtag)
                    gtag = new_gtag
                    parsing_child = True
                    parsing_child_for = "gtag"
                    parsing_child_end = new_gtag.tag.end
                elif gtag: # if GTag is defined
                    try:
                        ltag = parse_ltag(line)
                    except ValueError as e:
                        raise ValueError(f"error while parsing LTag in the following line:\n   {line}\nexception:\n{e}")
                    parsing_child = True
                    parsing_child_for = "ltag"
                    parsing_child_end = ltag.tag.end
                else:
                    raise ValueError(f"error in the following line:\n   {line}\nexception:\nunrecongized content")
        elif parsing_child and no_ws_compare(line, parsing_child_end):
            parsing_child = False
            if parsing_child_for == "gtag": # DUBLICATE
                gtag.child = child
            elif parsing_child_for == "ltag":
                ltag.child = child
                gtag.add_ltag(ltag)
            child = ""
        else:
            child += line
    
    # post-cycle complete checks
    if parsing_child:
        if parsing_child_for == "gtag": # DUBLICATE
            gtag.child = child
        elif parsing_child_for == "ltag":
            ltag.child = child
            gtag.add_ltag(ltag)

    if gtag:
        gtags.append(gtag)

    return gtags


def split_by_lines(text: str) -> Generator[str]:
    line: str = ""
    for i in text:
        line += i
        if i == "\n":
            yield line
            line = ""
    yield line