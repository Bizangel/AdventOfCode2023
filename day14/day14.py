from adventlib.fs import read_file_line_splitted

splitted = read_file_line_splitted("day14/input.txt")

columns = [''.join([row[col_idx] for row in splitted]) for col_idx in range(len(splitted[0]))]
# print(columns)

def col_slide(rocks: str):
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


slided_cols = [col_slide(col) for col in columns]

reconstructed = [''.join([col[row_idx] for col in slided_cols]) for row_idx in range(len(slided_cols[0]))]

tsum = 0
# Now just count result
for row_idx in range(len(reconstructed)):
    for rock in reconstructed[row_idx]:
        if rock == 'O':
            tsum += len(reconstructed) - row_idx

print(tsum)