import utils, re
import itertools

data_ex = "2333133121414131402"
data = utils.readfile("data/day09.txt")


def get_blocks(data):
    freespace = False
    s = []
    for i, v in enumerate(data):
        index = int(i / 2)
        count = int(v)
        s += ["" if freespace else index] * count
        freespace = not freespace
    return s


assert get_blocks("123") == [0, "", "", 1, 1, 1]
assert get_blocks("2333133121414131402") == [
    0,
    0,
    "",
    "",
    "",
    1,
    1,
    1,
    "",
    "",
    "",
    2,
    "",
    "",
    "",
    3,
    3,
    3,
    "",
    4,
    4,
    "",
    5,
    5,
    5,
    5,
    "",
    6,
    6,
    6,
    6,
    "",
    7,
    7,
    7,
    "",
    8,
    8,
    8,
    8,
    9,
    9,
]


def defrag(blocks):
    headblock = []
    tailblock = []
    head_index = 0
    tail_index = len(blocks) - 1
    while head_index <= tail_index:
        if blocks[head_index] != "":
            headblock.append(blocks[head_index])
        else:
            while blocks[tail_index] == "":
                tailblock = [""] + tailblock
                tail_index -= 1
            headblock.append(blocks[tail_index])
            tailblock = [""] + tailblock
            tail_index -= 1
        head_index += 1

    return headblock + tailblock


print("0099811188827773336446555566")
print("".join(list(map(str, defrag(get_blocks("2333133121414131402"))))))
assert (
    "".join(list(map(str, defrag(get_blocks("2333133121414131402")))))
    == "0099811188827773336446555566"
)


def defrag2(blocks):
    tail_index = len(blocks) - 1
    full_head_index = 0
    while tail_index >= 0:
        current_block = blocks[tail_index]
        size = 0
        while blocks[tail_index] == current_block:
            tail_index -= 1
            size += 1
        # Find an empty spot for the block, and maintain the index from which we should start searching (i.e. everything before this index is full)
        head_index = full_head_index
        empty_spot = 0
        encountered_blank = False
        while empty_spot < size and head_index <= tail_index:
            if blocks[head_index] != "":
                empty_spot = 0
                if not encountered_blank and head_index > full_head_index:
                    full_head_index = head_index
            else:
                encountered_blank = True
                empty_spot += 1
            head_index += 1

        if empty_spot == size:
            for i in range(size):
                blocks[head_index - 1 - i] = current_block
                blocks[tail_index + 1 + i] = ""
    return blocks


print("00992111777 44 333    5555 6666     8888  ")
print("".join(list(map(str, defrag2(get_blocks("2333133121414131402"))))))
assert (
    "".join(list(map(str, defrag2(get_blocks("2333133121414131402")))))
    == "0099211177744333555566668888"
)


def day09(data, part1=True):
    blocks = get_blocks(data)
    if part1:
        defrg = defrag(blocks)
    else:
        defrg = defrag2(blocks)
    checksum = 0
    for i, v in enumerate(defrg):
        if v:
            checksum += i * v
    return checksum


assert (day09(data_ex)) == 1928
print(day09(data[0]))

assert (day09(data_ex, False)) == 2858
print(day09(data[0], False))
