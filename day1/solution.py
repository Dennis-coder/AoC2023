from functools import cache, cmp_to_key
from queue import Queue, PriorityQueue
from heapq import heappush, heappop
import re
from copy import deepcopy
from math import *


def parse(file_name):
    with open(file_name, "r") as file:
        data = file.readlines()
    return data

def part1(data):
    nums = []
    for line in data:
        i = 0
        while True:
            if line[i].isdigit():
                break
            i += 1
        j = len(line) - 1
        while True:
            if line[j].isdigit():
                break
            j -= 1
        nums.append(int(line[i] + line[j]))
    return sum(nums)

def part2(data):
    str_nums = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "zero": "0"}
    nums = []
    for line in data:
        i = 0
        while True:
            if line[i].isdigit() or line[i:i+3] in str_nums or line[i:i+4] in str_nums or line[i:i+5] in str_nums:
                break
            i += 1
        
        j = len(line) - 1
        while True:
            if line[j].isdigit() or line[j:j+3] in str_nums or line[j:j+4] in str_nums or line[j:j+5] in str_nums:
                break
            j -= 1
        
        num_str = ""
        if line[i].isdigit():
            num_str += line[i]
        elif line[i:i+3] in str_nums:
            num_str += str_nums[line[i:i+3]]
        elif line[i:i+4] in str_nums:
            num_str += str_nums[line[i:i+4]]
        elif line[i:i+5] in str_nums:
            num_str += str_nums[line[i:i+5]]
        
        if line[j].isdigit():
            num_str += line[j]
        elif line[j:j+3] in str_nums:
            num_str += str_nums[line[j:j+3]]
        elif line[j:j+4] in str_nums:
            num_str += str_nums[line[j:j+4]]
        elif line[j:j+5] in str_nums:
            num_str += str_nums[line[j:j+5]]

        nums.append(int(num_str))
    return sum(nums)

def main():
    data = parse('input.txt')
    print(part1(data))
    print()
    print(part2(data))

if __name__ == "__main__":
    main()