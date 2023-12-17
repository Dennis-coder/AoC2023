def parse(file_name):
    with open(file_name, "r") as file:
        data = file.read().splitlines()
    
    empty_rows = []
    for i, row in enumerate(data):
        if sum([1 for char in row if char == "#"]) == 0:
            empty_rows.append(i)

    empty_cols = []
    for col in range(len(data[0])):
        if sum([1 for row in range(len(data)) if data[row][col] == "#"]) == 0:
            empty_cols.append(col)

    galaxies = [(row, col) for row in range(len(data)) for col in range(len(data[0])) if data[row][col] == "#"]

    return galaxies, empty_rows, empty_cols

def part1(data):
    galaxies, empty_rows, empty_cols = data

    total_dist = 0
    for i, (r1, c1) in enumerate(galaxies):
        for (r2, c2) in galaxies[i+1:]:
            total_dist += abs(r2-r1) + abs(c2-c1)

            for empty_col in empty_cols:
                if c1 < empty_col < c2 or c2 < empty_col < c1:
                    total_dist += 1
            for empty_row in empty_rows:
                if r1 < empty_row < r2:
                    total_dist += 1
    
    return total_dist

def part2(data):
    galaxies, empty_rows, empty_cols = data

    total_dist = 0
    for i, (r1, c1) in enumerate(galaxies):
        for (r2, c2) in galaxies[i+1:]:
            total_dist += abs(r2-r1) + abs(c2-c1)
            
            for empty_col in empty_cols:
                if c1 < empty_col < c2 or c2 < empty_col < c1:
                    total_dist += 999999
            for empty_row in empty_rows:
                if r1 < empty_row < r2:
                    total_dist += 999999
    
    return total_dist
