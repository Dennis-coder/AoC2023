def parse(file_name):
    with open(file_name, "r") as file:
        data = file.read().splitlines()
    numbers, symbols = [], set()
    for line_nr, line in enumerate(data):
        i = 0
        while True:

            while i < len(line) and line[i] == ".": i += 1

            if i == len(line): break

            if not line[i].isdigit():
                symbols.add((line_nr, i))
                i += 1
                continue

            start = i
            while i < len(line) and line[i].isdigit(): i += 1
            numbers.append((int(line[start:i]), (line_nr, start), (line_nr, i-1)))
            
    return data, numbers, symbols

def surronding(first, last):
    line, x1 = first
    _, x2 = last

    for line_nr in range(line - 1, line + 2):
        for x in range(x1 - 1, x2 + 2):
            yield (line_nr, x)

def is_part_number(number, symbols):
    _, start, last = number
    for pos in surronding(start, last):
        if pos in symbols:
            return True
    return False

def part1(data):
    _, numbers, symbols = data
    sum = 0
    for num in numbers:
        if is_part_number(num, symbols):
            sum += num[0]
    return sum
    
def part2(data):
    raw_text, numbers, symbols = data
    sum = 0
    for (line, x) in symbols:
        if raw_text[line][x] != "*": continue

        count = 0
        val = 1
        symbol_pos = (line, x)
        for (n, start, last) in numbers:   
            for pos in surronding(start, last):
                if pos == symbol_pos:
                    count += 1
                    val *= n
                    break
            if count > 2:
                break
        if count == 2:
            sum += val

    return sum
