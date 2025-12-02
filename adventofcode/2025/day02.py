import utils
import re 

data_ex = (
    "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,"
    "1698522-1698528,446443-446449,38593856-38593862,565653-565659,"
    "824824821-824824827,2121212118-2121212124"
)
data = utils.readfile("data/d02.txt")[0]

def day02(data):
    invalid = []
    ranges = [r.split('-') for r in data.split(',')]
    for a_range in ranges:
        print("** Range ", a_range)
        start = int(a_range[0])
        if start < 10:
            start = 10
        half_A = int(str(start)[0:len(str(start))//2])
        end = int(a_range[1])
        half_Z = int(str(end)[0:len(str(end))//2])
        
        print("half", half_A, ">", half_Z)
        if half_Z < half_A: 
            half_Z = half_Z * 10
        for i in range(half_A, half_Z+1):
            n = int(str(i) + str(i))
            if n > end:
                break
            if n >= start:
                invalid.append(n)
    return sum(invalid)

assert day02("90-111") == 99
assert day02("90-190") == 99
assert day02("90-400") == 99
assert day02("81-90") == 88
assert day02("77-99") == 77+88+99
assert day02("79-98") == 88
assert day02(data_ex) == 1227775554
print("AAAA :")
#print(day02(data))

def day02b(data):
    invalid = []
    ranges = [r.split('-') for r in data.split(',')]
    for a_range in ranges:
        print("** Range ", a_range)
        start = int(a_range[0])
        len_A = len(str(start))
        end = int(a_range[1])
        len_Z = len(str(end))
        for length in range(1, len(str(end))//2+1):
            print(length)
            occurences = [i for i in range( len_A // length, len_Z // length + 1)]
            if 1 in occurences:
                occurences.remove(1)
            if 0 in occurences:
                occurences.remove(0)
            print("lenghth", length, "occur", occurences)
            part_A = int(str(start)[0:length])
            part_Z = int(str(end)[0:length])
            if len_Z - len_A >= 1:
                part_A = int(str(1)+str(0)*(length-1))
                part_Z = int(str(9)*length)
            print("test part : ", part_A, part_Z)
            for part in range(part_A, part_Z+1):
                for occur in occurences:
                    n = int(str(part) * occur)
                    if start <= n <= end:
                        invalid.append(n)
    sorted(invalid)
    print(set(invalid))

    return sum(set(invalid))


assert day02b("11-33") == 66
assert day02b("1-300") == sum([33, 66, 99, 11, 44, 77, 111, 22, 55, 88, 222])
#day02b("4000-10000")
#assert day02b("99-7777777") == 1
assert day02b("95-111") == 99+111
assert day02b(data_ex) == 4174379265
print(day02b(data))
#
# 11-22 still has two invalid IDs, 11 and 22.
# 95-115 now has two invalid IDs, 99 and 111.
# 998-1012 now has two invalid IDs, 999 and 1010.
# 1188511880-1188511890 still has one invalid ID, 1188511885.
# 222220-222224 still has one invalid ID, 222222.
# 1698522-1698528 still contains no invalid IDs.
# 446443-446449 still has one invalid ID, 446446.
# 38593856-38593862 still has one invalid ID, 38593859.
# 565653-565659 now has one invalid ID, 565656.
# 824824821-824824827 now has one invalid ID, 824824824.
# 2121212118-2121212124 now has one invalid ID, 2121212121.


