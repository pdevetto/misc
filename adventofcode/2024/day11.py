import utils, re
import itertools

data_ex = "125 17"
data = "112 1110 163902 0 7656027 83039 9 74"


def stone_rule(stone):
    lng = len(stone)
    if stone == "0":
        return ["1"]
    if lng % 2 == 0:
        return [str(stone[0 : lng // 2]), str(int(stone[lng // 2 :]))]
    return [str(int(stone) * 2024)]


assert stone_rule("0") == ["1"]
assert stone_rule("1") == ["2024"]
assert stone_rule("10") == ["1", "0"]
assert stone_rule("99") == ["9", "9"]
assert stone_rule("999") == ["2021976"]


def blink(stones):
    new_stones = {}
    for stone, count in stones.items():
        for a_stone in stone_rule(stone):
            new_stones[a_stone] = new_stones.get(a_stone, 0) + count
    return new_stones

assert blink({"125":1, "17":1}) == {"253000":1, "1":1, "7":1}
assert blink({"253000":1, "1":1, "7":1}) == {"253":1, "0":1, "2024":1, "14168":1}
assert blink({"253":1, "0":1, "2024":1, "14168":1}) == {"512072":1, "1":1, "20":1, "24":1, "28676032":1}

def day11(data, n):
    stones = data.split(" ")
    stones = dict((k, len(list(gp))) for (k, gp) in itertools.groupby(stones))
    for i in range(n):
        print(i, len(stones))
        stones = blink(stones)
    return sum(stones.values())

assert (day11(data_ex, 1)) == 3
assert (day11(data_ex, 2)) == 4
assert (day11(data_ex, 3)) == 5
assert (day11(data_ex, 4)) == 9
assert (day11(data_ex, 5)) == 13
assert (day11(data_ex, 6)) == 22
print(day11(data, 25))
print(day11(data, 75))
