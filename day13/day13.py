from adventlib.fs import read_file_line_splitted

splitted = read_file_line_splitted("day13/input.txt")

patterns = []

pat = []
for line in splitted:
    if len(line.strip()) == 0:
        patterns.append(pat)
        pat = []
    else:
        pat.append(line)


# # pat.append(line)
patterns.append(pat)

def find_mirror(list_hashes):
    inbound = lambda x: x >= 0 and x < len(list_hashes)
    for center in range(1, len(list_hashes)):

        # print("Centering: ", center)
        left = center - 1
        right = center

        is_mirror = True
        while inbound(left) and inbound(right):
            # print("checking: ", list_hashes[left], 'and ', list_hashes[right])

            # check that they're equal
            if list_hashes[left] != list_hashes[right]:
                is_mirror = False
                break

            left -= 1
            right += 1

        if is_mirror:
            # print("found mirror")
            return center

def solve_pattern(pat: list[str]):
    cols = [''.join([row[col_idx] for row in pat]) for col_idx in range(len(pat[0]))]
    rows = pat

    # print(cols)

    # print(rows)
    horizontal_mirror = find_mirror(rows)
    vertical_mirror = find_mirror(cols)

    columns_to_left = 0
    if vertical_mirror is not None:
        columns_to_left = vertical_mirror

    rows_above = 0
    if horizontal_mirror is not None:
        rows_above = horizontal_mirror

    return columns_to_left, rows_above

    # print(vertical_mirror)

# print(patterns[-1])
results = [solve_pattern(pat) for pat in patterns]

# print(results)

for i in range(len(results)):
    res = results[i]
    assert(res[0] != 0 or res[1] != 0), f'No pattern founds on pattern:\n{'\n'.join(patterns[i])}'

leftres = sum([x[0] for x in results])
rightres = sum([x[1] for x in results])

print(leftres + 100*rightres)
