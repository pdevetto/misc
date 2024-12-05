import utils

data_ex = [
    "7 6 4 2 1",
    "1 2 7 8 9",
    "9 7 6 2 1",
    "1 3 2 4 5",
    "8 6 4 4 1",
    "1 3 6 7 9",
]
data = utils.readfile("data/day02.txt")


def safe_line(line):
    l = list(map(int, line.split(" ")))
    delta = 0
    old = l[0]
    for n in l[1:]:
        if abs(n - old) not in [1, 2, 3]:
            return False
        if delta == 0:
            if n < old:
                delta = -1
            if n > old:
                delta = 1
        else:
            if (n < old and delta == 1) or (n > old and delta == -1):
                return False
        old = n
    return True


def day02(data):
    allsafe = 0
    for line in data:
        allsafe += 1 if safe_line(line) else 0
    return allsafe


assert day02(data_ex) == 2
print(day02(data))


def safe_line_almost(l, once=True):
    # print("safe line almost ", l, " once" if once else " twice")
    delta = 0
    old = l[0]
    tolerance = True
    for i, n in enumerate(l[1:]):
        if abs(n - old) > 3:
            return False
        if delta == 0:
            if n < old:
                delta = -1
            if n > old:
                delta = 1
        else:
            if n == old or (n < old and delta == 1) or (n > old and delta == -1):
                if tolerance and once and i == len(l) - 2:
                    return True
                if tolerance and once:
                    # print("tolerance : ", i, " on ", n, "  l> ", l)
                    if i == 1 and once:
                        if safe_line_almost(l[0:1] + l[2:], once=False):
                            return True
                    tolerance = False
                    n = old
                else:
                    return False
        old = n
    return True


assert safe_line_almost([1, 3, 2, 4, 5])
assert safe_line_almost([7, 8, 5, 4])
assert safe_line_almost([8, 6, 4, 4, 1])
assert safe_line_almost([1, 3, 6, 7, 9])


def day02b(data):
    allsafe = 0
    for line in data:
        l = list(map(int, line.split(" ")))
        saf = safe_line_almost(l)
        if not saf:
            print(l, " > not safe")
            # if safe_line_almost(l[1:], False):
            #    saf = True
        allsafe += 1 if saf else 0
    return allsafe


assert day02b(data_ex) == 4
print(day02b(data))


def other_safe_line(l):
    delta = 0
    old = l[0]
    for n in l[1:]:
        if abs(n - old) not in [1, 2, 3]:
            return False
        if delta == 0:
            if n < old:
                delta = -1
            if n > old:
                delta = 1
        else:
            if (n < old and delta == 1) or (n > old and delta == -1):
                return False
        old = n
    return True


def day02c(data):
    allsafe = 0
    for line in data:
        l = list(map(int, line.split(" ")))
        print("------\n", l)
        saf = other_safe_line(l)
        if not saf:
            i = -1
            while not saf and i < len(l):
                print(l[0 : i + 1] + l[i + 2 :])
                saf = other_safe_line(l[0 : i + 1] + l[i + 2 :])
                i += 1
        allsafe += 1 if saf else 0
    return allsafe


assert day02c(data_ex) == 4
print(day02c(data))
