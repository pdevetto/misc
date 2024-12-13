import utils, re

data_ex = utils.readfile("data/day05_ex.txt")
data = utils.readfile("data/day05.txt")


def well_ordered_list(suite, graph):
    etius = list(reversed(suite))
    for i, number in enumerate(etius):
        inter = set(etius[i + 1 :]).intersection(set(graph.get(number, [])))
        if len(inter) != 0:
            print(inter, " before ", number)
            return False
    return True


def reorder_list(suite, graph):
    new_suite = []
    while len(suite) != 0:
        numb = suite[0]
        suite = suite[1:]
        if len(set(graph.get(numb, [])).intersection(suite)) == 0:
            new_suite = [numb] + new_suite
        else:
            suite.append(numb)
    return new_suite


zegraph = {
    47: [53, 13, 61, 29],
    97: [13, 61, 47, 29, 53, 75],
    75: [29, 53, 47, 61, 13],
    61: [13, 53, 29],
    29: [13],
    53: [29, 13],
}
assert reorder_list([61, 13, 29], zegraph) == [61, 29, 13]
assert reorder_list([75, 97, 47, 61, 53], zegraph) == [97, 75, 47, 61, 53]
assert reorder_list([97, 13, 75, 29, 47], zegraph) == [97, 75, 47, 29, 13]


def day05(data):
    graph = {}
    suites = []
    for line in data:
        isrule = re.findall("([0-9]*)\|([0-9]*)", line)
        if len(isrule) == 1:
            rule = isrule[0]
            graph[int(rule[0])] = graph.get(int(rule[0]), []) + [int(rule[1])]
        else:
            suite = re.findall("([0-9]+)", line)
            if suite:
                print(suite)
                suites.append(list(map(int, suite)))

    print(graph)
    print(suites)

    sum = 0
    sum_new_ordered = 0

    for suite in suites:
        if well_ordered_list(suite, graph):
            sum += suite[len(suite) // 2]
        else:
            newsuite = reorder_list(suite, graph)
            sum_new_ordered += newsuite[len(newsuite) // 2]
    return sum, sum_new_ordered


assert day05(data_ex) == (143, 123)
print("OK")
print(day05(data))
