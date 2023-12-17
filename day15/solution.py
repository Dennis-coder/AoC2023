from functools import cache


def parse(file_name):
    with open(file_name, "r") as file:
        data = file.read().split(",")
    return data

@cache
def calc_val(str):
        val = 0
        for char in str:
            val = ((val + ord(char))*17) % 256
        return val

def part1(data):
    return sum([calc_val(step) for step in data])

def part2(data):
    boxes = [([], []) for _ in range(256)]
    for line in data:
        if line[-1] == "-":
            label = line[:-1]
            labels, focals  = boxes[calc_val(label)]
            if label in labels:
                i = labels.index(label)
                labels.pop(i)
                focals.pop(i)
        if line[-2] == "=":
            label = line[:-2]
            focal = int(line[-1])
            labels, focals = boxes[calc_val(label)]
            if label in labels:
                i = labels.index(label)
                focals[i] = focal
            else:
                labels.append(label)
                focals.append(focal)
    return sum([
        (i+1) * (j+1) * focal
        for i, (_, focals) in enumerate(boxes)
        for j, focal in enumerate(focals)
    ])
