def parse(file_name):
    with open(file_name, "r") as file:
        data = [
            [i] + [
                set([int(x) for x in part.strip().split()])
                for part in line.split(":")[1].split("|")
            ]
            for i, line in enumerate(file.read().splitlines())
        ]
    return data

def part1(data):
    points = 0
    for i, winning, numbers in data:
        a = len(winning.intersection(numbers))
        if a == 0:
            continue
        points += 2 ** (a - 1)
    return points

def part2(data):
    nr_of_winning_numbers = [0] * len(data)
    for i, winning, numbers in data:
        nr_of_winning_numbers[i] = len(winning.intersection(numbers))
    
    scratchcards = [1] * len(data)

    for i in range(len(data)):
        for j in range(i+1, i+nr_of_winning_numbers[i]+1):
            scratchcards[j] += scratchcards[i]

    return sum(scratchcards)
