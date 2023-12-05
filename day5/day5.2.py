from adventlib.fs import read_file_line_splitted

splitted = read_file_line_splitted("day5/input.txt")

seedslinestrings = splitted[0]

splitted = splitted[2:]

mapstring = {}

digits = "0123456789"
last_map = None
for line in splitted:
    if len(line.strip()) == 0:
        continue

    if line[0] in digits:
        # it's a map line
        mapstring[last_map].append(line)
    else:
        last_map, _ = line.split(' ')
        mapstring[last_map] = []


mapranges_old = {}
# parse into numbers
for mp in mapstring:
    mapranges_old[mp] = [[int (y) for y in x.split(" ")] for x in mapstring[mp]]


mapranges = {}
mapreverse = {}
for category in mapranges_old:
    mapranges[category] = {}
    mapreverse[category] = {}
    for rangelist in mapranges_old[category]:
        dst, src, rangelen = rangelist
        mapranges[category][(src, src+rangelen)] = (dst, dst+rangelen)
        mapreverse[category][(dst, dst+rangelen) ] = (src, src+rangelen)


# ranges are either fully contained
# not contained
# overlap left
# overlap right.

# IF fully contained -> just predict all of them.
# IF not contained -> drop the range.
# if overlapped left. ->  predict the available ones
# same for right.

# test_range

test_range = [(50, 80)]



print(test_range)
# def jump_range():
#     return






