import utils, re

data_ex = [
    "..X...",
    ".SAMX.",
    ".A..A.",
    "XMAS.S",
    ".X....",
]
data_ex2 = [
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX",
]
data = utils.readfile("data/day04.txt")


def get_potential_vectors(x, y, max_x, max_y):
    vectors = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    vectors = list(
        filter(
            lambda v: x + v[0] * 3 >= 0
            and x + v[0] * 3 <= max_x
            and y + v[1] * 3 >= 0
            and y + v[1] * 3 <= max_y,
            vectors,
        )
    )
    return vectors


assert get_potential_vectors(0, 0, 2, 2) == []
assert get_potential_vectors(0, 0, 3, 3) == [[0, 1], [1, 1], [1, 0]]
assert get_potential_vectors(0, 0, 1, 3) == [[0, 1]]
assert get_potential_vectors(1, 1, 4, 4) == [[0, 1], [1, 1], [1, 0]]
assert get_potential_vectors(3, 3, 3, 3) == [[0, -1], [-1, -1], [-1, 0]]


def count_from_x(data, x, y):
    maxx = len(data) - 1
    maxy = len(data[0]) - 1
    xmas_count = 0
    for vect in get_potential_vectors(x, y, maxx, maxy):
        if (
            data[x + vect[0]][y + vect[1]] == "M"
            and data[x + vect[0] * 2][y + vect[1] * 2] == "A"
            and data[x + vect[0] * 3][y + vect[1] * 3] == "S"
        ):
            xmas_count += 1
    return xmas_count


assert count_from_x(data_ex, 0, 2) == 1
assert count_from_x(data_ex, 3, 0) == 1
assert count_from_x(data_ex, 1, 1) == 0


def day04(data):
    sum = 0
    for x, line in enumerate(data):
        for y, letter in enumerate(line):
            if letter == "X":
                sum += count_from_x(data, x, y)

    return sum


assert day04(data_ex) == 4
assert day04(data_ex2) == 18

print(day04(data))


data_ex3 = ["M.S", ".A.", "M.S"]

data_ex4 = [
    ".M.S......",
    "..A..MSMS.",
    ".M.S.MAA..",
    "..A.ASMSM.",
    ".M.S.M....",
    "..........",
    "S.S.S.S.S.",
    ".A.A.A.A..",
    "M.M.M.M.M.",
    "..........",
]


def is_xmas_from_A(data, x, y):
    maxx = len(data) - 1
    maxy = len(data[0]) - 1    
    if x < 1 or y < 1 or x >= maxx or y >= maxy:
        return False
    count = 0
    for vect in [[1, 1], [1, -1], [-1, -1], [-1, 1]]:
        if (
            data[x - vect[0]][y - vect[1]] == "M"
            and data[x + vect[0]][y + vect[1]] == "S"
        ):
            count += 1
    if count == 2:
        return True
    return False


assert is_xmas_from_A(data_ex3, 1, 1) == 1
assert is_xmas_from_A(data_ex3, 2, 2) == 0


def day04_B(data):
    sum = 0
    for x, line in enumerate(data):
        for y, letter in enumerate(line):
            if letter == "A":
                sum += 1 if is_xmas_from_A(data, x, y) else 0

    return sum

assert day04_B(data_ex4) == 9
print(day04_B(data))