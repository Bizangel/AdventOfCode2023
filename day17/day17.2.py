from adventlib.fs import read_file_line_splitted
from collections import deque
import numpy as np
from queue import PriorityQueue

splitted = read_file_line_splitted("day17/input.txt")

grid = [[int(x) for x in row] for row in splitted]

dir2tuple = {
    'up': np.array((-1,0)),
    'left': np.array((0,-1)),
    'right': np.array((0,1)),
    'down': np.array((1,0))
}

dir2arrows = {
    'up': '^',
    'left': '<',
    'right': '>',
    'down': 'v',
}


splitoptions = {
    'right': ['up', 'down'],
    'left': ['up', 'down'],
    'down': ['left', 'right'],
    'up': ['left', 'right'],
}

class State:
    def __init__(self, pos: tuple[int, int], direction: str, sq_left: int):
        self.pos = pos
        self.dir = direction
        self.tiles_this_dir = sq_left

    def is_final_corner(self):
        return self.pos[0] == (len(grid) - 1) and self.pos[1] == (len(grid[0]) - 1)

    def dist_to_corner(self):
        return ((len(grid) - 1) - self.pos[0])**2 + ((len(grid[0]) - 1) - self.pos[1])**2

    def possible_actions(self):
        if self.tiles_this_dir < 4:
            possibilities = [self.dir] # must keep going straight
        elif self.tiles_this_dir < 10:
            possibilities = [self.dir] # can go straight
            possibilities.extend(splitoptions[self.dir]) # or can turn 90
        else:
            possibilities = splitoptions[self.dir][:] # must turn

        within_bounds = lambda tile: (
            (tile[0] >= 0 and tile[0] < len(grid)) and
            (tile[1] >= 0 and tile[1] < len(grid[0]))
            )

        possibilities = [direction for direction in possibilities if within_bounds(dir2tuple[direction] + np.array(self.pos))]
        return possibilities

    def move_state(self, dir: str):
        new_tiles = self.tiles_this_dir + 1 if dir == self.dir else 1
        new_pos = np.array(self.pos) + dir2tuple[dir]
        return State((new_pos[0], new_pos[1]), dir, new_tiles)

    def __str__(self) -> str:
        return f"({self.pos[0]}, {self.pos[1]}) - {self.dir} {self.tiles_this_dir} thisdir"

    def __repr__(self) -> str:
        return f"({self.pos[0]}, {self.pos[1]}) - {self.dir} {self.tiles_this_dir} thisdir"

    def __eq__(self, other: 'State'):
        return (self.pos, self.dir, self.tiles_this_dir) == (other.pos, other.dir, other.tiles_this_dir)

    def __lt__(self, other: 'State'):
        return (self.pos, self.dir, self.tiles_this_dir) < (other.pos, other.dir, other.tiles_this_dir)

    def __hash__(self) -> int:
        return (self.pos, self.dir, self.tiles_this_dir).__hash__()


bestheat: dict[State, int] = {}
que: PriorityQueue[tuple[int, State]]= PriorityQueue()

init_state1 = State((0,0), 'right', 0)
init_state2 = State((0,0), 'down', 0)

INF = 10**9+9

# Q_nodes = [State((i,j), direction, sq) for i in range(len(grid)) for j in range(len(grid[0])) for direction in dir2tuple.keys() for sq in [2,1,0]]

# for node in Q_nodes:
#     bestheat[node] = INF
#     que.put((INF,node))


bestheat[init_state1] = 0
bestheat[init_state2] = 0

prev = {}

que.put((0, init_state1))
que.put((0, init_state2))

res = INF
while not que.empty():
    heatlossthissquare, curr = que.get()

    if curr.is_final_corner():
        res = min(heatlossthissquare, res)
    neighbors = [curr.move_state(dir) for dir in curr.possible_actions()]


    # print(curr)
    for neighbor in neighbors:
        previous_best = bestheat.get(neighbor, INF)
        new_cost = bestheat[curr] + grid[neighbor.pos[0]][neighbor.pos[1]]
        if new_cost < previous_best:
            bestheat[neighbor] = new_cost
            prev[neighbor] = curr
            que.put((new_cost, neighbor))

print(
    min([bestheat.get(
    State((len(grid) - 1, len(grid[0]) - 1), direction, sq)
     , INF) for direction in dir2tuple.keys() for sq in range(4, 11)])
)


min_state = min(
        [
            State((len(grid) - 1, len(grid[0]) - 1), direction, sq) for direction in dir2tuple.keys() for sq in range(4, 11)
        ],
    key=lambda x: bestheat.get(x, INF))

# rebuild path
path = []
curr = min_state
while True:
    if curr in prev:
        path.append(prev[curr])
        curr = prev[curr]
    else:
        break

path = path[::-1]


# visualize
pathset = {state.pos: state.dir for state in path }

for i in range(len(grid)):
    for j in range(len(grid[0])):
        if (i,j) in pathset:
            print(dir2arrows[pathset[(i,j)]], end='')
        else:
            print(grid[i][j], end='')

    print()

