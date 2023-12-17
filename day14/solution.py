def parse(file_name):
    with open(file_name, "r") as file:
        data = file.read().splitlines()
    round = {(row, col) for row in range(len(data)) for col in range(len(data[0])) if data[row][col]=="O"}
    square = {(row, col) for row in range(len(data)) for col in range(len(data[0])) if data[row][col]=="#"}
    return round, square, len(data), len(data[0])

def tilt_north(round, square, rows, cols):
    new_pos = set()
    for col in range(cols):
        rocks = 0
        for row in range(rows-1, -1, -1):
            if (row, col) in round:
                rocks += 1
            elif (row, col) in square:
                for new_row in range(row+1, row+rocks+1):
                    new_pos.add((new_row, col))
                rocks = 0
        for new_row in range(0, rocks):
            new_pos.add((new_row, col))
    return new_pos

def tilt_east(round, square, rows, cols):
    new_pos = set()
    for row in range(rows):
        rocks = 0
        for col in range(cols):
            if (row, col) in round:
                rocks += 1
            elif (row, col) in square:
                for new_col in range(col-rocks, col):
                    new_pos.add((row, new_col))
                rocks = 0
        for new_col in range(cols-rocks, cols):
            new_pos.add((row, new_col))
    return new_pos

def tilt_south(round, square, rows, cols):
    new_pos = set()
    for col in range(cols):
        rocks = 0
        for row in range(rows):
            if (row, col) in round:
                rocks += 1
            elif (row, col) in square:
                for new_row in range(row-rocks, row):
                    new_pos.add((new_row, col))
                rocks = 0
        for new_row in range(rows-rocks, rows):
            new_pos.add((new_row, col))
    return new_pos

def tilt_west(round, square, rows, cols):
    new_pos = set()
    for row in range(rows):
        rocks = 0
        for col in range(cols-1, -1, -1):
            if (row, col) in round:
                rocks += 1
            elif (row, col) in square:
                for new_col in range(col+1, col+rocks+1):
                    new_pos.add((row, new_col))
                rocks = 0
        for new_col in range(0, rocks):
            new_pos.add((row, new_col))
    return new_pos

def cycle(round, square, rows, cols):
    round = tilt_north(round, square, rows, cols)
    round = tilt_west(round, square, rows, cols)
    round = tilt_south(round, square, rows, cols)
    round = tilt_east(round, square, rows, cols)
    return round

def cycles(round, square, rows, cols, n):
    prev = []
    for i in range(n):
        for j, r2 in enumerate(prev):
            if len(r2.difference(round)) == 0:
                return cycles(round, square, rows, cols, (n-i) % (i-j))
        prev.append(round)
        round = cycle(round, square, rows, cols)
    return round

def cycles2(round, square, rows, cols, n):
    for i in range(n):
        round = cycle(round, square, rows, cols)
    return round

def calc_load(round, rows):
    total_load = 0
    for (row, _) in round:
        total_load += rows-row
    return total_load

def pprint(round, rows, cols):
    for row in range(rows):
        row_str = ""
        for col in range(cols):
            row_str += "O" if (row, col) in round else "."
        print(row_str)

def part1(data):
    round, square, rows, cols = data
    round = tilt_north(round, square, rows, cols)
    return calc_load(round, rows)

def part2(data):
    round, square, rows, cols = data
    round = cycles(round, square, rows, cols, 1000000000)
    return calc_load(round, rows)
