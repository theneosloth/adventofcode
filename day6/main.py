import fileinput
from itertools import islice, takewhile
from typing import Generator


def get_chunks(line: str, chunk_size: int) -> Generator:
    for i in range(0, len(line)):
        if i + chunk_size <= len(line):
            yield islice(line, i, i + chunk_size)


def get_start_of_packet(line: str, chunk_size: int) -> int:
    dupes = takewhile(
        lambda x: len(x) < chunk_size,
        (set(chunk) for chunk in get_chunks(line, chunk_size)),
    )
    return chunk_size + len(list(dupes))


if __name__ == "__main__":
    with fileinput.FileInput() as f:
        line = f.readline()
        print(get_start_of_packet(line, 4))
        print(get_start_of_packet(line, 14))
