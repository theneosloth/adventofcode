import fileinput
import re
from collections import deque
from copy import copy
from enum import Enum
from typing import Iterable, NamedTuple, Tuple

# Absolutely god awful 2 am coding
label = str
index = int
stack = deque[label]


class Command(NamedTuple):
    move_count: int
    move_from: int
    move_to: int


Crates = Tuple


def parse_line(line: str) -> Tuple:
    res = ()
    for i in range(1, len(line), 4):
        res = (*res, line[i])  # type: ignore
    return res


def parse_command(line: str) -> Command:
    words = line.split()
    num1, num2, num3 = words[1], words[3], words[5]
    return Command(int(num1), int(num2), int(num3))


def run_crates(lines: list[str]) -> Crates:

    sections = "".join(lines).split("\n\n")
    crates_section = sections[0].split("\n")
    num_lines = int(crates_section[-1].split()[-1])
    print(num_lines)
    crates_str = crates_section[:-1]
    commands_str = sections[1].split("\n")
    columns = [parse_line(line) for line in crates_str]
    crates = tuple(stack() for i in range(num_lines))
    for column in columns:

        index = 0
        for row in column:
            if row != " ":
                crates[index].append(row)
            index = index + 1
    commands = [parse_command(line) for line in commands_str if line != ""]

    for command in commands:
        execute_command_pt2(crates, command)

    return crates


def execute_command(crates: Crates, command: Command) -> Crates:
    for i in range(command.move_count):
        val = crates[command.move_from - 1].popleft()
        crates[command.move_to - 1].appendleft(val)
    return crates


def execute_command_pt2(crates: Crates, command: Command) -> Crates:

    buf = []
    for i in range(command.move_count):
        val = crates[command.move_from - 1].popleft()
        buf.append(val)
    print(buf)
    crates[command.move_to - 1].extendleft(buf[::-1])

    print(crates)
    return crates


def get_top(crates: Crates) -> str:
    return "".join(crate[0] for crate in crates)


if __name__ == "__main__":
    with fileinput.FileInput() as f:
        lines = list(f)
        crates = run_crates(lines)
        print(get_top(crates))
