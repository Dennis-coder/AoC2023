from functools import cache, cmp_to_key
from queue import Queue, PriorityQueue
from heapq import heappush, heappop
import re
from copy import deepcopy
from math import *


def parse(file_name):
    with open(file_name, "r") as file:
        data = []
        for line in file.read().splitlines():
            direction, length, color = line.split()
            data.append((direction, int(length), color[2:8]))
    return data

def dx_dy(direction):
    match direction:
        case "U": return (0,-1)
        case "D": return (0,1)
        case "L": return (-1,0)
        case "R": return (1,0)
        case "3": return (0,-1)
        case "1": return (0,1)
        case "2": return (-1,0)
        case "0": return (1,0)

def part1(data):
    x = y = 0
    edges = {(x, y)}
    for direction, length, color in data:
        dx, dy = dx_dy(direction)
        for _ in range(length):
            x += dx
            y += dy
            edges.add((x,y))
    x1 = min([x for x, y in edges])
    x2 = max([x for x, y in edges])
    y1 = min([y for x, y in edges])
    y2 = max([y for x, y in edges])

    dfs = [(x1-1, y1-1)]
    visited = set()
    while dfs:
        x, y = dfs.pop()
        if (x,y) in visited or (x,y) in edges or x < x1-1 or x > x2+1 or y < y1-1 or y > y2+1:
            continue
        visited.add((x,y))
        dfs.append((x+1,y))
        dfs.append((x-1,y))
        dfs.append((x,y+1))
        dfs.append((x,y-1))
    
    x1 = min([x for x, y in visited])
    x2 = max([x for x, y in visited])
    y1 = min([y for x, y in visited])
    y2 = max([y for x, y in visited])

    return (x2 - x1 + 1) * (y2 - y1 + 1) - len(visited)

def part2(data):
    x = y = 0
    corners = [(x, y)]
    total_length = 0
    for _,_, color in data:
        direction = color[5]
        length = int(color[0:5], 16)
        total_length += length
        dx, dy = dx_dy(direction)
        x += dx*length
        y += dy*length
        corners.append((x,y))
    xs_set = set()
    ys_set = set()
    prev = corners[0]
    for corner in corners[1:]:
        if prev[0] == corner[0]:
            xs_set.add(corner[0])
        else:
            ys_set.add(corner[1])
        prev = corner

    xs = sorted(xs_set)
    ys = sorted(ys_set)

    x_to_i = {x:i for i,x in enumerate(xs)}
    y_to_i = {y:i for i,y in enumerate(ys)}

    corners_set = set()

    prev = corners[0]
    for corner in corners[1:]:
        if prev[0] == corner[0]:
            y1 = prev[1]
            y2 = corner[1]
            for i in range(y_to_i[min(prev[1], corner[1])], y_to_i[max(prev[1], corner[1])]):
                corners_set.add((corner[0], ys[i], corner[0], ys[i+1]))
        else:
            for i in range(x_to_i[min(prev[0], corner[0])], x_to_i[max(prev[0], corner[0])]):
                corners_set.add((xs[i], corner[1], xs[i+1], corner[1]))
        prev = corner


    dfs = [(0, 0)]
    visited = set()

    xs.insert(0, xs[0]-1)
    xs.append(xs[-1]+1)
    ys.insert(0, ys[0]-1)
    ys.append(ys[-1]+1)

    while dfs:
        i, j = dfs.pop()
        if (i,j) in visited or i < 0 or i == len(xs)-1 or j < 0 or j == len(ys)-1:
            continue
        visited.add((i,j))
        x1 = xs[i]
        x2 = xs[i+1]
        y1 = ys[j]
        y2 = ys[j+1]
        
        if not ((x1, y1, x2, y1) in corners_set or (x2, y1, x1, y1) in corners_set): 
            dfs.append((i, j-1))
        if not ((x2, y1, x2, y2) in corners_set or (x2, y2, x2, y1) in corners_set):
            dfs.append((i+1, j))
        if not ((x1, y2, x2, y2) in corners_set or (x2, y2, x1, y2) in corners_set):
            dfs.append((i, j+1))
        if not ((x1, y1, x1, y2) in corners_set or (x1, y2, x1, y1) in corners_set):
            dfs.append((i-1, j))
    
    volume = (xs[-1] - xs[0]) * (ys[-1]- ys[0])
    for i, j in visited:
        volume -= (xs[i+1] - xs[i]) * (ys[j+1] - ys[j])
    return volume + total_length // 2 + 1

