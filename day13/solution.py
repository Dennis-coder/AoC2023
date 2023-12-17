def parse(file_name):
    with open(file_name, "r") as file:
        data = file.read().split("\n\n")
    
    maps = []
    for map in data:
        rows = map.splitlines()
        cols = [
            "".join([
                rows[row][col]
                for row in range(len(rows))
            ]) for col in range(len(rows[0]))
        ]
        maps.append((rows, cols))
    return maps

def part1(data):
    def possible_mirror_positions(lines):
        for i in range(len(lines)-1):
            if lines[i] == lines[i+1]:
                yield i

    def is_mirror_position(lines, point):
        i = point 
        j = point+1
        while i >= 0 and j < len(lines):
            if lines[i] != lines[j]:
                return False
            i -= 1
            j += 1
        return True

    def mirror_position(rows, cols):
        for point in possible_mirror_positions(rows):
            if is_mirror_position(rows, point):
                return 100*(point+1)
        for point in possible_mirror_positions(cols):
            if is_mirror_position(cols, point):
                return point+1

    return sum([mirror_position(rows, cols) for rows, cols in data])

def part2(data):
    def calc_diff(l1, l2):
        diff = 0
        for j in range(len(l1)):
            if l1[j] != l2[j]:
                diff += 1
        return diff

    def possible_mirror_positions(lines):
        for i in range(len(lines)-1):
            diff = calc_diff(lines[i], lines[i+1])
            if diff <= 1:
                yield i

    def is_mirror_position(lines, point):
        i = point
        j = point+1
        diff = 0
        while i >= 0 and j < len(lines):
            diff += calc_diff(lines[i], lines[j])
            if diff > 1:
                return False
            i -= 1
            j += 1
        return diff == 1

    def mirror_position(rows, cols):
        for point in possible_mirror_positions(rows):
            if is_mirror_position(rows, point):
                return 100*(point+1)
        for point in possible_mirror_positions(cols):
            if is_mirror_position(cols, point):
                return point+1

    return sum([mirror_position(rows, cols) for rows, cols in data])
