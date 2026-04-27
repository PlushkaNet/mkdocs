from typing import Optional
from mkdocs.templates.template import Template
from mkdocs.parser import GTag, split_by_lines, parse_tree
import mkdocs.py2html as h

class OlDOC_Template(Template):
    # TODO add related pages
    __slots__ = ["page_title", "body_title", "description", "usage", "examples"]
    def __init__(self):
        self.page_title: Optional[str] = None
        self.body_title: Optional[str] = None
        self.description: Optional[str] = None
        self.usage: Optional[str] = None
        self.examples: Optional[str] = None


    def take_tag(self, tag: GTag):
        if tag.tag.name in self.__slots__:
            self.__setattr__(tag.tag.name, tag.child)


    # TODO optimize
    def _build_examples(self) -> str:
        compl = ""
        
        if self.examples:
            gtags: list[GTag] = parse_tree(split_by_lines(self.examples))
            for gtag in gtags:
                if gtag.child:
                    compl += h.xmp(gtag.child) # snippet
                    if gtag.ltags and gtag.ltags[0].tag.name == "related":
                        relgtags: list[GTag] = parse_tree(split_by_lines(gtag.ltags[0].child))
                        for relgtag in relgtags:
                            if relgtag.tag.subtags.get("url"):
                                compl += h.p(h.a(relgtag.child, href=relgtag.tag.subtags["url"]))
                    compl += h.hr()

        return compl
    

    def build(self) -> str:
        return h.html(
            h.head(
                h.meta(charset="utf-8"),
                h.title(self.page_title) if self.page_title else ""
            ),
            h.body(
                h.insert(
                    h.center(
                        h.h1(self.body_title)
                    ), h.hr()
                ).If(self.body_title),
                h.insert(
                    h.h2("Description"),
                    h.p(h.pwrap(h.htmlify(self.description))),
                    h.hr()
                ).If(self.description),
                h.insert(
                    h.h2("Usage"),
                    h.spacing(4),
                    h.code(h.htmlify(self.usage)),
                    h.hr()
                ).If(self.usage),
                h.insert(
                    h.h2("Examples"),
                    h.hr(),
                    self._build_examples()
                ).If(self.examples)
            )
        )