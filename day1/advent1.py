

with open('day1/input.txt','r') as fhandle:
    contents = fhandle.read()


string2num = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight' : 8,
    'nine': 9
}

digits = "123456789"

def get_line_val(val: str):

    stringidx = {str(string2num[d]) : val.find(d) for d in string2num}
    digitidx = {d : val.find(d) for d in digits}

    def valkey(x):
        if stringidx[x] == -1:
            return digitidx[x] if digitidx[x] > -1 else float('inf')
        elif digitidx[x] == -1:
            return stringidx[x] if stringidx[x] > -1 else float('inf')

        return min(stringidx[x], digitidx[x])


    leftmostval = min(stringidx, key=valkey)

    # Redo with rightmost search
    stringidx = {str(string2num[d]) : val.rfind(d) for d in string2num}
    digitidx = {d : val.rfind(d) for d in digits}

    def valkey2(x):
        return max(stringidx[x], digitidx[x])

    rightmost = max(stringidx, key=valkey2)

    return int(leftmostval + rightmost)


splitted = contents.split('\n')

tsum = 0
for line in splitted:
    tsum += get_line_val(line)

print(tsum)