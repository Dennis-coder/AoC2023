from math import sqrt


def parse(file_name):
    with open(file_name, "r") as file:
        data = [
            line.split()[1:]
            for line in file.read().splitlines()
        ]
    return data

def part1(data):
    val = 1
    for (sec, dist) in (
        (
            int(data[0][i]), 
            int(data[1][i])
        ) 
        for i in range(len(data[0]))
    ):
        x1 = int(sec/2 - sqrt((sec/2)**2 -dist)) + 1
        val *= sec - 2 * x1 + 1
    return val

def part2(data):
    sec  = int("".join(data[0]))
    dist = int("".join(data[1]))
    x1 = int(sec/2 - sqrt((sec/2)**2 -dist)) + 1
    return sec - 2 * x1 + 1