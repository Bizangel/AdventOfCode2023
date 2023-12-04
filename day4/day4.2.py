from adventlib.fs import read_file_line_splitted


splitted_cards = read_file_line_splitted('day4/input.txt')


def card_numbers(cards: str):
    _, cardinfo = cards.split(':')
    winning_numbers, have_numbers = [x.strip() for x in cardinfo.split('|')]

    winning_numbers = [x.strip() for x in winning_numbers.split(' ') if x.strip() != '']
    have_numbers = [x.strip() for x in have_numbers.split(' ') if x.strip() != '']

    winning_numbers = [int(x) for x in winning_numbers]
    have_numbers = [int(x) for x in have_numbers]

    return winning_numbers, have_numbers

total_n_cards = len(splitted_cards)
card_amounts = [1] * total_n_cards

def process_card(card_idx: int, card: str):
    win_ns, have = card_numbers(card)

    match_count = len([x for x in have if x in win_ns])

    for i in range(card_idx+1, card_idx+match_count+1):
        if i < total_n_cards:
            card_amounts[i] += card_amounts[card_idx]




for i in range(total_n_cards):
    process_card(i,splitted_cards[i])

print(sum(card_amounts))
