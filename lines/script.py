import argparse
import os
import sys
import time

import deep_search


# activate ANSI escape codes
os.system("")

# constants
DELTA = 0.05  # time between printing content from folder
ANY_EXTENSION = "any"
EMPTY = "\u001b[37;1m" + "-"
L_BRACKET = "\u001b[37;1m" + "["
R_BRACKET = "\u001b[37;1m" + "]"
LINE_RESET = "\r" + " " * 96 + "\r"

FILE = "\u001b[32;1m" + "#"
FOLD = "\u001b[33;1m" + "#"
ERROR = "\u001b[31;1m" + "#"
# FILE = "#"
# FOLD = "/"

# argument parser
parser = argparse.ArgumentParser(
    prog="lines", description="== Count lines ==")
parser.add_argument("extensions", nargs="*", default=ANY_EXTENSION,
                    help="filter extensions of files. defaults to any")
parser.add_argument("-r", action="store", type=int, nargs="?",
                    dest="depth", default=1, help="count lines recursively. depth level is optional")
parser.add_argument("-f", "--fast", action="store_true",
                    dest="fast_mode", help="compute next file without delay")
parser.add_argument("-i", "--ignore-blank", action="store_true",
                    dest="ignore_blank", help="ignore empty lines")


def main() -> None:
    args = parser.parse_args()
    lines = 0
    files = 0
    folds = 0
    errors = set()
    directory = os.getcwd()
    directory_name = directory.split(os.path.sep)[-1]

    # if initial directory is empty
    f_string = f"{LINE_RESET}\u001b[37;1mData: {L_BRACKET}{R_BRACKET}"
    sys.stdout.write(f_string)
    sys.stdout.flush()

    progress = {}

    def callback(path: str, level: int, step: int, target: int):
        nonlocal lines, files, folds, errors, progress
        global ERROR

        if not level in progress.keys():
            progress[level] = ""

        if os.path.isfile(path):
            if args.extensions != ANY_EXTENSION:
                _fpath, extension = os.path.splitext(path)
                if not extension[1:] in args.extensions:  # '.py'[1:] -> 'py'
                    return
            files += 1
            try:
                f = open(path, "r")
                if args.ignore_blank:
                    lines += len([line for line in f.readlines()
                                 if line != "\n"])
                else:
                    lines += len(f.readlines())
                f.close()

                progress[level] += FILE
            except (PermissionError, UnicodeDecodeError) as error:
                errors.add(error.__class__.__name__)
                progress[level] += ERROR

        elif os.path.isdir(path):
            folds += 1
            progress[level] += FOLD

        # if (args.fast_mode and level == 1) or not args.fast_mode:  # top level
        if args.fast_mode:
            if level != 1:
                return
        diff = (target - step)
        current = progress[level] + EMPTY * (target - step - 1)
        ansi_code = f"\r\u001b[{7 + step}C"  # cursor position
        f_string = f"{LINE_RESET}\u001b[37;1mData: {L_BRACKET}{current}{R_BRACKET}{ansi_code}"
        sys.stdout.write(f_string)
        sys.stdout.flush()
        if not args.fast_mode:
            time.sleep(DELTA)

    # deep search level of `0` or `None` is treated as infinite
    depth = (-1 if args.depth in (0, None) else args.depth)
    deep_search.map_files(directory, callback, depth=depth, filters=[
                          os.path.isfile, os.path.isdir])
    top_level = progress[1]
    f_string = f"{LINE_RESET}\u001b[37;1mData: {L_BRACKET}{top_level}{R_BRACKET}\n"
    sys.stdout.write(f_string)
    sys.stdout.flush()

    # content to display
    OK = f"\u001b[32mOK\u001b[0m"
    ERROR = f"{', '.join(errors)}: files denied access or could not be decoded"
    content = [
        f"\u001b[37;1mIn directory \u001b[32m{directory_name}\u001b[37;1m:\n",
        f"  \u001b[35;1m[Lines]\u001b[0m: \u001b[35m{lines}\u001b[0m\n",
        f"  \u001b[32;1m[Files]\u001b[0m: \u001b[32m{files}\u001b[0m\n",
        f"  \u001b[33;1m[Folds]\u001b[0m: \u001b[33m{folds}\u001b[0m\n",
        f"  \u001b[31;1m[Error]\u001b[0m: \u001b[31m{OK if errors == set() else ERROR}\u001b[0m"
    ]
    # display
    if args.fast_mode:
        sys.stdout.writelines(content)
    else:
        for item in content:
            sys.stdout.write(item)
            time.sleep(DELTA)


if __name__ == "__main__":
    main()
