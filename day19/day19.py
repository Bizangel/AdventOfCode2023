from adventlib.fs import read_file_line_splitted
from re import split

splitted = read_file_line_splitted("day19/input.txt")

operators = set(['<', '>'])

def parse_workflow(wf: str):
    wf = wf[:-1] # remove }
    wf_name, wf_contents = wf.split('{')

    wf_rules = wf_contents.split(',')

    wf_splitted = [split(r'(<|>|:)', rule) for rule in wf_rules]

    return wf_name, wf_splitted

def parse_part(part: str):
    part = part[1:-1]
    vals = part.split(',')
    valpairs = [val.split('=') for val in vals]

    return {x[0]: int(x[1]) for x in valpairs}


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


parts_parsed = [parse_part(x) for x in parts]
parts_evaluated = [evaluate_workflow(part, workflows_parsed) for part in parts_parsed]

parts_accepted = [part for part, accepted in zip(parts_parsed, parts_evaluated) if accepted == 'A']

parts_ratings = [part['x'] + part['m'] + part['a'] + part['s'] for part in parts_accepted]

print(sum(parts_ratings))
