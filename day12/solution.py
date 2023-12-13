from functools import cache, cmp_to_key
from queue import Queue, PriorityQueue
from heapq import heappush, heappop
import re
from copy import deepcopy
from math import *


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

def permutations2(record, lengths):
    count = 0
    expected = sum(lengths)
    dfs = [(record, 0, 0)]
    record_len = len(record)
    lengths_len = len(lengths)
    seen = set()
    while dfs:
        rec, length_i, rec_i = dfs.pop()
        n = rec.count("#")


        if n == expected and check_record(rec, lengths):
            count += 1
            continue

        if (rec, length_i, rec_i) in seen:
            continue

        seen.add((rec, length_i, rec_i))

        if length_i == lengths_len or n == expected or rec_i == len(rec):
            continue

        length = lengths[length_i]
        start = rec_i
        damaged_found = False
        for i in range(rec_i, record_len+1):
            if i == record_len:
                break
            char = record[i]
            if char != "#" and i - start == length:
                break
            elif char == "#" and i - start == length and rec[start] == "#":
                start = record_len
                break
            elif char == "#" and i - start == length:
                start += 1
            elif char == "#":
                damaged_found = True
            elif char == "." and damaged_found:
                start = record_len
                break
            elif char == ".":
                start = i + 1

    
        if i - start != length or start == record_len:
            continue

        dfs.append((
            rec[:rec_i] + "."*(start-rec_i) + "#"*length + "." + rec[i+1:],
            length_i+1,
            i+1
        ))

        if not rec[start] == "#":
            while start < record_len and rec[start] == "#":
                start += 1
            dfs.append((
                rec[:rec_i] + rec[rec_i:start+1].replace("?", ".") + rec[start+1:],
                length_i,
                start+1
            ))
        
    return count

def part1(data):
    sum = 0
    for (record, lengths) in data:
        sum += permutations2(record, lengths)
    return sum

def part2(data):
    sum = 0
    for i, (record, lengths) in enumerate(data):
        if record[0] == "#":
            count = permutations2(record, lengths) ** 5
        else: 
            record = "?".join([record for _ in range(5)])
            lengths = lengths * 5
            count = permutations2(record, lengths)
        sum += count
    return sum
