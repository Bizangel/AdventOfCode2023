with open('day2/input.txt','r') as fhandle:
    contents = fhandle.read()

splitted = contents.split('\n')

splitted_games = [x.split(':')[1].strip() for x in splitted]

max_cube_amounts = {
    'red': 12,
    'green': 13,
    'blue': 14,
}
def get_color_mapping_amount(cubestring: str):
    base_d = {'red' : 0, 'green' : 0, 'blue' : 0}
    cubes = [x.strip() for x in cubestring.split(',')]
    for x in cubes:
        amount, color = x.split(' ')
        base_d[color] = int(amount)

    return base_d


def is_possible(game_string: str):
    shown_cubes_moves = [x.strip() for x in game_string.split(";")]

    shown_dicts = [get_color_mapping_amount(x) for x in shown_cubes_moves]

    for dict in shown_dicts:
        for color in max_cube_amounts:
            if dict[color] > max_cube_amounts[color]:
                return False

    return True

possible_games = [ is_possible(x) for x in splitted_games]

tsum = 0
for i in range(len(possible_games)):
    if possible_games[i]:
        tsum += (i+1)
    # print(i+1, " -> ", possible_games[i])
# print(possible_games)

print(tsum)