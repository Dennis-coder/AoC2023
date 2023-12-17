def parse(file_name):
    with open(file_name, "r") as file:
        data = []
        for line in file.readlines():
            game, cubes_sets = line.strip().split(": ")
            game = int(game[5:])
            parsed_sets = []
            for cubes_set in cubes_sets.split("; "):
                parsed_set = [0,0,0]
                for cubes in cubes_set.split(", "):
                    amount, color = cubes.split(" ")
                    i = 0 if color == "red" else 1 if color == "green" else 2
                    parsed_set[i] = int(amount)
                parsed_sets.append(parsed_set)
            data.append((game, parsed_sets))
    return data

def part1(data):
    sum = 0
    for game_id, revealed_sets in data:
        valid = True
        for revealed_set in revealed_sets:
            if revealed_set[0] > 12 or revealed_set[1] > 13 or revealed_set[2] > 14:
                valid = False
                break
        sum += game_id * valid
    return sum

def part2(data):
    sum = 0
    for game_id, revealed_sets in data:
        lowest_amount = [0,0,0]
        for revealed_set in revealed_sets:
            for i in range(3):
                lowest_amount[i] = max(lowest_amount[i], revealed_set[i])
        sum += lowest_amount[0] * lowest_amount[1] * lowest_amount[2]
    return sum
