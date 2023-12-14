from adventlib.fs import read_file_line_splitted

splitted = read_file_line_splitted("day14/input.txt")

def col_slide_up(rocks: str):
    stacked_indexes = {}

    stacked = 0
    for i in range(len(rocks) - 1, -1, -1):
        if rocks[i] == '#':
            stacked_indexes[i] = stacked
            stacked = 0
        elif rocks[i] == 'O':
            stacked += 1

    # -1 will be top layer rock so to speak
    stacked_indexes[-1] = stacked

    # reconstruct.
    rock_locs = set(stacked_indexes.keys())
    col_construct = []

    # check stacked atop rocks
    col_construct.extend(['O'] * stacked_indexes.get(-1, 0))
    i = stacked_indexes.get(-1, 0)
    while i < len(rocks):
        if i in rock_locs:
            col_construct.append("#")
            # append all stucked rocks
            col_construct.extend(['O'] * stacked_indexes[i])
            i += stacked_indexes[i] + 1
            continue
        else:
            col_construct.append(".")
        i+= 1


    return ''.join(col_construct)

def col_slide_down(rocks: str):
    stacked_indexes = {}

    stacked = 0
    for i in range(len(rocks)):
        if rocks[i] == '#':
            stacked_indexes[i] = stacked
            stacked = 0
        elif rocks[i] == 'O':
            stacked += 1

    # -1 will be top layer rock so to speak
    stacked_indexes[-1] = stacked

    # reconstruct.
    rock_locs = set(stacked_indexes.keys())
    col_construct = []

    # check stacked atop rocks
    col_construct.extend(['O'] * stacked_indexes.get(-1, 0))
    i = len(rocks) - stacked_indexes.get(-1, 0) - 1
    while i >= 0:
        if i in rock_locs:
            col_construct.append("#")
            # append all stucked rocks
            col_construct.extend(['O'] * stacked_indexes[i])
            i -= stacked_indexes[i] + 1
            continue
        else:
            col_construct.append(".")
        i -= 1


    return ''.join(col_construct[::-1])


def cycle_north(grid: list[str]):
    columns = [''.join([row[col_idx] for row in grid]) for col_idx in range(len(grid[0]))]
    slided_cols = [col_slide_up(col) for col in columns]
    return [''.join([col[row_idx] for col in slided_cols]) for row_idx in range(len(slided_cols[0]))]

def cycle_south(grid: list[str]):
    columns = [''.join([row[col_idx] for row in grid]) for col_idx in range(len(grid[0]))]
    slided_cols = [col_slide_down(col) for col in columns]
    return [''.join([col[row_idx] for col in slided_cols]) for row_idx in range(len(slided_cols[0]))]

def cycle_west(grid: list[str]):
    slided_rows = [col_slide_up(row) for row in grid]
    return slided_rows

def cycle_east(grid: list[str]):
    slided_rows = [col_slide_down(row) for row in grid]
    return slided_rows




def full_cycle(grid: list[str]):
    c1 = cycle_north(grid)
    c2 = cycle_west(c1)
    c3 = cycle_south(c2)
    c4 = cycle_east(c3)
    return c4





cycle_hashes = {}

def find_loop(grid: list[str]):
    cycle_hashes['\n'.join(grid)] = 0
    cyc = grid
    for i in range(cycles):
        cyc = full_cycle(cyc)

        stringcyc = '\n'.join(cyc)
        if stringcyc in cycle_hashes:
            return (i + 1, cycle_hashes[stringcyc])

        cycle_hashes[stringcyc] = (i + 1) # 1-based indexing

    return (-1, -1)

cycles = 1_000_000_000

loop_found, loop_start = find_loop(splitted)

start = [a[0] for a in cycle_hashes.items() if a[1] == loop_start][0]
start_splitted = start.split('\n')
loop_every = loop_found - loop_start

target_cycles = cycles - loop_start

target_cycles -= (target_cycles // loop_every) * loop_every


cyc = start_splitted
for _ in range(target_cycles):
    cyc = full_cycle(cyc)

print(cyc)

tsum = 0
# Now just count result
for row_idx in range(len(cyc)):
    for rock in cyc[row_idx]:
        if rock == 'O':
            tsum += len(cyc) - row_idx

print(tsum)
