import fileinput
from functools import reduce
from itertools import chain, islice

priority = int


def get_priority(char: str) -> priority:
    if len(char) > 1:
        raise TypeError("Character expected")

    if ord(char) >= ord("a") and ord(char) <= ord("z"):
        return ord(char) - ord("a") + 1

    if ord(char) >= ord("A") and ord(char) <= ord("Z"):
        return ord(char) - ord("A") + 27

    raise IndexError("Provided character not in the alphabet")


def split_rucksack(lines: list[str]) -> int:
    compartments = [(l[: len(l) // 2], l[len(l) // 2 :]) for l in lines]
    overlaps = chain.from_iterable([(set(l) & set(r)) for l, r in compartments])

    return sum([get_priority(i) for i in overlaps])


def get_badge(lines: list[str]) -> int:
    chunks = zip(*[iter(lines)] * 3)
    items = [[set(c.strip()) for c in group] for group in chunks]
    badges = [reduce(lambda a, b: a & b, i) for i in items]
    priorities = [get_priority(list(i)[0]) for i in badges]
    return sum(priorities)


if __name__ == "__main__":
    with fileinput.FileInput() as f:
        lines = list(f)
        print(split_rucksack(lines))
        print(get_badge(lines))
