def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content


def dict_plusplus(data, i, val):
    if not i in data.keys():
        data[i] = 0
    data[i] += val
    return data


def dict_append(data, i, val):
    if not i in data.keys():
        data[i] = []
    data[i].append(val)
    return data

def xy2k(x, y) -> str:
    return f"{x}.{y}"


def k2xy(k) -> tuple[int, int]:
    return tuple(map(int, k.split(".")))

def k_delta(k, delta):
    x, y = k2xy(k)
    return xy2k(x + delta[0], y + delta[1])