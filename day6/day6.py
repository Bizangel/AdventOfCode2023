from adventlib.fs import read_file_line_splitted

splitted = read_file_line_splitted("day6/input.txt")

race_times = [int(x.strip()) for x in splitted[0].split(':')[1].split(' ') if x.strip() != '']
race_distances = [int(x.strip()) for x in splitted[1].split(':')[1].split(' ') if x.strip() != '']

def calc_possibilities(time, distance):
    tsum = 0
    for i in range(time):
        moved = i * (time - i)
        if moved > distance:
            tsum += 1
    return tsum

tprod = 1
for i in range(len(race_times)):
    tprod *= calc_possibilities(race_times[i], race_distances[i])

print(tprod)