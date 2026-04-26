from mkdocs import parser, makehtml, py2html, tests

version = "0.11"

# update 0.11
# - added logging for some methods (program.py, makehtml.py)
# - implemented method for splitting paragraphs in html by whitespaces (\n)
# - now user will see an exception details if something went wrong
# - added override possible argument in process_directory (program.py), but there's no flag to activate it in __main__.py