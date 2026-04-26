from sys import argv
from mkdocs import tests
from mkdocs.program import process_file, process_directory


def argv_check(expected: int) -> bool:
    if len(argv) != expected:
        print(f"error: given number of args doesn't fit expected number ({expected})")
        return False
    return True


if __name__ == "__main__":
    if len(argv) > 1:
        if argv[1] == "test":
            if len(argv) > 2:
                if argv[2] == "parser":
                    if len(argv) > 2 and len(argv) <= 4:
                        tests.parsertest.main(argv[3] if len(argv) == 4 else None)
                    else:
                        print("error: more than 3 arguments were given, expected 2")
                elif argv[2] == "py2html":
                    tests.py2htmltest.main()
            else:
                print("Running py2html and parser tests")
                tests.parsertest.main()
                tests.py2htmltest.main()
                print("All tests passed successfully!")
        elif argv[1] == "file":
            if argv_check(4):
                try:
                    process_file(argv[2], argv[3])
                except:
                    print("error: failed to read/create file")
        elif argv[1] == "dir":
            if argv_check(4):
                try:
                    process_directory(argv[2], argv[3])
                except:
                    print("error: failed to read/create files")
        else:
            print("error: undefined argument")
    else:
        print("error: no args was specified")