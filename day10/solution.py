def parse(file_name):
    with open(file_name, "r") as file:
        data = file.read().splitlines()

    maze = [
        [
            1*(char in "|LJ") + 2*(char in "-LF") + 4*(char in "|F7") + 8*(char in "-7J") + 15*(char == "S")
            for char in row
        ] for row in data
    ]

    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == "S":
                return maze, (row, col)
        
def get_path(state):
    path = []
    while state != None:
        pos, _, next_state = state
        path.append(pos)
        state = next_state
    return path

def path_dfs(maze, start):
    dfs = [(start, 0, None)]
    visited = set()

    while dfs:
        state = dfs.pop()
        pos, dir, _ = state
        (row, col) = pos

        if pos == start and dir:
            return get_path(state)
        
        if pos in visited or not (0 <= row < len(maze)) or not (0 <= col < len(maze[0])):
            continue
        
        visited.add(pos)

        if row-1 >= 0 and maze[row][col] & 1 and maze[row-1][col] & 4 and dir != 3:
            dfs.append(((row-1, col), 1, state))

        if col+1 < len(maze[0]) and maze[row][col] & 2 and maze[row][col+1] & 8 and dir != 4:
            dfs.append(((row, col+1), 2, state))

        if row+1 < len(maze) and maze[row][col] & 4 and maze[row+1][col] & 1 and dir != 1:
            dfs.append(((row+1, col), 3, state))

        if col-1 >= 0 and maze[row][col] & 8 and maze[row][col-1] & 2 and dir != 2:
            dfs.append(((row, col-1), 4, state))

def tiles_dfs(start, visited, rows, cols):
    dfs = [start]

    while dfs:
        pos = dfs.pop()
        (row, col) = pos

        if pos in visited or not (0 <= row < rows) or not (0 <= col < cols):
            continue
        
        visited.add(pos)

        dfs.append((row-1, col))
        dfs.append((row, col+1))
        dfs.append((row+1, col))
        dfs.append((row, col-1))

def part1(data):
    maze, start = data
    path = path_dfs(maze, start)
    return len(path) // 2

def part2(data):
    maze, start = data
    path = path_dfs(maze, start)

    modified_path = [(start[0]*2, start[1]*2)]
    prev_pos = start
    for pos in path[1:]:
        r1, c1 = prev_pos
        r2, c2 = pos
        dr = r2 - r1
        dc = c2 - c1

        modified_path.append((r1 * 2 + dr, c1 * 2 + dc))
        modified_path.append((r2 * 2, c2 * 2))
        prev_pos = pos

    visited = set(modified_path)
    rows, cols = len(maze)*2, len(maze[0])*2
    for i in range(len(maze)*2):
        tiles_dfs((0      , i)     , visited, rows, cols)
        tiles_dfs((i      , cols-1), visited, rows, cols)
        tiles_dfs((rows-1 , i)     , visited, rows, cols)
        tiles_dfs((i      , 0)     , visited, rows, cols)
    
    enclosed = {(row // 2, col // 2) for row in range(rows) for col in range(cols) if (row, col) not in visited and row % 2 == 0 and col % 2 == 0}
    return len(enclosed)


