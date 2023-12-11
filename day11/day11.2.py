from adventlib.fs import read_file_line_splitted
from queue import Queue
from itertools import combinations

EXPANDED_DISTANCE = 1000000

def print_galaxy(galmap):
    for galmaprow in galmap:
        for x in galmaprow:
            print(x, end='')
        print('')

splitted = read_file_line_splitted("day11/input.txt")

galaxymap = [[y for y in x] for x in splitted]


expanded_rows = set([i for i in range(len(galaxymap)) if all([x == '.' for x in galaxymap[i]])])
expanded_cols = set([col for col in range(len(galaxymap[0]))
                  if all([galaxymap[i][col] == '.' for i in range(len(galaxymap)) ])])


galaxy_locations = []
for i in range(len(galaxymap)):
    for j in range(len(galaxymap[0])):
        if galaxymap[i][j] == '#':
            galaxy_locations.append((i,j))



dir2tuple = {
    'up': (-1,0),
    'left': (0,-1),
    'right': (0,1),
    'down': (1,0)
}

def is_within_bounds(loc):
    return (
        0 <= loc[0] < len(galaxymap) and
    0 <= loc[1] < len(galaxymap[0])
    )


def get_adjacents(curr, visited: set[tuple[int,int]]):
    directions = ['up','down','left','right'] # consider all 4 directions.
    tuples = [dir2tuple[x] for x in directions]

    adjacents = [(curr[0] + tup[0], curr[1] + tup[1]) for tup in tuples]
    adjacents = [x for x in adjacents if is_within_bounds(x) and x not in visited]

    return adjacents

def distance_to_other_galaxies(start):
    # find the total sum of distances to all other galaxies via bfs.

    distance_to = {}
    # total_dist_sum = 0

    visited = set([])
    que: Queue[tuple[tuple[int,int], int]]= Queue()
    que.put((start, 0)) # dist 0

    while not que.empty():
        curr, dist = que.get()

        if curr in visited:
            continue

        visited.add(curr)

        if curr != start and galaxymap[curr[0]][curr[1]] == '#':
            # another galaxy
            distance_to[curr] = dist
            # total_dist_sum += dist

        # find nearby nodes
        nodes = get_adjacents(curr, visited)

        for node in nodes:
            if (node[0] in expanded_rows) or node[1] in expanded_cols:
                que.put((node, dist + EXPANDED_DISTANCE))
            else:
                que.put((node, dist + 1))

    return distance_to


galaxy_dist_map = {}


print("Number of galaxies: ", len(galaxy_locations))

for i, galaxy in enumerate(galaxy_locations):
    print("Galaxy:", i)
    galaxy_dist_map[galaxy] = distance_to_other_galaxies(galaxy)

total_sum = 0
for comb in combinations(galaxy_locations, 2):
    g1, g2 = comb
    total_sum += galaxy_dist_map[g1][g2]

print(total_sum)

