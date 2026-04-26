from abc import ABC
from mkdocs.parser import GTag

class Template(ABC):
    def take_tag(self, tag: GTag): ...