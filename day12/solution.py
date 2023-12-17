def parse(file_name):
    with open(file_name, "r") as file:
        records = []
        for line in file.read().splitlines():
            record, lengths = line.split()
            lengths = [int(x) for x in lengths.split(",")]
            records.append((record, lengths))
    return records

def get_groups(record):
    groups = []
    group = 0
    for char in record:
        if char == "#":
            group += 1
            continue
        if group:
            groups.append(group)
            group = 0
    if group:
        groups.append(group)
    return groups


def check_record(record, lengths):
    groups = get_groups(record)
    if len(groups) != len(lengths):
        return False
    for (group, length) in zip(groups, lengths):
        if group != length:
            return False
    return True

def permutations(record, lens):
    record_len = len(record)
    lens_len = len(lens)
    memo = {}
    def dp(rec_i, lens_i, cur_len):
        key = (rec_i, lens_i, cur_len)
        if key in memo:
            return memo[key]
        if rec_i == record_len:
            if lens_i == lens_len and cur_len == 0:
                return 1
            if lens_i == lens_len - 1 and cur_len == lens[-1]:
                return 1
            return 0
        
        count = 0
        char = record[rec_i]
        if char != "#" and cur_len == 0:
            count += dp(rec_i+1, lens_i, 0)
        if char != "#" and lens_i < lens_len and cur_len == lens[lens_i]:
            count += dp(rec_i+1, lens_i+1, 0)
        if char != ".":
            count += dp(rec_i+1, lens_i, cur_len+1)
        memo[key] = count
        return count
    
    dp(0,0,0)
    return memo[(0,0,0)]

def part1(data):
    sum = 0
    for record, lengths in data:
        sum += permutations(record, lengths)
    return sum

def part2(data):
    sum = 0
    for record, lengths in data:
        record = "?".join([record for _ in range(5)])
        lengths = lengths * 5
        sum += permutations(record, lengths)
    return sum
