from functools import cache, cmp_to_key
from queue import Queue, PriorityQueue
from heapq import heappush, heappop
import re
from copy import deepcopy
from math import *


def parse(file_name):
    with open(file_name, "r") as file:
        data = [
            [int(x) for x in line]
            for line in file.read().splitlines()
        ]
    return data

def astar(maze, start, goal, min_steps, max_steps):
    pq = PriorityQueue()
    pq.put((0, *start, 0,0, min_steps))
    visited = set()
    while not pq.empty():
        heat_loss, x, y, dx, dy, steps = pq.get()

        if (x,y,dx,dy,steps) in visited or steps > max_steps:
            continue
        
        visited.add((x,y,dx,dy,steps))

        if (x,y) == goal and steps >= min_steps:
            return heat_loss

        for dx2, dy2 in ((1,0), (-1,0), (0,1), (0,-1)):

            if (dx,dy) == (dx2,dy2): 
                if not (0 <= x+dx2 < len(maze[0]) and 0 <= y+dy2 < len(maze)):
                    continue
                pq.put((
                    heat_loss + maze[y+dy2][x+dx2], x+dx2, y+dy2, dx2, dy2, steps + 1
                ))

            elif (-dx,-dy) != (dx2,dy2):
                if not (0 <= x+dx2*min_steps < len(maze[0]) and 0 <= y+dy2*min_steps < len(maze)):
                    continue
                
                x2 = x+dx2
                y2 = y+dy2
                heat_loss2 = heat_loss + maze[y2][x2]
                for i in range(1, min_steps):
                    visited.add((x2, y2, dx2, dy2, i))
                    x2 += dx2
                    y2 += dy2
                    heat_loss2 += maze[y2][x2]

                pq.put((
                    heat_loss2, x2, y2, dx2, dy2, min_steps
                ))

def part1(data):
    start = (0,0)
    goal = (len(data[0])-1, len(data)-1)
    return astar(data, start, goal, 1, 3)
    
def part2(data):
    start = (0,0)
    goal = (len(data[0])-1, len(data)-1)
    return astar(data, start, goal, 4, 10)
