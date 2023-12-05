from functools import cache, cmp_to_key
from queue import Queue, PriorityQueue
from heapq import heappush, heappop
import re
from copy import deepcopy
from math import *


def parse(file_name):
    with open(file_name, "r") as file:
        data = file.read().split("\n\n")
        seeds = [
            int(x)
            for x in data[0].split(": ")[1].split()
        ]
        maps = [
            [
                [
                    int(x)
                    for x in line.split()
                ]
                for line in map.split("\n")[1:]
            ]
            for map in data[1:]
        ]
    return seeds, maps

def part1(data):
    seeds, maps = data
    vals = [x for x in seeds]

    for map in maps:
        for i, val in enumerate(vals):
            for (dest, src, length) in map:
                if val >= src and val < src + length:
                    vals[i] = dest + (val - src)
                    break
    
    return min(vals)

def part2(data):
    seeds, maps = data
    vals = []
    for i in range(0, len(seeds), 2):
        vals.append((seeds[i], seeds[i] + seeds[i+1] - 1))
    
    for map in maps:
        new_vals = []
        while vals:
            (start, stop) = vals.pop()
            pass_through = True
            for (dest, src, length) in map:

                if start >= src and stop <= (src + length - 1):
                    new_vals.append((
                        dest + start - src, 
                        dest + stop - src
                    ))
                    pass_through = False
                    break

                elif src <= start and (src + length - 1) > start:
                    new_vals.append((
                        dest + start - src, 
                        dest + length - 1
                    ))
                    vals.append((
                        src + length,
                        stop
                    ))
                    pass_through = False
                    break

                elif (src + length - 1) >= stop and src < stop:
                    vals.append((
                        start,
                        src - 1
                    ))
                    new_vals.append((
                        dest,
                        dest + stop - src
                    ))
                    pass_through = False
                    break

                elif src > start and (src + length - 1) < stop:
                    vals.append((
                        start,
                        src - 1
                    ))
                    new_vals.append((
                        dest,
                        dest + length - 1
                    ))
                    vals.append((
                        src + length,
                        stop
                    ))
                    pass_through = False
                    break

            if pass_through:
                new_vals.append((start, stop))

        vals = new_vals

    return min(vals, key=lambda x : x[0])[0]
