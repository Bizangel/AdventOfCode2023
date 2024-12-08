from adventlib.fs import read_file_line_splitted
import numpy as np
from collections import deque

splitted = read_file_line_splitted("day18/input.txt")

dir2tuple = {
    'U': np.array((-1,0)),
    'L': np.array((0,-1)),
    'R': np.array((0,1)),
    'D': np.array((1,0))
}

dir2right = {
    'U': 'R',
    'R': 'D',
    'D': 'L',
    'L': 'U'
}

dir2arrows = {
    'U': '^',
    'L': '<',
    'R': '>',
    'D': 'v',
}

def print_grid(grid: list[list[str]]):
    for i in range(m):
        for j in range(n):
            print(grid[i][j], end='')
        print()

def move(pos: tuple[int,int], instruction: tuple[str, int, str]):
    d,l,color = instruction
    newpos = np.array(pos) + dir2tuple[d] * l
    return (newpos[0], newpos[1])

instructions = [line.split(' ') for line in splitted ]
instructions = [(x,int(y),z) for x,y,z in instructions]

rightmost = 0
bottommost = 0
leftmost = 0
topmost = 0

# find rightmost to create map
curr = (0,0)
for instruction in instructions:
    curr = move(curr, instruction)

    leftmost= min(leftmost, curr[1])
    topmost = min(topmost, curr[0])

    rightmost = max(rightmost, curr[1])
    bottommost = max(bottommost, curr[0])

start_corner = (topmost, leftmost)
# end_corner = (bottommost, rightmost)
m = (bottommost - topmost) + 1
n = (rightmost - leftmost) + 1

# repeat, now keep track of where holes are created.
grid = [['.' for _ in range(n)] for _ in range(m)]

diggedset: set[tuple[int,int]]= set()

que: deque[tuple[int,int]] = deque()

# dig outline
curr = (-topmost, -leftmost)
for instruction in instructions:
    d,l,color = instruction
    movetup = dir2tuple[d]
    inwarddir = dir2right[d]
    for _ in range(l):
        grid[curr[0]][curr[1]] = '#' # mark as digged
        # grid[curr[0]][curr[1]] = dir2arrows[d] # mark as digged
        diggedset.add((curr[0], curr[1]))

        # consider inward tile for bfs dig
        inwardtile = curr + dir2tuple[inwarddir]
        que.append((inwardtile[0], inwardtile[1]))

        curr += movetup

# print_grid(grid)

def is_within_bounds(loc: tuple[int, int]):
    return (
        0 <= loc[0] < len(grid) and
    0 <= loc[1] < len(grid[0])
    )

# bfs, dig insides
while len(que) > 0:
    curr = que.pop()

    if curr in diggedset:
        continue

    grid[curr[0]][curr[1]] = '#' # dig
    diggedset.add(curr)

    neighbors = [np.array(curr) + offset for offset in dir2tuple.values()]
    neighbors = [(array[0], array[1]) for array in neighbors]
    neighbors = [x for x in neighbors if is_within_bounds(x)]
    neighbors = [x for x in neighbors if x not in diggedset]

    for neighbor in neighbors:
        que.append(neighbor)

# count digged
res = 0
for i in range(m):
    for j in range(n):
        if grid[i][j] == '#':
            res += 1

print(res)






