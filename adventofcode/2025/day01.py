import utils

data_ex = [
    "L68","L30","R48","L5","R60","L55","L1","L99","R14","L82"
]
data = utils.readfile("data/d01.txt")


def day01(data):
    N = 50
    left_zero = 0
    for seq in data:
        update = (-1 if seq[0] == 'L' else 1) * int(seq[1:])
        N = (N + update) % 100
        if N == 0:
            left_zero += 1
        print( update, N, left_zero)
    return left_zero

#assert day01(data_ex) == 3
#print(day01(data))

def day01b(data):
    N = 50
    pass_zero = 0
    for seq in data:
        update = (-1 if seq[0] == 'L' else 1) * int(seq[1:])
        if N == (-1 * update):
            passed = 1
        elif N != 0 or update > 0:
            passed = abs((N + update) // 100)
            if update < 0 and (N+update) % 100 == 0:
                passed += 1
        else: 
            passed = abs(update) // 100
        print(N, "+", update, "###", N+update, ":", passed)
        N = (N + update) % 100
        pass_zero += passed
        print("=", pass_zero, " (", N, ")")
    return pass_zero

print("-- Part B --\n\n")
assert day01b(data_ex) == 6
print("-- Part B --\n\n")
assert day01b(["R650"]) == 7
assert day01b(["R49","L699"]) == 7

print(day01b(data))
