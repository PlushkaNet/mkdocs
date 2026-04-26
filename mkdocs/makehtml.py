from mkdocs.parser import GTag
from mkdocs.templates.oldoc_template import OlDOC_Template

def build_html(gtags: list[GTag]) -> str:
    page = OlDOC_Template()
    for gtag in gtags:
        page.take_tag(gtag)
    
    return page.build()