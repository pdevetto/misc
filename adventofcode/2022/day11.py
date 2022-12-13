import utils, sys, re, numpy
import functools
from itertools import product

def pf(k):
    [i,j] = k.split('.')
    return int(i), int(j)
def fp(i,j):
    return str(i) + '.' + str(j)

data_ex = utils.readfile("data/d11_ex.txt")
data = utils.readfile("data/d11.txt")

def evaluate(op, old):
    return eval(op.replace("old", str(old)))
    
assert evaluate("old * old", 5) == 25
assert evaluate("8 * old", 9) == 72

def d111(data):
    regexp = r"^Monkey ([0-9]+):\n"
    regexp+= r"Starting items:(.*)\n"
    regexp+= r"Operation: new = (.*)\n"
    regexp+= r"Test: divisible by (.*)\n"
    regexp+= r"If true: throw to monkey ([0-9]*)\n"
    regexp+= r"If false: throw to monkey ([0-9]*)"
    get_monkeys = re.findall(regexp, "\n".join([line.strip() for line in data]), re.MULTILINE)
    monkeys = {}
    for monkey in get_monkeys:
        mid, items, formula, test, monktrue, monkfalse = monkey
        monkeys[mid] = {
            "items": [int(item.strip()) for item in items.split(",")],
            "op": formula,
            "test": int(test),
            "throw": {"1":monktrue, "0":monkfalse}
        }
    meval = {mid:0 for mid in monkeys.keys()}
    for theround in range(0, 20):
        if theround % 10 == 0:
            print(theround)
        for mid in monkeys.keys():
            monkey = monkeys[mid]
            for worry in monkey["items"]:
                meval[mid] += 1
                new_worry = evaluate(monkey["op"], worry) // 3
                test = new_worry % monkey["test"] == 0
                throwto = monkey["throw"][str(int(test))]
                monkeys[throwto]["items"].append(new_worry)
            monkeys[mid]["items"] = []
    print([(key,monkey["items"]) for key, monkey in monkeys.items()])
    meval = sorted(meval.values())
    print(meval)
    print(numpy.prod(list(meval[-2:])))
        

d111(data_ex)
#d111(data)


def d112(data):
    regexp = r"^Monkey ([0-9]+):\n"
    regexp+= r"Starting items:(.*)\n"
    regexp+= r"Operation: new = (.*)\n"
    regexp+= r"Test: divisible by (.*)\n"
    regexp+= r"If true: throw to monkey ([0-9]*)\n"
    regexp+= r"If false: throw to monkey ([0-9]*)"
    get_monkeys = re.findall(regexp, "\n".join([line.strip() for line in data]), re.MULTILINE)
    monkeys = {}
    mitems = {}
    todivide = 1
    for monkey in get_monkeys:
        mid, items, formula, test, monktrue, monkfalse = monkey
        monkeys[mid] = {
            "op": formula,
            "test": int(test),
            "throw": {"1":monktrue, "0":monkfalse}
        }
        monkeys[mid]["plus"]=0
        monkeys[mid]["times"]=0
        add = formula.split("+")
        mul = formula.split("*")
        if len(add) == 2:
            monkeys[mid]["plus"]= int(add[1])
        elif len(mul) == 2 and mul[1].strip() != "old":
            monkeys[mid]["times"]=int(mul[1])
        todivide *= int(test)
        mitems[mid] = [int(item.strip()) for item in items.split(",")]
    meval = {mid:0 for mid in monkeys.keys()}
    for theround in range(0, 10000):
        if theround % 100 == 0:
            print(theround)
        for mid in monkeys.keys():
            monkey = monkeys[mid]
            for worry in mitems[mid]:
                meval[mid] += 1
                if monkey["plus"] != 0:
                    new_worry = worry + monkey["plus"]
                elif monkey["times"] != 0:
                    new_worry = worry * monkey["times"]
                else:
                    new_worry = worry * worry
                new_worry = new_worry % todivide
                test = new_worry % monkey["test"] == 0
                throwto = monkey["throw"][str(int(test))]
                if test :
                    mitems[throwto].append(new_worry)
                else:
                    mitems[throwto].append(new_worry)
            mitems[mid] = []
    print(mitems)
    meval = sorted(meval.values())
    print(meval)
    print(numpy.prod(list(meval[-2:])))

print(5766556 // 5468)
    
d112(data)
