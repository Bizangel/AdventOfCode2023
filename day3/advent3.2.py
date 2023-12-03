from adventlib.fs import read_file_line_splitted

splitted = read_file_line_splitted('day3/input.txt')

grid = [[y for y in x] for x in splitted]

digits = set("0123456789")
nonsymbols = set("0123456789.")

numbers = []

gear2numbers = {

}


for line_idx in range(len(splitted)):
    line = splitted[line_idx]

    visited = set()
    for i in range(len(line)):
        if line[i] == '*':
            gear_pos = (line_idx, i)
            # print("--------------------")
            # print("Found gear *: ", (line_idx, i))
            # gear loc.

            def check(x: int,y: int):
                within_bounds = (
                    (x >= 0) and (x < len(grid))) and (
                    (y >= 0) and (y < len(line))
                )

                if not within_bounds:
                    return

                if (x,y) not in visited and grid[x][y] in digits:

                    # print("checking: ", grid[x][y])
                    # find leftmost
                    curr_pos = (x,y)
                    while curr_pos[1] > 0 and grid[curr_pos[0]][curr_pos[1] - 1] in digits:
                        curr_pos = (curr_pos[0], curr_pos[1] - 1)

                    number = ""
                    # now go right building number.
                    while curr_pos[1] < len(line) and grid[curr_pos[0]][curr_pos[1]] in digits:
                        number += grid[curr_pos[0]][curr_pos[1]]
                        visited.add((curr_pos[0], curr_pos[1]))

                        curr_pos = (curr_pos[0], curr_pos[1] + 1)

                    # associate number
                    nums = gear2numbers.get(gear_pos,[])
                    nums.append(int(number))
                    gear2numbers[gear_pos] = nums
                    # print(number)
                    # print(visited)
                    # print(gear2numbers)


            # check adjacency
            # check left
            check(line_idx - 1, i - 1)
            check(line_idx, i - 1)
            check(line_idx + 1, i - 1)

            # check right
            check(line_idx - 1, i + 1)
            check(line_idx, i + 1)
            check(line_idx + 1, i + 1)

            # up and down
            check(line_idx - 1, i)
            check(line_idx + 1, i)

            # clear visited per gear
            visited.clear()

# print(gear2numbers)

tsum = 0
for gear in gear2numbers:
    if len(gear2numbers[gear]) == 2:
        tsum  += gear2numbers[gear][0] * gear2numbers[gear][1]

print(tsum)


