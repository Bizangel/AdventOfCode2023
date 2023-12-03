from adventlib.fs import read_file_line_splitted

splitted = read_file_line_splitted('day3/input.txt')

grid = [[y for y in x] for x in splitted]
# splitted = [[y for y in x] for x in splitted]


# def bfs():
#     element = ""

#     return

digits = set("0123456789")
nonsymbols = set("0123456789.")

numbers = []
for line_idx in range(len(splitted)):
    line = splitted[line_idx]
    last_n = None
    is_part_number = False

    n_on_line = []
    for i in range(len(line)):
        if line[i] in digits:
            # create n
            if last_n is None:
                last_n = line[i]
            else:
                last_n += line[i]

            # check adjacency
            if i > 0:
                if grid[line_idx][i-1] not in nonsymbols: # check left
                    is_part_number = True

                if line_idx > 0 and grid[line_idx-1][i-1] not in nonsymbols: # check UP-left
                    is_part_number = True

                if line_idx < (len(grid) - 1) and grid[line_idx+1][i-1] not in nonsymbols: # check DOWN-left
                    is_part_number = True

            if i < (len(grid[0]) - 1):
                if grid[line_idx][i+1] not in nonsymbols: # check right
                    is_part_number = True

                if line_idx > 0 and grid[line_idx-1][i+1] not in nonsymbols: # check UP-right
                    is_part_number = True

                if line_idx < (len(grid) - 1) and grid[line_idx+1][i+1] not in nonsymbols: # check DOWN-right
                    is_part_number = True

            if line_idx > 0 and grid[line_idx-1][i] not in nonsymbols: # check up
                is_part_number = True

            if line_idx < (len(grid) - 1) and grid[line_idx+1][i] not in nonsymbols: # check down
                is_part_number = True


        elif line[i] not in digits and last_n is not None:
            if is_part_number:
                numbers.append(int(last_n))
                n_on_line.append(int(last_n))

            last_n = None
            is_part_number = False

    if last_n is not None and is_part_number:
        numbers.append(int(last_n))
        n_on_line.append(int(last_n))
    # print(n_on_line)



# print(numbers)
print(sum(numbers))