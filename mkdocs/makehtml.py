from mkdocs.parser import GTag
from mkdocs.templates.oldoc_template import OlDOC_Template
import logging

def build_html(gtags: list[GTag]) -> str:
    logging.info("(build_html) using OlDOC Template by default. There will be more in the future")
    page = OlDOC_Template()
    for gtag in gtags:
        page.take_tag(gtag)
    
    return page.build()