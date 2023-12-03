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


def minimum_power_cube(game_string: str):
    shown_cubes_moves = [x.strip() for x in game_string.split(";")]

    shown_dicts = [get_color_mapping_amount(x) for x in shown_cubes_moves]

    max_per_color = {
        'red': -1, 'blue': -1, 'green': -1
    }


    for dict in shown_dicts:
        for color in max_per_color:
            max_per_color[color] = max(max_per_color[color], dict[color])

    return max_per_color['red'] * max_per_color['green'] * max_per_color['blue']

cube_powers = [ minimum_power_cube(x) for x in splitted_games]


print(sum(cube_powers))
# tsum = 0
# for i in range(len(possible_games)):
#     if possible_games[i]:
#         tsum += (i+1)
    # print(i+1, " -> ", possible_games[i])
# print(possible_games)

# print(tsum)