from adventlib.fs import read_file_line_splitted
from functools import cmp_to_key as key_compare


splitted = read_file_line_splitted("day7/input.txt")

cardvals = 'AKQT98765432J'

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

    # print(card_counts)
    if card_counts.get('J') is not None:
        def max_non_J(val):
            return card_counts.get(val) if val != 'J' else -1
        # there are some jokers. modify

        highest_card = max(card_counts, key=max_non_J)
        if highest_card == 'J':
            highest_card = 'A' # default to somthing if J wins
        card_counts[highest_card] = card_counts.get(highest_card, 0) + card_counts.get('J')
        card_counts.pop('J')
        # recalc amounts
        amounts = list(sorted(card_counts.values(), reverse=True))

    # print(card_counts)
    # print("============")
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


# print(card_type('JJJJJ'))
cards = [(x.split(" ")[0], int(x.split(" ")[1])) for x in splitted]

weakest_first = sorted(cards, key=lambda x: card_value(x[0]))

ranksum = 0
for i in range(len(weakest_first)):
    ranksum += (weakest_first[i][1] * (i + 1))

print(ranksum)

