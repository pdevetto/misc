import utils, re
import itertools

data_ex = [
    "89010123",
    "78121874",
    "87430965",
    "96549874",
    "45678903",
    "32019012",
    "01329801",
    "10456732",
]
data = utils.readfile("data/day10.txt")





def trailhead_score(trailhead, maph, part2=False):
    next_position_delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    trails = [(trailhead, 0)]
    score = 0
    cont = {}
    passed = []
    while len(trails) != 0:
        (trail, height) = trails.pop()
        if height == 9:
            score += 1
        else:
            for delta in next_position_delta:
                next_k = utils.k_delta(trail, delta)
                if height == 0 and next_k in maph:
                    print(trail, next_k)
                if (
                    next_k in maph
                    and maph[next_k] == height + 1
                    and (part2 or next_k not in passed)
                ):
                    passed.append(next_k)
                    cont[maph[next_k]] = cont.get(maph[next_k], 0) + 1
                    trails.append((next_k, height + 1))
        print(">> trail ", trail, height, " : ", score, " / ", trails)
    print(" >> Score = ", score, " and ", cont)
    return score


def day10(data, part1=True):
    maph = {}
    trailhead = []
    maxi = len(data)
    maxj = len(data[0])
    for i, line in enumerate(data):
        for j, height in enumerate(line):
            k = utils.xy2k(i, j)
            maph[k] = int(height)
            if height == "0":
                trailhead.append(k)
    scores = 0
    scores_2 = 0
    for k in trailhead:
        score1 = trailhead_score(k, maph)
        score2 = trailhead_score(k, maph, part2=True)
        scores += score1
        scores_2 += score2

    print(scores, " and ", scores_2)
    return scores, scores_2


assert (day10(data_ex)) == (36, 81)
print(day10(data))
