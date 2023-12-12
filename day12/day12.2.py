from adventlib.fs import read_file_line_splitted
from itertools import product
import re

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

def identify_group(line, identify_position: int):
    group_id = 0
    for i in range(len(line)):
        if i == identify_position:
            return group_id

        if line[i] != line[identify_position]:
            group_id += 1


    return group_id

def adjacent_marks_or_hashes(line, pos):
    marks = []
    for i in range(pos + 1, len(line)):
        if line[i] == '?' or line[i] == '#':
            marks.append(i)
        else:
            break
    return marks

def rec(line: str, count: list[int]):

    # perform fat processing
    # try and infer from line
    hashgroup_idx = 0
    hashgrouplen = 0

    # print("===========================================================")
    # print(f"Rec input: {line} | {count}")
    i = 0
    while i < len(line):

        if line[i] == '?':
            break # no more processing as we don't know.

        # print(f"Currently on: {i} and {line[i]}")
        # print("Line as processed: ", line)
        # print("=-=-")
        if (i < len(line) - 1 and line[i] == '#' and line[i + 1] != '#') or (line[i] == '#' and i == len(line) - 1):
            hashgrouplen += 1

            # print(f"------- Identified Hashgroup: {hashgroup_idx}")
            # print(f"Length:  {hashgrouplen}")
            # print('-----------')

            if hashgroup_idx >= len(count): # generated more hashgroups than expected!
                return 0

            # check hashgroup
            if count[hashgroup_idx] == hashgrouplen: # we're done!
                # next string MUST be dot. suppose as such.
                if i < len(line) - 1 and line[i+1] == '?':
                    line = ''.join([line[j] if j != i+1 else '.' for j in range(len(line))])

            if hashgrouplen > count[hashgroup_idx]: # generated hashgroup with more hashes than expected
                return 0 # not really a possibility!


            if hashgrouplen < count[hashgroup_idx]:
                # see if able to recoup from next ?
                adj_marks = adjacent_marks_or_hashes(line, i)

                if len(adj_marks) >= count[hashgroup_idx] - hashgrouplen: # can recoup
                    # take only as many as you need
                    adj_marks = adj_marks[:count[hashgroup_idx] - hashgrouplen]
                    line = ''.join([line[j] if j not in adj_marks else '#' for j in range(len(line))])
                    i += len(adj_marks)
                    hashgrouplen += len(adj_marks) - 1 # -1 as the last hash will be added on next loop
                    continue;
                else:
                    # not enough adjacent marks, this was never a possibility, stop.
                    return 0



            hashgroup_idx += 1
            hashgrouplen = 0

        elif line[i] == '#':
            hashgrouplen += 1

        i += 1


    # print("----------> Processed: ", line)
    qmark_pos = line.find('?')
    if qmark_pos == -1:
        return 1 if string_match(line, count) else 0

    broken = rec(line.replace('?', '#', 1), count)
    good = rec(line.replace('?', '.', 1), count)

    return broken + good

# def solve(line: str, expected_count: list[int]):
#     # possibilities = all_possibilities(line)
#     print(rec(line, expected_count))

#     return





# expand
springlines = [line + '?' + line + '?' + line + '?' + line + '?' + line for line in springlines]
springcounts = [count * 5 for count in springcounts]



# print(rec('?#?#?#?#?#?#?#?', [1,3,1,6]))



tsum = 0
for i in range(len(springlines)):
    print('i: ', i)
    unknownsprings, springcount = springlines[i], springcounts[i]
    res =  rec(unknownsprings, springcount)

    tsum += res

print(tsum)



