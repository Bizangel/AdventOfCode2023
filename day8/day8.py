from adventlib.fs import read_file_line_splitted
from functools import cmp_to_key as key_compare
from itertools import cycle

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



current = 'AAA'
dir_generator = cycle(directions)
steps = 0
while current != 'ZZZ':
    dir = next(dir_generator)

    current = stepmap[current][0 if dir == 'L' else 1]
    steps += 1

print(steps)





