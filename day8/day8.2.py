from adventlib.fs import read_file_line_splitted
from itertools import cycle
from math import lcm

splitted = read_file_line_splitted("day8/input.txt")

directions = splitted[0]

splitted = splitted[2:]

stepmap = {}

for instructions in splitted:
    src, dst = instructions.split("=")
    src = src.strip()
    dst = dst.strip()[1:-1] # remove parenthesis
    dst = [x.strip() for x in dst.split(',')]

    stepmap[src] = dst

def count_steps_to_end(start):
    current = start
    dir_generator = cycle(directions)
    steps = 0
    while current[-1] != 'Z':
        dir = next(dir_generator)
        current = stepmap[current][0 if dir == 'L' else 1]
        steps += 1
    return steps

all_starts = [key for key in stepmap.keys() if key[-1] == 'A' ]


vals = [count_steps_to_end(start) for start in all_starts]

print(lcm(*vals))






