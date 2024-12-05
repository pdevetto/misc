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
