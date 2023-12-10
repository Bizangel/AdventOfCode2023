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
    print(directions)
    tuples = [dir2tuple[x] for x in directions]

    adjacents = [(curr[0] + tup[0], curr[1] + tup[1]) for tup in tuples]
    adjacents = [x for x in adjacents if is_within_bounds(x) and x not in visited]
    return adjacents

def get_adjacents_bfs_nonpipe(curr, visited: set[tuple[int,int]]):
    directions = ['up','down','left','right']
    tuples = [dir2tuple[x] for x in directions]

    adjacents = [(curr[0] + tup[0], curr[1] + tup[1]) for tup in tuples]
    adjacents = [x for x in adjacents if is_within_bounds(x) and x not in visited]
    adjacents = [x for x in adjacents if gridtile[x[0]][x[1]] == '.']
    return adjacents

def bfs(start: tuple[int,int]):
    visited = set([])
    que: Queue[tuple[int,int]]= Queue()
    que.put(start) # dist 0

    while not que.empty():
        curr = que.get()

        if curr in visited:
            continue

        visited.add(curr)

        # find nearby nodes
        nodes = get_adjacents_bfs_nonpipe(curr, visited)

        for node in nodes:
            que.put(node)


    return visited

tup2dir = {
    (-1,0): 'up',
    (0,-1): 'left',
    (0,1): 'right',
    (1,0): 'down'
}

# rotate90dir = {
#     'right': 'down',
#     'down': 'left',
#     'left': 'up',
#     'up': 'right'
# }

rotate90dir = {
    'down': 'right',
    'right': 'up',
    'up': 'left',
    'left': 'down'
}




def identify_loop_inside_tiles(start_tile: tuple[int,int], start_tile_pipe: str):

    visited = set([])

    inside_initial_tiles = set()

    curr = start_tile
    previous_tile = curr

    while True:
        print("===========")
        print(curr)
        visited.add(curr)

        pipe_type = gridtile[curr[0]][curr[1]]
        if pipe_type == 'S': pipe_type = start_tile_pipe

        # find nearby nodes
        nodes = get_adjacents(curr, pipe_type, visited)

        if pipe_type == '|' or pipe_type == '-':
            # get delta

            delta = tup2dir[(curr[0] - previous_tile[0], curr[1] -  previous_tile[1])] # type: ignore
            print(delta)
            adjacent_dir = rotate90dir[delta]

            dir_tup = dir2tuple[adjacent_dir]
            inside_tile = (curr[0] + dir_tup[0], curr[1] + dir_tup[1])
            if is_within_bounds(inside_tile) and gridtile[inside_tile[0]][inside_tile[1]] == '.':
                inside_initial_tiles.add(inside_tile)

        assert len(nodes) <= 1 or (curr == start_tile), 'More than one option when transversing'
        if (len(nodes) == 0):
            break

        previous_tile = curr
        curr = nodes[0]


    # for i in range(len(gridtile)):
    #     for j in range(len(gridtile[0])):
    #         if (i,j) in visited:
    #             print("X",end='')
    #         elif (i,j) in inside_initial_tiles:
    #             print("I", end='')
    #         else:
    #             print(".",end='')

    #     print("")


    return visited, inside_initial_tiles


def find_start_pos():
    for i in range(len(gridtile)):
        for j in range(len(gridtile[0])):
            if gridtile[i][j] == 'S':
                return (i,j)


start_pos = find_start_pos()
if start_pos is None:
    raise ValueError("not found start")

loop_tiles, init_inside_tiles = list(identify_loop_inside_tiles(start_pos, 'F'))


all_tiles = set()
# bfs for each tile.
for tile in init_inside_tiles:
    all_tiles = all_tiles.union(bfs(tile))

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




