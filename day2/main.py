import fileinput
from collections import namedtuple
from enum import IntEnum
from functools import reduce
from itertools import chain
from typing import Any, Iterable, Literal, NamedTuple, TypedDict


class Rps(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(IntEnum):
    LOSS = 0
    DRAW = 3
    WIN = 6


class ChoiceResult(NamedTuple):
    result: Result
    choice: Rps


rps_beats: dict[Rps, Rps] = {
    Rps.ROCK: Rps.SCISSORS,
    Rps.PAPER: Rps.ROCK,
    Rps.SCISSORS: Rps.PAPER,
}

rps_loses: dict[Rps, Rps] = {v: k for k, v in rps_beats.items()}


def code_to_choice(code: str) -> Rps:
    match code:
        case "A" | "X":
            return Rps.ROCK
        case "B" | "Y":
            return Rps.PAPER
        case "C" | "Z":
            return Rps.SCISSORS
        case _:
            raise TypeError("Invalid symbol")


def beats(opp: Rps, player: Rps) -> Result:
    if opp == player:
        return Result.DRAW

    if rps_beats[opp] == player:
        return Result.LOSS

    return Result.WIN


def guide_pt1(lines: list[str]) -> int:
    strategy_guide = [[code_to_choice(y) for y in x.split()] for x in lines]
    won = [beats(*game) for game in strategy_guide]
    results = (ChoiceResult(g, r[1]) for r, g in zip(strategy_guide, won))
    return sum(chain(*results))


def beats_pt2(opp: str, player: str) -> ChoiceResult:

    oppChoice = code_to_choice(opp)
    match (player, oppChoice):
        case ("Y", _):
            return ChoiceResult(Result.DRAW, oppChoice)
        case ("X", _):
            return ChoiceResult(Result.LOSS, rps_beats[oppChoice])
        case ("Z", _):
            return ChoiceResult(Result.WIN, rps_loses[oppChoice])
        case default:
            raise TypeError("Invalid option provided")


def guide_pt2(lines: list[str]) -> int:
    strategy_guide = [tuple(x.split()) for x in lines]
    choices = [beats_pt2(*move) for move in strategy_guide]
    return sum(chain(*choices))


if __name__ == "__main__":
    with fileinput.FileInput() as f:
        lines = list(f)
        print(guide_pt1(lines))
        print(guide_pt2(lines))
