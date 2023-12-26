from functools import cache, cmp_to_key
from queue import Queue, PriorityQueue
from heapq import heappush, heappop
import re
from copy import deepcopy
from math import *


def parse(file_name):
    with open(file_name, "r") as file:
        data = file.read()

    bricks = []
    for brick in data.splitlines():
        (x1,y1,z1), (x2,y2,z2) = [
            [int(x) for x in side.split(",")]
            for side in brick.split("~")
        ]
        bricks.append( ( (x1,y1,z1), (x2,y2,z2) ) ) 

    bricks.sort(key=lambda x: x[0][2])
    
    def full_brick(brick): 
        (x1,y1,z1), (x2,y2,z2) = brick
        return {
            (x,y,z)
            for x in range(x1, x2+1)
            for y in range(y1, y2+1)
            for z in range(z1, z2+1)
        }

    n = len(bricks)
    occupied = set()
    for i in range(n):
        (x1,y1,z1), (x2,y2,z2) = bricks[i]
        while not occupied.intersection(full_brick( ( (x1,y1,z1-1), (x2,y2,z2-1) ) )) and z1 > 1:
            z1 -= 1
            z2 -= 1
        
        bricks[i] = ( (x1,y1,z1), (x2,y2,z2) )
        occupied.update(full_brick(bricks[i]))
    
    bricks.sort(key=lambda x: x[0][2])


    over = {i:[] for i in range(n)}
    under = {i:[] for i in range(n)}

    for i in range(n):
        (x1,y1,z1), (x2,y2,z2) = bricks[i]
        full_brick_i = full_brick( ( (x1,y1,z1+1), (x2,y2,z2+1) ) )
        for j in range(i+1, n):
            if bricks[j][0][2] > z2+1:
                break

            if full_brick_i.intersection(full_brick(bricks[j])):
                under[j].append(i)
                over[i].append(j)

    return bricks, over, under

def part1(data):
    bricks, over, under = data
    return sum( all( len(under[j]) > 1 for j in over[i] ) for i in range(len(bricks)) )

def part2(data):
    bricks, over, under = data

    n = len(bricks)
    bottom = [i for i,brick in enumerate(bricks) if brick[0][2] == 1]
    total = 0
    for brick in range(n):
        visited = set()
        dfs = [i for i in bottom]

        while dfs:
            i = dfs.pop()
            if i in visited:
                continue
            visited.add(i)
            if i == brick:
                continue
            dfs.extend(over[i])

        total += n-len(visited)
    
    return total
            

