from adventlib.fs import read_file_line_splitted
from itertools import product

def all_possibilities(string):
    count = string.count('?')
    possibilities = list(product('.#', repeat=count))
    result = []

    for possibility in possibilities:
        replaced = iter(possibility)
        result.append(''.join(char if char != '?' else next(replaced) for char in string))

    return result

splitted = read_file_line_splitted("day12/input.txt")

springlines = [x.split(' ')[0] for x in splitted]
springcounts = [x.split(' ')[1] for x in splitted]

# make springcounts integerish
springcounts = [[int(i) for i in x.split(',')] for x in springcounts]

def string_match(string: str, count: list[int]):
    splits = string.split('.')
    # remove empty splits
    splits = [x for x in splits if x != '']

    # check that len matches expected
    if len(splits) != len(count):
        return False

    # if it matches, check that each segment length matches

    return all([len(splits[i]) == count[i] for i in range(len(count))])


def get_match_count(line: str, expected_count: list[int]):
    possibilities = all_possibilities(line)

    # matched = []
    matchcount = 0
    for possibility in possibilities:
        if string_match(possibility, expected_count):
            matchcount += 1


    return matchcount

    # check for each possibility if it matches.



# get_match_count('???.###', [1,1,3])

tsum = 0
for i in range(len(springlines)):
    print("i: ", i)
    unknownsprings, springcount = springlines[i], springcounts[i]
    tsum += get_match_count(unknownsprings, springcount)

print(tsum)

