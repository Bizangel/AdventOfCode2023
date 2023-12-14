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


patterns.append(pat)

def stringdiffcount(str1: str, str2: str):
    return len([i for i in range(len(str1)) if str1[i] != str2[i]])

def find_row_differs(comparelist):
    inbound = lambda x: x >= 0 and x < len(comparelist)

    differs_by_one_line = []
    for center in range(1, len(comparelist)):

        # print("Centering: ", center)
        left = center - 1
        right = center


        # is_mirror = 1
        differs_indexes = []
        while inbound(left) and inbound(right):
            # print("checking: ", list_hashes[left], 'and ', list_hashes[right])

            # check that they're equal
            if comparelist[left] != comparelist[right]:
                differs_indexes.append((left, right))

            left -= 1
            right += 1

        if len(differs_indexes) == 1:
            differs_by_one_line.append((center, differs_indexes[0]))

    # those that differ by one, check which one only differs by a single character
    differs_by_one = [x for x in differs_by_one_line if stringdiffcount(comparelist[x[1][0]], comparelist[x[1][1]]) == 1]
    if len(differs_by_one) > 1:
        raise ValueError("Found more than 2 fixes for mirror")

    return differs_by_one[0][0] if len(differs_by_one) == 1 else None # return center


def solve_pattern(pat: list[str]):
    cols = [''.join([row[col_idx] for row in pat]) for col_idx in range(len(pat[0]))]
    rows = pat

    horizontal_mirror = find_row_differs(rows)
    vertical_mirror = find_row_differs(cols)

    columns_to_left = 0
    if vertical_mirror is not None:
        columns_to_left = vertical_mirror

    rows_above = 0
    if horizontal_mirror is not None:
        rows_above = horizontal_mirror

    return columns_to_left, rows_above

results = [solve_pattern(pat) for pat in patterns]

for i in range(len(results)):
    res = results[i]
    assert(res[0] != 0 or res[1] != 0), f'No pattern founds on pattern:\n{'\n'.join(patterns[i])}'

leftres = sum([x[0] for x in results])
rightres = sum([x[1] for x in results])

print(leftres + 100*rightres)
