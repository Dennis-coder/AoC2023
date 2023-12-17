def parse(file_name):
    def derivatives(history):
        cur = history
        derivatives = [history]
        while True:
            derivative = []
            for i in range(1, len(cur)):
                derivative.append(cur[i] - cur[i-1])
            if all([x == 0 for x in derivative]):
                return derivatives
            derivatives.append(derivative)
            cur = derivative

    with open(file_name, "r") as file:
        data = [
            derivatives([
                int(x)
                for x in line.split()
            ])
            for line in file.read().splitlines()
        ]
    return data

def part1(data):
    sum = 0
    for derivatives in data:
        for derivative in derivatives:
            sum += derivative[-1]
    return sum 

def part2(data):
    sum = 0
    for derivatives in data:
        val = 0
        for derivative in derivatives[::-1]:
            val = derivative[0] - val
        sum += val
    return sum 
