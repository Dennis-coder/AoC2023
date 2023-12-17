def parse(file_name):
    with open(file_name, "r") as file:
        data = file.read().splitlines()
    return data

def pprint(data, visited):
    for y in range(len(data)):
        row = ""
        for x in range(len(data[0])):
            row += "#" if \
                (x, y, 1, 0) in visited or \
                (x, y, -1, 0) in visited or \
                (x, y, 0, 1) in visited or \
                (x, y, 0, -1) in visited \
                else "."
        print(row)

def dfs(data, x, y, dx, dy):
    def out_of_bounds(x, y):
        return x < 0 or x >= len(data[0]) or y < 0 or y >= len(data)

    dfs = [(x, y, dx, dy)]
    visited = set()
    while dfs:
        key = dfs.pop()
        x, y, dx, dy = key

        if key in visited or out_of_bounds(x, y):
            continue

        visited.add((x, y, dx,dy))

        char = data[y][x]
        if char == ".":
            dfs.append((x+dx, y+dy, dx, dy))
        elif char == "-":
            dfs.append((x-1, y, -1, 0))
            dfs.append((x+1, y, 1, 0))
        elif char == "|":
            dfs.append((x, y-1, 0, -1))
            dfs.append((x, y+1, 0, 1))
        elif char == "/":
            dfs.append((x-dy, y-dx, -dy, -dx))
        elif char == "\\":
            dfs.append((x+dy, y+dx, dy, dx))
        
    return len({(x,y) for x,y,_,_ in visited})

def part1(data):
    return dfs(data, 0, 0, 1, 0)

def part2(data):
    tiles = 0
    for y in range(len(data)):
        visited = dfs(data, 0, y, 1, 0)
        tiles = max(tiles, visited)
        visited = dfs(data, len(data[0])-1, y, -1, 0)
        tiles = max(tiles, visited)

    for x in range(len(data[0])):
        visited = dfs(data, x, 0, 0, 1)
        tiles = max(tiles, visited)
        visited = dfs(data, x, len(data)-1, 0, -1)
        tiles = max(tiles, visited)
    
    return tiles

