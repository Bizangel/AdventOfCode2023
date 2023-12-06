from adventlib.fs import read_file_line_splitted

splitted = read_file_line_splitted("day6/input.txt")

# time = 71530
# dist = 940200

race_time =  51699878
race_distance = 377117112241505

def calc_possibilities(time, distance):
    tsum = 0
    for i in range(time):
        moved = i * (time - i)
        if moved > distance:
            tsum += 1
    return tsum

print(calc_possibilities(race_time, race_distance))

# tprod = 1
# for i in range(len(race_times)):
#     tprod *= calc_possibilities(race_times[i], race_distances[i])

# print(tprod)