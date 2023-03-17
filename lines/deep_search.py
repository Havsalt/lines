import os
from collections.abc import Iterable


def map_files(directory: str, callback, /, *, depth: int = -1, filters: Iterable = os.path.isfile, _level: int = 1):
    """Recursivly map directory file paths to callback

    Args:
        directory (str): _description_
        callback (function): function to call on each file
        depth (int, optional): recursive depth (passing `-1` means no limit)
        filters (function, optional): filter type of files, may be a list of filters (defaults to `os.path.isfile`)
        _level (int, private): keeps track of current depth
    """
    try:
        files = os.listdir(directory)
    except PermissionError:
        return
    target = len(files)
    for step, name in enumerate(files):
        path = os.path.join(directory, name)

        if filters == None:
            callback(path, _level, step, target)
        elif isinstance(filters, Iterable):
            if any(filter_func(path) for filter_func in filters):
                callback(path, _level, step, target)
        elif filters(path):
            callback(path, _level, step, target)

        if os.path.isdir(path):
            if _level >= depth and not depth == -1:  # -1 is iterate all
                continue
            map_files(path, callback, depth=depth,
                      filters=filters, _level=(_level + 1))
