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

def process_card(card: str):
    win_ns, have = card_numbers(card)
    win_ns = set(win_ns)

    winning_count = len([x for x in have if x in win_ns])
    if winning_count == 0:
        return 0

    winning_count -= 1
    pts = 2**winning_count
    return pts


tsum = 0
for card in splitted_cards:
    tsum += process_card(card)

print(tsum)
