import fileinput
from typing import NamedTuple


class Range(NamedTuple):
    first: int
    second: int


class RangePair(NamedTuple):
    first: Range
    second: Range


def get_sections(r: str) -> Range:
    start, end = r.split("-")
    return Range(int(start), int(end))


def get_ranges(lines: list[str]) -> list[RangePair]:
    return [
        RangePair(get_sections(first), get_sections(second))
        for first, second in [l.split(",") for l in lines]
    ]


def range_contains(r1: Range, r2: Range) -> bool:
    return (min(r1) >= min(r2) and max(r1) <= max(r2)) or (
        min(r2) >= min(r1) and max(r2) <= max(r1)
    )


def get_contains(pairs: list[RangePair]) -> list[RangePair]:
    return [p for p in pairs if range_contains(p.first, p.second)]


def range_overlaps(r1: Range, r2: Range) -> bool:
    return min(r1) <= max(r2) and max(r1) >= min(r2)


def get_overlaps(pairs: list[RangePair]) -> list[RangePair]:
    return [p for p in pairs if range_overlaps(p.first, p.second)]


if __name__ == "__main__":
    with fileinput.FileInput() as f:
        lines = list(f)
        ranges = get_ranges(lines)
        c = get_contains(ranges)
        print(len(c))

        o = get_overlaps(ranges)
        print(len(o))
