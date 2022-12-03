import fileinput
from itertools import chain
def get_priority(char: str):
    if len(char) > 1:
        raise TypeError("Character expected")

    if ord(char) >= ord('a') and ord(char) <= ord('z'):
        return ord(char) - ord('a') + 1

    if ord(char) >= ord('A') and ord(char) <= ord('Z'):
        return ord(char) - ord('A') + 27

    raise IndexError("Provided character not in the alphabet")

def split_rucksack(lines: str):
    compartments = [
        (l[:len(l)//2], l[len(l)//2:]) for l in lines
    ]
    overlaps = chain(*[
        (set(l) & set(r)) for l,r in compartments
    ])
    return sum([get_priority(i) for i in overlaps])

if __name__ == "__main__":
    with fileinput.FileInput() as f:
        lines = list(f)
        print(split_rucksack(lines))
