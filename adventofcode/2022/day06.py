import utils, sys, re
import functools

data_ex="mjqjpqmgbljsphdztnvjfqwrcgsmlb"
data = utils.readfile("data/d6.txt")[0]
print(data_ex)

def d06(data, n=14):
    seq = []
    for i, c in enumerate(data):
        if len(seq)==n:
            seq.pop(0)
        seq.append(c)
        if len(seq)==n and len(set(seq)) == n:
            print("".join(seq), i+1)
            return i+1
            
assert d06(data_ex, 4) == 7
assert d06("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
assert d06("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
assert d06("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10
assert d06("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11

d06(data, 4)

assert d06(data_ex) == 19
assert d06("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
assert d06("nppdvjthqldpwncqszvftbrmjlhg") == 23
assert d06("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29
assert d06("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26

d06(data)

