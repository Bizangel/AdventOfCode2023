from adventlib.fs import read_file_line_splitted
from copy import deepcopy
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

# print(mapranges)

def container_image(to_predict_range, rangemapping_input):
    rmapping = {}

    # chop ranges so that they are within expected to_predict_range.
    for rang in rangemapping_input:
        if (to_predict_range[1] < rang[0] or rang[1] < to_predict_range[0]): # no overlap
            continue

        if to_predict_range[0] <= rang[0] and to_predict_range[1] < rang[1]:
            # chop via right
            rmapping[(rang[0], to_predict_range[1])] = (rangemapping_input[rang][0], rangemapping_input[rang][1] - (rang[1] - to_predict_range[1]))
        elif rang[0] < to_predict_range[0]  and rang[1] <= to_predict_range[1] :
            # chop via left
            rmapping[(to_predict_range[0], rang[1])] = (rangemapping_input[rang][0] + (to_predict_range[0] - rang[0]), rangemapping_input[rang][1])
        # range contains full to_predict
        elif rang[0] < to_predict_range[0] and to_predict_range[1] < rang[1]:
            # chop to range
            rmapping[(to_predict_range[0], to_predict_range[1])] = (
                rangemapping_input[rang][0] + (to_predict_range[0] - rang[0]),
                rangemapping_input[rang][1] - (rang[1] - to_predict_range[1]),
            )
        else:
            rmapping[rang] = rangemapping_input[rang]

    source_range_points = [y for x in rmapping.keys() for y in x if to_predict_range[0] <= y <= to_predict_range[1]]
    source_range_points.extend([to_predict_range[0],to_predict_range[1]])

    stoppoints = list(sorted(set(source_range_points)))
    stoppoints_ranges = [(stoppoints[idx], stoppoints[idx+1]) for idx in range(len(stoppoints) - 1)]


    res_ranges = []
    for rang in stoppoints_ranges:
        mapped_range = rmapping.get(rang)
        if mapped_range is not None:
            res_ranges.append(mapped_range)
        else:
            res_ranges.append(rang)

    print("Mapping: ", to_predict_range, '--->', res_ranges)
    return res_ranges

# ranges = {
#     (50, 75): (50, 75),
#     (80, 90): (80, 90),
#     (95, 105): (90, 100),
# }

initial_seeds = [int(x.strip()) for x in seedslinestrings.split(":")[1].split(" ") if x.strip() != ""]
seed_ranges = [(initial_seeds[idx], initial_seeds[idx] + initial_seeds[idx+1]) for idx in range(0, len(initial_seeds), 2)]

# Debug range mapping
# print(seed_ranges)
# for cat in mapranges:
#     print(cat, "==========")
#     for src in mapranges[cat]:
#         dst = mapranges[cat][src]
#         delta = dst[0] - src[0]
#         delta_symbol = '+' if delta > 0 else '-'
#         print(src, '--->', dst, f"({delta_symbol} {abs(delta)})")
#     print('\n')


initial_ranges = seed_ranges
print("Start range: ", initial_ranges)
current_ranges = initial_ranges
for cat in mapranges:
    print("========", cat)
    rangmap = mapranges[cat]
    current_ranges = [container_image(rang, rangmap) for rang in current_ranges]
    current_ranges = [y for x in current_ranges for y in x] # flatten

    print(current_ranges)
    # could merge, but unnecessary.

    # print(current_ranges)
print(current_ranges)
print(min([y for x in current_ranges for y in x]))





