from functools import cache, cmp_to_key
from queue import Queue, PriorityQueue
from heapq import heappush, heappop
import re
from copy import deepcopy
from math import *


def parse(file_name):
    with open(file_name, "r") as file:
        lr, nodes = file.read().split("\n\n")
    lr = [0 if x == "L" else 1 for x in lr]
    nodes = {
        key: val[1:-1].split(", ")
        for key, val in [
            line.split(" = ") 
            for line in nodes.splitlines()
        ]
    }
    return lr, nodes

def part1(data):
    instructions, nodes = data
    cur_node = "AAA"
    steps = 0
    while True:
        for inst in instructions:
            steps += 1
            cur_node = nodes[cur_node][inst]
            if cur_node == "ZZZ":
                return steps

def part2(data):
    instructions, nodes = data
    cur_nodes = [node for node in nodes.keys() if node[2] == "A"]
    steps = [0 for _ in cur_nodes]
    
    for i, node in enumerate(cur_nodes):
        cur_node = node
        while True:
            for inst in instructions:
                steps[i] += 1
                cur_node = nodes[cur_node][inst]
                if cur_node.endswith("Z"):
                    break
            if cur_node.endswith("Z"):
                break
    
    return lcm(*steps)
