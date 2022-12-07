import fileinput
import shlex
from collections import defaultdict
from enum import Enum
from functools import reduce
from itertools import chain, takewhile, tee
from pathlib import PurePath
from typing import Dict, Iterable, NamedTuple, NewType, Tuple, TypedDict

NEEDED_SPACE = 300_00_000
TOTAL_SPACE = 700_00_000


class File(NamedTuple):
    name: PurePath
    size: int


def is_command(inp: str) -> bool:
    return inp.startswith("$")


def is_cd(inp: str) -> bool:
    return is_command(inp) and "cd" in inp


def cd(line: str, currpath: PurePath) -> PurePath:
    cmd = shlex.split(line[1:])
    match cmd:
        case ["cd", ".."]:
            return currpath.parent
        case ["cd", "/"]:
            return PurePath("/")
        case ["cd", d]:
            return currpath / d
        case default:
            raise ValueError("Invalid command")


def execute_file(lines: Iterable) -> dict:
    p = PurePath()
    sizes: Dict[PurePath, int] = {PurePath("/"): 0}
    for line in lines:
        match shlex.split(line):
            case ["$", "cd", _]:
                p = cd(line, p)
            case ["$", "ls"] | ["dir", _]:
                pass
            case [size, fname]:
                if p in sizes:
                    sizes[p] += int(size)
                else:
                    sizes[p] = int(size)
    for n, s in sizes.copy().items():
        for folder in n.parents:
            if folder in sizes:
                sizes[folder] += s
            else:
                sizes[folder] = s

    return sizes


def pt1(lines: list[str]) -> int:
    files = execute_file(lines)
    sizes = (s for _, s in files.items() if s <= 100000)
    return sum(sizes)


def pt2(lines: list[str]) -> int:
    tree = execute_file(lines)
    disk_usage = tree[PurePath("/")]
    unused_space = TOTAL_SPACE - disk_usage
    print(f"Total is {unused_space}")
    valid_dirs = ((f, s) for f, s in tree.items() if (unused_space + s) >= NEEDED_SPACE)
    smallest_dir = min(s for _, s in valid_dirs)
    return smallest_dir


if __name__ == "__main__":
    with fileinput.FileInput() as f:
        lines = list(f)
        print(pt1(lines))
        print(pt2(lines))
