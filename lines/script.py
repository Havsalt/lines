import sys
import os
import time


# activate ANSI escape codes
os.system("")


def get_flags():
    flags = []
    for arg in sys.argv:
        if arg[0:1] == "--":
            flags.append(arg)
        elif arg[0] == "-":
            flags.append(arg)
    return flags


def main():
    DELTA = 0.05  # time between reading content in folder
    lines, files, folders, errors = (0, 0, 0, 0)

    directory = os.getcwd()
    flags = get_flags()
    # flags
    FLAG_IGNORE_BLANK_LINE = "-i" in flags or "--ignore-blank" in flags
    FLAG_INSTANT_COUNT = "-f" in flags or "--fast-count" in flags
    #FLAG_DEEP_SEARCH = "-d" in flags or "--deep-search" in flags
    # counter
    size = len(os.listdir(directory))
    sys.stdout.write("\u001b[37;1mData: [" + " " * size)
    sys.stdout.write("]")
    sys.stdout.write("\r\u001b[7C")  # 7 = len("Data: ")
    sys.stdout.write("\u001b[0m")
    sys.stdout.flush()

    for path in os.listdir(directory):
        file = os.path.join(directory, path)
        if os.path.isfile(file):
            try:
                files += 1  # count files independent on errors
                with open(file, "r", encoding='utf-8') as f:
                    # NOTE: idk if I should do +1
                    if FLAG_IGNORE_BLANK_LINE:
                        lines += len([line for line in f.readlines()
                                     if line != "\n"])
                    else:
                        lines += len(f.readlines())
                # is file
                sys.stdout.write("\u001b[32m#\u001b[0m")
                sys.stdout.flush()
            except (PermissionError, UnicodeDecodeError):
                # is error
                sys.stdout.write("\u001b[31m#\u001b[0m")
                sys.stdout.flush()
                errors += 1
        else:
            # is folder
            sys.stdout.write("\u001b[33m#\u001b[0m")
            sys.stdout.flush()
            folders += 1
        if not FLAG_INSTANT_COUNT:
            time.sleep(DELTA)
    sys.stdout.write("\n")

    directory_name = directory.split("\\")[-1]
    OK = f"\u001b[32mOK\u001b[0m"
    ERROR = f"{errors} files denied access or could not be decoded"
    content = [
        f"\u001b[37;1mIn directory \u001b[32m{directory_name}\u001b[37;1m:",
        f"  \u001b[35;1m[Lines]\u001b[0m: \u001b[35m{lines}\u001b[0m",
        f"  \u001b[32;1m[Files]\u001b[0m: \u001b[32m{files}\u001b[0m",
        f"  \u001b[33;1m[Folds]\u001b[0m: \u001b[33m{folders}\u001b[0m",
        f"  \u001b[31;1m[Error]\u001b[0m: \u001b[31m{ERROR if errors != 0 else OK}\u001b[0m"
    ]
    # display
    for item in content:
        print(item)
        if not FLAG_INSTANT_COUNT:
            time.sleep(DELTA)

    # print("Lines in directory '\u001b[32m" +
    #      directory_name + "\u001b[0m':\u001b[35m", str(lines) + "\u001b[0m")


# execute
if __name__ == "__main__":
    main()
