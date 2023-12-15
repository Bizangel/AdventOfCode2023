from adventlib.fs import read_file_line_splitted

def indexof( array, elem):
    try:
        return array.index(elem)
    except ValueError:
        return -1

splitted = read_file_line_splitted("day15/input.txt")


strings = splitted[0].split(',')
# columns = [''.join([row[col_idx] for row in splitted]) for col_idx in range(len(splitted[0]))]


def HASH_STRING(string: str):
    currval = 0

    for let in string:
        currval += ord(let)
        currval *= 17
        currval %= 256

    # print(currval)
    return currval

boxes = {}

def process_string(string: str):
    if string.count('=') == 1: # add new lens
        label, focal_len = string.split('=')
        target_box = HASH_STRING(label)

        box = boxes.get(target_box, [])

        box_labels = [x[0] for x in box]
        idx_label = indexof(box_labels, label)

        if idx_label == -1: # simply add new label
            box.append((label, focal_len))
        else:
            # replace
            box[idx_label] = (label, focal_len)

        boxes[target_box] = box

    elif string.count('-') == 1:
        label, _ = string.split('-')
        target_box = HASH_STRING(label)

        box = boxes.get(target_box, [])

        box_labels = [x[0] for x in box]
        idx_label = indexof(box_labels, label)

        if idx_label == -1: # not present cannot remove
            return
        else: # just remove
            box.pop(idx_label)

# # print(strings)

for s in strings:
    # print(s)
    process_string(s)

# print(boxes)

tfocus = 0
for box in boxes:
    for i, len in enumerate(boxes.get(box, [])):
        # print(f"Len: {len[0]}: {box + 1} * {i + 1} * {len[1]} = {(box + 1) * (i + 1) * int(len[1])}")
        focus_power = (box + 1) * (i + 1) * int(len[1])
        tfocus += focus_power

print(tfocus)
