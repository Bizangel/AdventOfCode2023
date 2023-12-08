from adventlib.fs import read_file_line_splitted
from functools import cmp_to_key as key_compare


splitted = read_file_line_splitted("day7/input.txt")

cardvals = 'AKQJT98765432'

card2strength = {
    cardvals[i] : len(cardvals) - i for i in range(len(cardvals))
}

type2strength = {
    'five': 7,
    'four': 6,
    'full_house': 5,
    'three': 4,
    'two_pairs': 3,
    'one_pair': 2,
    'distinct': 1,
}

def card_type(card: str):
    card_counts = {}
    for let in card:
        card_counts[let] = card_counts.get(let, 0) + 1

    amounts = list(sorted(card_counts.values(), reverse=True))

    if amounts[0] == 5:
        return 'five'

    if amounts[0] == 4:
        return 'four'

    if amounts[0] == 3 and amounts[1] == 2:
        return 'full_house'

    if amounts[0] == 3:
        return 'three'

    if amounts[0] == 2 and amounts[1] == 2:
        return 'two_pairs'

    if amounts[0] == 2:
        return 'one_pair'

    return 'distinct'


def card_value(card: str):
    return (type2strength[card_type(card)], *([card2strength[x] for x in card]))

cards = [(x.split(" ")[0], int(x.split(" ")[1])) for x in splitted]

weakest_first = sorted(cards, key=lambda x: card_value(x[0]))

ranksum = 0
for i in range(len(weakest_first)):
    ranksum += (weakest_first[i][1] * (i + 1))

print(ranksum)

