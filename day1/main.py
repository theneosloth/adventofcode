import fileinput
from itertools import starmap
from collections import namedtuple

Result = namedtuple('Result', 'top_elf top_three_elves')

def get_calories(input: str):
    groups = [group.split() for group in input.split("\n\n")]
    int_groups = starmap(lambda *list: map(int, list), groups)
    sums = sorted(map(sum, int_groups))
    top_elf = sums[-1]
    top_three_elves = sum(sums[-3:])
    return Result(top_elf, top_three_elves)


if __name__ == "__main__":
    with open("input.txt") as f:
        print(get_calories(f.read()))