import utils, sys, re
import time, numpy, collections

data_ex= ["32T3K 765",
        "T55J5 684",
        "KK677 28",
        "KTJJT 220",
        "QQQJA 483"]
data = utils.readfile("data/d_2023_07.txt")

def hand_type(hand):
    counter = dict(collections.Counter(hand[0:5]))
    header = {5:'G', 4:'F', 1:'A'}
    max_count = max(counter.values())
    if max_count in header:
        return header[max_count]+hand
    if max_count==2:
        if len([i for i in counter.values() if i == 2]) == 2:
            return 'C'+hand
        return 'B'+hand
    if 2 in counter.values():
        return 'E'+hand
    return 'D'+hand 
    
assert hand_type('11111') == 'G11111' # FIVE
assert hand_type('11112') == 'F11112' # FOUR
assert hand_type('11122') == 'E11122' # FULL
assert hand_type('11123') == 'D11123' # THIRD
assert hand_type('11223') == 'C11223' # 2 PAIRS
assert hand_type('11234') == 'B11234' # PAIR
assert hand_type('12345') == 'A12345' # HIGH

def hand_value(hand):
    typed_hand = hand_type(hand)
    numhand = ""
    for c in hand[0:5]:
        if c in list(map(str,range(2, 10))):
            numhand += "0"+c
        else:
            numhand += {
                "T":"10",
                "J":"11",
                "Q":"12",
                "K":"13",
                "A":"14",
            }[c]
    return typed_hand[0] + numhand + typed_hand[6:]

assert hand_value('32T3K 765') == 'B0302100313 765'
assert hand_value('T55J5 684') == 'D1005051105 684'

def day07(data):
    data = list(map(hand_value,data))
    data = sorted(data)
    gain = 0
    for i, hand_valued in enumerate(data):
        gain += (i+1) * int(hand_valued[12:])
    print(gain)
    return gain

def hand_type_joker(hand):
    counter = dict(collections.Counter(hand[0:5].replace('J', '')))
    counter_j = dict(collections.Counter(hand[0:5]))
    jokers = counter_j['J'] if 'J' in counter_j else 0
    header = {5:'G', 6:'G', 7:'G', 8:'G', 9:'G', 10:'G',
             4:'F', 1:'A'}
    max_count = max(counter.values())+jokers if counter!={} else jokers
    print("max:", max_count)
    if max_count in header:
        return header[max_count]+hand
    if max_count==3:
        print(counter)
        if 2 in counter.values() and jokers == 0:
            return 'E'+hand
        if len([i for i in counter.values() if i == 2]) == 2:
            return 'E'+hand 
        return 'D'+hand
    if max_count==2:
        if len([i for i in counter.values() if i == 2]) == 2:
            return 'C'+hand
        return 'B'+hand
    
assert hand_type_joker('11111') == 'G11111' # FIVE
assert hand_type_joker('111JJ') == 'G111JJ' # FIVE
assert hand_type_joker('JJJJJ') == 'GJJJJJ' # FIVE
assert hand_type_joker('11112') == 'F11112' # FOUR
assert hand_type_joker('11JJ2') == 'F11JJ2' # FOUR
assert hand_type_joker('11122') == 'E11122' # FULL
assert hand_type_joker('11J22') == 'E11J22' # FULL
assert hand_type_joker('11123') == 'D11123' # THIRD
assert hand_type_joker('11J23') == 'D11J23' # THIRD
assert hand_type_joker('1JJ23') == 'D1JJ23' # THIRD
assert hand_type_joker('11223') == 'C11223' # 2 PAIRS
assert hand_type_joker('11234') == 'B11234' # PAIR
assert hand_type_joker('1234J') == 'B1234J' # PAIR
assert hand_type_joker('12345') == 'A12345' # HIGH


def hand_value_joker(hand):
    typed_hand = hand_type_joker(hand)
    numhand = ""
    for c in hand[0:5]:
        if c in list(map(str,range(2, 10))):
            numhand += "0"+c
        else:
            numhand += {
                "T":"10",
                "J":"00",
                "Q":"12",
                "K":"13",
                "A":"14",
            }[c]
    return typed_hand[0] + numhand + typed_hand[6:]

assert hand_value_joker('32T3K 765') == 'B0302100313 765'
assert hand_value_joker('T55J5 684') == 'F1005050005 684'

def day07_b(data):
    data = list(map(hand_value_joker,data))
    data = sorted(data)
    gain = 0
    for i, hand_valued in enumerate(data):
        gain += (i+1) * int(hand_valued[12:])
    print(gain)
    return gain
    pass

assert day07(data_ex) == 6440
start = time.time()
print("result", day07(data))
end = time.time()
print("Time : ", (end - start)*1000, " ms")

assert day07_b(data_ex) == 5905
start = time.time()
print("result", day07_b(data))
end = time.time()
print("Time : ", (end - start)*1000, " ms")
