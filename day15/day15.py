from adventlib.fs import read_file_line_splitted

splitted = read_file_line_splitted("day15/input.txt")


strings = splitted[0].split(',')
# columns = [''.join([row[col_idx] for row in splitted]) for col_idx in range(len(splitted[0]))]


def HASH_STRING(string: str):
    currval = 0

    for let in string:
        currval += ord(let)
        currval *= 17
        currval %= 256

    # print(currval)
    return currval


# print(strings)

tsum = 0
for s in strings:
    tsum += HASH_STRING(s)

print(tsum)