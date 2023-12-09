from adventlib.fs import read_file_line_splitted


splitted = read_file_line_splitted("day9/input.txt")


def find_value(seq: list[int]):
    sequences = [seq]
    current_seq = seq
    while any([x != 0 for x in current_seq]):
        current_seq = get_differences(current_seq)
        sequences.append(current_seq)

    sequences[len(sequences) - 1].insert(0, 0) # add 0 extrapolate
    for i in range(len(sequences) - 2, -1, -1):
        sequences[i].insert(0, sequences[i][0] - sequences[i + 1][0] )

    return sequences[0][0]


def get_differences(seq: list[int]):
    return [seq[i+1] - seq[i] for i in range(len(seq) - 1)]


initial_sequences = [[int(x.strip()) for x in stringlist.split(' ')] for stringlist in splitted]

vals = [find_value(x) for x in initial_sequences]

print(sum(vals))





