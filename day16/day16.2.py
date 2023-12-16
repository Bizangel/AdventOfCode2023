from adventlib.fs import read_file_line_splitted
from queue import Queue

splitted = read_file_line_splitted("day16/input.txt")

dir2tuple = {
    'up': (-1,0),
    'left': (0,-1),
    'right': (0,1),
    'down': (1,0)
}

mirror2dir = {
    '/': { # this is RAY direction, not where it's coming
        'left': ['down'],
        'right': ['up'],
        'up': ['right'],
        'down': ['left']
    },
    '\\': {
        'left': ['up'],
        'up': ['left'],
        'down': ['right'],
        'right': ['down']
    },
    '|': {
        'left': ['up', 'down'],
        'right': ['up', 'down'],
        'up': ['up'],
        'down': ['down'],
    },
    '-': {
        'left': ['left'],
        'right': ['right'],
        'up': ['left','right'],
        'down': ['left','right'],
    },
}

mirrortiles = set(['|', '\\', '/', '-'])

def transverse(grid: list[str], start: tuple[int, int], starting_dir: str):
    print("Transversing: ", start, starting_dir)
    energized = set([])
    que: Queue[tuple[tuple[int,int], str]]= Queue()
    que.put((start, starting_dir)) # dist 0

    visited_with_dir: set[tuple[tuple[int,int], str]] = set()

    within_bounds = lambda tile: (
        (tile[0] >= 0 and tile[0] < len(grid)) and
        (tile[1] >= 0 and tile[1] < len(grid[0]))
        )

    while not que.empty():
        curr, direction = que.get()

        if (curr, direction) in visited_with_dir:
            continue

        visited_with_dir.add((curr, direction))
        energized.add(curr)

        mirrorvalue = grid[curr[0]][curr[1]]

        # print(f"Currently on: {curr}: {mirrorvalue}")
        if (mirrorvalue in mirrortiles):
            # find next directions
            next_dirs = mirror2dir[mirrorvalue][direction]
            # find next
            next_tiles = [((curr[0] + dir2tuple[d][0] , curr[1] + dir2tuple[d][1]), d) for d in next_dirs]
            # check that they are not oob
            next_tiles = [x for x in next_tiles if within_bounds(x[0])]

            for tile, dir in next_tiles:
                que.put((tile, dir))


        else:
            # keep going straight
            next_tile = (curr[0] + dir2tuple[direction][0] , curr[1] + dir2tuple[direction][1])

            if within_bounds(next_tile):
                que.put((next_tile, direction))

    return energized


cols = len(splitted[0])
rows = len(splitted)

# try atop configs
topres = [len(transverse(splitted, (0,i), 'down')) for i in range(cols)]

leftres = [len(transverse(splitted, (i,0), 'right')) for i in range(rows)]
rightres = [len(transverse(splitted, (i, cols - 1), 'left')) for i in range(rows)]

bottomres = [len(transverse(splitted, (rows-1,i), 'up')) for i in range(cols)]


all_lengths = []
all_lengths.extend(topres)
all_lengths.extend(leftres)
all_lengths.extend(rightres)
all_lengths.extend(bottomres)


print(max(all_lengths))