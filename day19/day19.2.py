from adventlib.fs import read_file_line_splitted
from re import split
from queue import Queue
from copy import deepcopy

splitted = read_file_line_splitted("day18/input.txt")

operators = set(['<', '>'])

def parse_workflow(wf: str):
    wf = wf[:-1] # remove }
    wf_name, wf_contents = wf.split('{')

    wf_rules = wf_contents.split(',')

    wf_splitted = [split(r'(<|>|:)', rule) for rule in wf_rules]

    return wf_name, wf_splitted

def binary_eval_operator(ele1: int, operator: str, ele2: int):
    if operator == '<':
        return ele1 < ele2
    elif operator == '>':
        return ele1 > ele2
    else:
        raise ValueError("Received operator: ", operator)

def evaluate_workflow(part: dict[str,int], workflows: dict[str, list[str]]):

    curr_workflow = 'in'
    while curr_workflow not in ['A', 'R']:

        curr_rules = workflows[curr_workflow]
        # print('rules: ', curr_rules)
        for rule in curr_rules:
            # print('checking rule: ', rule)
            # print(rule[0])
            if len(rule) == 1: # simply go there.
                curr_workflow = rule[0]
                break
            else:
                # check if rule works
                var1 = part[rule[0]]
                if binary_eval_operator(var1, rule[1], int(rule[2])):
                    # go to that workflow
                    curr_workflow = rule[-1]
                    break

    return curr_workflow

workflows = []
parts = []

is_workflow = True
for line in splitted:
    if line.strip() == "":
        is_workflow = False
        continue
    if is_workflow:
        workflows.append(line.strip())
    else:
        parts.append(line.strip())



workflows_parsed = {}
for wf in workflows:
    name, contents = parse_workflow(wf)
    workflows_parsed[name] = contents


def negate_op(op):
    if op == '<':
        return '>='
    elif op == '>':
        return '<='
    raise ValueError("Negating invalid operator: ", op)

def bfs(workflows: dict[str, list[str]]):

    que = Queue()
    que.put(('in', 0, []))

    accepted_nodes = []
    rejected_nodes = []
    while not que.empty():
        curr_node = que.get()

        # print("Node: ", curr_node)
        if curr_node[0] == 'A':
            accepted_nodes.append(curr_node)
            continue

        if curr_node[0] == 'R':
            rejected_nodes.append(curr_node)
            continue

        rule = workflows[curr_node[0]][curr_node[1]]
        if (len(rule) > 1):
            # print(rule)
            curr_rule = (rule[0], rule[1], rule[2])
            negated_rule = (rule[0], negate_op(rule[1]), rule[2])
            # split if condition is met
            que.put((rule[-1], 0, deepcopy(curr_node[2]) + [curr_rule]))
            # or if condition is NOT met
            que.put((curr_node[0], curr_node[1] + 1, deepcopy(curr_node[2]) + [negated_rule]))
        else:
            que.put((rule[0], 0, deepcopy(curr_node[2])))

    return accepted_nodes


MIN_VALUE = 1
MAX_VALUE = 4000

accepted_nodes = bfs(workflows_parsed)

accepting_rules = [x[2] for x in accepted_nodes]

def rule_to_interval(rule: tuple[str, str, str]):
    # count how many values match that rule following the operator.
    op = rule[1]
    val = int(rule[2])
    if op == '<':
        return (MIN_VALUE, val - 1)
    elif op == '<=':
        return (MIN_VALUE, val)
    elif op == '>':
        return (val + 1, MAX_VALUE)
    elif op == '>=':
        return (val, MAX_VALUE)

    return
# print(rulecount(('s', '<=', '-20')))

# IF IT DOESN'T WORK, KEEP IN MIND NON ORDERED INTERVALS / EMPTY INTERVALS

def find_overlapping_interval(intervals):
    if not intervals:
        return None

    # Sort the intervals based on their start values
    sorted_intervals = sorted(intervals, key=lambda x: x[0])

    # Initialize the result with the first interval
    result_start, result_end = sorted_intervals[0]

    # Iterate through the intervals to find the overlapping interval
    for interval_start, interval_end in sorted_intervals[1:]:
        # If there's an overlap, update the result interval
        result_end = min(result_end, interval_end)
        result_start = max(result_start, interval_start)

    return (result_start, result_end)


def interval_length(inter: tuple[int,int]):
    return inter[1] - inter[0] + 1

def prod(mylist: list[int]):
    tprod = 1
    for ele in mylist:
        tprod *= ele

    return tprod

def is_overlapping(int1,int2):
    return max(int1[0],int2[0]) <= min(int1[1],int2[1])

tsum = 0

all_intervals = []

for treeflow in accepting_rules:
    var_intervals = {}
    for rule in treeflow:
        rulelist = var_intervals.get(rule[0], [])
        rulelist.append(rule_to_interval(rule))
        var_intervals[rule[0]] = rulelist

    # print("=========================")
    # print(treeflow)

    # if any var is missing default to full range.
    for let in ['s','a','x','m']:
        if let not in var_intervals:
            var_intervals[let] = [(MIN_VALUE, MAX_VALUE)]

    # print(var_intervals)
    res = []
    for let in var_intervals:
        res.append(find_overlapping_interval(var_intervals[let]))

    # print(res)
    all_intervals.append(res)
    interval_lengths = [interval_length(x) for x in res]
    # print(interval_lengths)
    tsum += prod(interval_lengths)

print(tsum)

# for int1 in all_intervals:
#     for int2 in all_intervals:
#         if int1 != int2:
#             if all([is_overlapping(comp1, comp2) for comp1, comp2 in zip(int1, int2)]):
#                 print("Found overlapping intervals: ", int1, 'with ', int2)


# print(all_intervals)
