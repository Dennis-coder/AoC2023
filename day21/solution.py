from queue import Queue


def parse(file_name):
    with open(file_name, "r") as file:
        garden = file.read().splitlines()
    start = [
        (x, y)
        for y, row in enumerate(garden)
        for x, plot in enumerate(row)
        if plot == "S"
    ][0]
    return garden, start

def moves(x, y):
    yield (x,y-1)
    yield (x+1,y)
    yield (x,y+1)
    yield (x-1,y)

def bfs(garden, start, max_steps):
    total_steps = [0,0]
    visited = set()
    bfs = Queue()
    bfs.put((start,0))
    while not bfs.empty():
        (x,y), steps = bfs.get()

        if (x,y) in visited or garden[y % len(garden)][x % len(garden[0])] == "#" or steps > max_steps:
            continue

        visited.add((x,y))
        total_steps[steps % 2] += 1

        for move in moves(x,y):
            bfs.put((move, steps+1))

    return total_steps[max_steps % 2]

def part1(data):
    garden, start = data
    return bfs(garden, start, 64)

def part2(data):
    garden, start = data
    size = len(garden)
    goal = 26501365
    edge = size // 2

    y = [bfs(garden, start, (edge + i * size)) for i in range(3)]
    print(y)

    n = ((goal - edge) // size)
    a = (y[2] - (2 * y[1]) + y[0]) // 2
    b = y[1] - y[0] - a
    c = y[0]
    return (a * n**2) + (b * n) + c
