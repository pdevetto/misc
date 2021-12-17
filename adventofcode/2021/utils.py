def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content