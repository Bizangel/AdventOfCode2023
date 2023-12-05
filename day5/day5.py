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


mapranges = {}
# parse into numbers
for mp in mapstring:
    mapranges[mp] = [[int (y) for y in x.split(" ")] for x in mapstring[mp]]


# print(mapranges)


def find_jump(n, rangelist):
    for rang in rangelist:
        dst, src, rangelen = rang
        if (src <= n) and (n < (src + rangelen)):
            return dst + (n - src)

    return n

# they're in order so yeah

def seed_location(seed_n):
    curr = seed_n
    for jump in mapranges:
        rangelist = mapranges[jump]
        curr = find_jump(curr, rangelist)

    return curr


# print(find_jump(50,mapranges['seed-to-soil']))

# print(seed_location(13))
# print(seedslinestrings)

initial_seeds = [int(x.strip()) for x in seedslinestrings.split(":")[1].split(" ") if x.strip() != ""]


locations = [seed_location(seed) for seed in initial_seeds]

print(locations)
print(min(locations))





