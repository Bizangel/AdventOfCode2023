from adventlib.fs import read_file_line_splitted
from queue import Queue

splitted = read_file_line_splitted("day10/input.txt")

gridtile = [[x for x in split] for split in splitted]




pipe2adjacent = {
    '|': ['up', 'down'],
    '-': ['left', 'right'],
    'L': ['up', 'right'],
    'J': ['up', 'left'],
    '7': ['down', 'left'],
    'F': ['right','down'],
    '.': []
}

dir2tuple = {
    'up': (-1,0),
    'left': (0,-1),
    'right': (0,1),
    'down': (1,0)
}



def is_within_bounds(loc):
    return (
        0 <= loc[0] < len(gridtile) and
    0 <= loc[1] < len(gridtile[0])
    )

def get_adjacents(curr, pipe_type, visited: set[tuple[int,int]]):
    directions = pipe2adjacent[pipe_type]
    tuples = [dir2tuple[x] for x in directions]
    # print(directions)

    adjacents = [(curr[0] + tup[0], curr[1] + tup[1]) for tup in tuples]
    adjacents = [x for x in adjacents if is_within_bounds(x) and x not in visited]
    return adjacents

def bfs(start: tuple[int,int], consider_start: str):
    distmap = [['.' for _ in range(len(gridtile[0]))] for _ in range(len(gridtile))]
    # distmap = '\n'.join([''.join(['.' for _ in range(len(gridtile[0]))]) for _ in range(len(gridtile))])

    visited = set([])
    que: Queue[tuple[tuple[int,int], int]]= Queue()
    que.put((start, 0)) # dist 0

    while not que.empty():
        curr, dist = que.get()
        # print(curr)


        if curr in visited:
            continue

        visited.add(curr)
        distmap[curr[0]][curr[1]] = str(dist)


        pipe_type = gridtile[curr[0]][curr[1]]
        if pipe_type == 'S': pipe_type = consider_start

        # find nearby nodes
        nodes = get_adjacents(curr, pipe_type, visited)
        # print("Expanded: ", nodes)
        # print("=================")
        for node in nodes:
            que.put((node, dist + 1))


    return distmap




def find_start_pos():
    for i in range(len(gridtile)):
        for j in range(len(gridtile[0])):
            if gridtile[i][j] == 'S':
                return (i,j)


start_pos = find_start_pos()
if start_pos is None:
    raise ValueError("not found start")

distmap = bfs(start_pos, '-')
print(distmap)

# get max
max_val = -1
for val in [y for x in distmap for y in x]:
    if val != '.':
        max_val = max(int(val), max_val)

print(max_val)




