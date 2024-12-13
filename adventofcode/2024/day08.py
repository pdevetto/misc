import utils, re
import itertools

data_ex = [
    "............",
    "........0...",
    ".....0......",
    ".......0....",
    "....0.......",
    "......A.....",
    "............",
    "............",
    "........A...",
    ".........A..",
    "............",
    "............",
]
data = utils.readfile("data/day08.txt")


def xy2k(x, y) -> str:
    return f"{x}.{y}"


def k2xy(k) -> tuple[int, int]:
    return tuple(map(int, k.split(".")))


def k_in(k, maxi, maxj):
    i, j = k2xy(k)
    return i >= 0 and j >= 0 and i <= maxi and j <= maxj


assert k_in("4.3", 10, 10)
assert k_in("0.10", 10, 10)
assert k_in("10.0", 10, 10)
assert not k_in("12.3", 10, 10)
assert not k_in("2.12", 10, 10)
assert not k_in("-1.0", 10, 10)


def get_antinode(k1, k2):
    i1, j1 = k2xy(k1)
    i2, j2 = k2xy(k2)
    return xy2k(i1 - (i2 - i1), j1 - (j2 - j1)), xy2k(i2 - (i1 - i2), j2 - (j1 - j2))


assert (get_antinode("4.3", "5.5")) == ("3.1", "6.7")


def get_any_antinodes(k1, k2, maxi, maxj):
    i1, j1 = k2xy(k1)
    i2, j2 = k2xy(k2)
    antinodes = []
    delta = (i2 - i1, j2 - j1)

    di, dj = i1, j1
    while 0 <= di <= maxi and 0 <= dj <= maxj:
        antinodes.append(xy2k(di, dj))
        di = di - delta[0]
        dj = dj - delta[1]
    di, dj = i2, j2
    while 0 <= di <= maxi and 0 <= dj <= maxj:
        antinodes.append(xy2k(di, dj))
        di = di + delta[0]
        dj = dj + delta[1]
    return antinodes


assert (sorted(get_any_antinodes("1.2", "2.4", 10, 10))) == sorted(
    ["0.0", "1.2", "2.4", "3.6", "4.8", "5.10"]
)
print(sorted(["0.0", "1.2", "2.4", "3.6", "4.8", "5.10"]))


def day08(data, part1=True):
    max_i = len(data) - 1
    max_j = len(data[0]) - 1
    antennas = {}
    for i, line in enumerate(data):
        for j, letter in enumerate(line):
            if letter != ".":
                antennas[letter] = antennas.get(letter, []) + [xy2k(i, j)]
    antinodes = {}
    k_in_max = lambda k: k_in(k, max_i, max_j)
    for antenna, locations in antennas.items():
        print(f"Antena {antenna}")
        if len(locations) >= 2:
            for combi in itertools.combinations(locations, 2):
                if part1:
                    for antinode in filter(k_in_max, get_antinode(combi[0], combi[1])):
                        antinodes[antinode] = antinodes.get(antinode, []) + [antenna]
                else:
                    for antinode in get_any_antinodes(combi[0], combi[1], max_i, max_j):
                        antinodes[antinode] = antinodes.get(antinode, []) + [antenna]
    print(antinodes)
    return len(antinodes)


assert (day08(data_ex)) == 14
print(day08(data))

assert (day08(data_ex, False)) == 34
print(day08(data, False))
