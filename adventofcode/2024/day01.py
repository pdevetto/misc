import utils
import collections

data_ex = [
    "3   4",
    "4   3",
    "2   5",
    "1   3",
    "3   9",
    "3   3",
]
data = utils.readfile("data/day01.txt")


def day01(data):
    l = list(map(lambda n: list(filter(None, n.split(" "))), data))

    l1 = sorted(map(lambda n: int(n[0]), l))
    l2 = sorted(map(lambda n: int(n[1]), l))

    dist = 0
    for i, n in enumerate(l1):
        dist += abs(n - l2[i])
    return dist


assert day01(data_ex) == 11
print(day01(data))


def day01b(data):
    l = list(map(lambda n: list(filter(None, n.split(" "))), data))

    l1 = sorted(map(lambda n: int(n[0]), l))
    l2 = sorted(map(lambda n: int(n[1]), l))
    cnt = collections.Counter(l2)
    print(cnt)
    sim = 0
    for n in l1:
        sim += n * cnt.get(n, 0)
    return sim


assert day01b(data_ex) == 31
print(day01b(data))
