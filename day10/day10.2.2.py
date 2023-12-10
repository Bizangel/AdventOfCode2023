from adventlib.fs import read_file_line_splitted
from queue import Queue
from itertools import cycle

splitted = read_file_line_splitted("day10/input.txt")

gridtile = [[x for x in split] for split in splitted]




pipe2adjacent = { # make sure choice always comes first clockwise.
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

    adjacents = [(curr[0] + tup[0], curr[1] + tup[1]) for tup in tuples]
    adjacents = [x for x in adjacents if is_within_bounds(x) and x not in visited]
    return adjacents

def get_adjacents_bfs_nonloop(curr, visited: set[tuple[int,int]], loop_ignore: set[tuple[int,int]]):
    directions = ['up','down','left','right']
    tuples = [dir2tuple[x] for x in directions]

    adjacents = [(curr[0] + tup[0], curr[1] + tup[1]) for tup in tuples]
    adjacents = [x for x in adjacents if is_within_bounds(x) and x not in visited]
    adjacents = [x for x in adjacents if x not in loop_ignore]
    return adjacents

def bfs(start: tuple[int,int], loop_ignore: set[tuple[int,int]]):
    visited = set([])
    que: Queue[tuple[int,int]]= Queue()
    que.put(start) # dist 0

    while not que.empty():
        curr = que.get()

        if curr in visited:
            continue

        visited.add(curr)

        # find nearby nodes
        nodes = get_adjacents_bfs_nonloop(curr, visited, loop_ignore)

        for node in nodes:
            que.put(node)


    return visited

tup2dir = {
    (-1,0): 'up',
    (0,-1): 'left',
    (0,1): 'right',
    (1,0): 'down'
}

rotate90dir = {
    'right': 'down',
    'down': 'left',
    'left': 'up',
    'up': 'right'
}

rotate90dir_reverse = {
    'down': 'right',
    'right': 'up',
    'up': 'left',
    'left': 'down'
}

# rotate90dir = {
#     'down': 'right',
#     'right': 'up',
#     'up': 'left',
#     'left': 'down'
# }

def identify_inside_tiles(loop_tiles: list[tuple[int,int]], flip_dirs=False):
    if flip_dirs:
        loop_tiles = loop_tiles[::-1]

    loop_tiles_set = set(loop_tiles)

    initial_tiles = set()
    for i in range(len(loop_tiles) - 1):
        prev_tile, curr = loop_tiles[i], loop_tiles[i+1]

        delta = tup2dir[(curr[0] - prev_tile[0], curr[1] - prev_tile[1])] # type: ignore
        adjacent_dir = rotate90dir[delta]

        dir_tup = dir2tuple[adjacent_dir]
        inside_tile = (curr[0] + dir_tup[0], curr[1] + dir_tup[1])
        if is_within_bounds(inside_tile) and not inside_tile in loop_tiles_set:
            initial_tiles.add(inside_tile)

    for i in range(len(loop_tiles) - 2, -1, -1):
        prev_tile, curr = loop_tiles[i+1], loop_tiles[i]

        delta = tup2dir[(curr[0] - prev_tile[0], curr[1] - prev_tile[1])] # type: ignore
        adjacent_dir = rotate90dir_reverse[delta]

        dir_tup = dir2tuple[adjacent_dir]
        inside_tile = (curr[0] + dir_tup[0], curr[1] + dir_tup[1])
        if is_within_bounds(inside_tile) and not inside_tile in loop_tiles_set:
            initial_tiles.add(inside_tile)

    # print(initial_tiles)
    return initial_tiles

def identify_loop_tiles(start_tile: tuple[int,int], start_tile_pipe: str):

    visited = set([])
    loop_tiles = []
    curr = start_tile

    while True:
        visited.add(curr)
        loop_tiles.append(curr)

        pipe_type = gridtile[curr[0]][curr[1]]
        if pipe_type == 'S': pipe_type = start_tile_pipe

        # find nearby nodes
        nodes = get_adjacents(curr, pipe_type, visited)

        if len(nodes) == 0:
            break

        curr = nodes[0]

    return loop_tiles


def find_start_pos():
    for i in range(len(gridtile)):
        for j in range(len(gridtile[0])):
            if gridtile[i][j] == 'S':
                return (i,j)


start_pos = find_start_pos()
if start_pos is None:
    raise ValueError("not found start")




loop_tiles = identify_loop_tiles(start_pos, '-')
inside_tiles = identify_inside_tiles(loop_tiles, flip_dirs=True)

# init_inside_tiles = init_inside_tiles.union(other_init_tiles)


all_tiles = set()
# bfs for each tile.
for tile in inside_tiles:
    all_tiles = all_tiles.union(bfs(tile, set(loop_tiles)))

for i in range(len(gridtile)):
        for j in range(len(gridtile[0])):
            if (i,j) in loop_tiles:
                print("X",end='')
            elif (i,j) in all_tiles:
                print("I", end='')
            else:
                print(".",end='')

        print("")

print(len(all_tiles))




