from functools import cache, cmp_to_key
from queue import Queue, PriorityQueue
from heapq import heappush, heappop
import re
from copy import deepcopy
from math import *


def parse(file_name):
    with open(file_name, "r") as file:
        maze = file.read().splitlines()

    nodes_1, nodes_2, nodes_pos = get_nodes_from_maze(maze)
    remove_nodes(nodes_1)
    remove_nodes(nodes_2)
    nodes_1, nodes_i_1, nodes_pos_1 = rename_nodes(nodes_1, nodes_pos)
    nodes_2, nodes_i_2, nodes_pos_2 = rename_nodes(nodes_2, nodes_pos)

    start, goal = get_start_goal(maze)

    return (nodes_1, nodes_i_1[start], nodes_i_1[goal]), (nodes_2, nodes_i_2[start], nodes_i_2[goal])

def get_nodes_from_maze(maze):
    def in_bound(x,y):
        return 0 <= x < len(maze[0]) and 0 <= y < len(maze)

    def adjacent(x,y):
        yield x,y-1, 1
        yield x+1,y, 2
        yield x,y+1, 4
        yield x-1,y, 8
    
    def is_junction(x,y):
        if maze[y][x] != '.': 
            return False
        dirs = sum(dir for x2,y2,dir in adjacent(x,y) if in_bound(x2,y2) and maze[y2][x2] != '#')
        return dirs != 5 and dirs != 10
    
    nodes_1 = []
    nodes_2 = []
    nodes_i = {}
    nodes_pos = []
    node_i = 0

    w,h = len(maze[0]), len(maze)

    for y in range(h):
        prev = None
        prev_i = None
        only_left = False
        only_right = False
        for x in range(w):
            if maze[y][x] == '#':
                prev = None
                prev_i = None
            elif maze[y][x] == '<':
                only_left = True
            elif maze[y][x] == '>':
                only_right = True
            
            if not is_junction(x,y):
                continue

            node = (x,y)
            nodes_i[node] = node_i
            nodes_pos.append(node)
            nodes_1.append([])
            nodes_2.append([])
            if prev and not only_left:
                nodes_1[prev_i].append((node_i, x-prev[0]))
            if prev and not only_right:
                nodes_1[node_i].append((prev_i, x-prev[0]))
            if prev:
                nodes_2[prev_i].append((node_i, x-prev[0]))
                nodes_2[node_i].append((prev_i, x-prev[0]))

            prev = node
            prev_i = node_i
            node_i += 1
            only_left = False
            only_right = False
    
    for x in range(w):
        prev = None
        prev_i = None
        only_up = False
        only_down = False
        for y in range(h):
            if maze[y][x] == '#':
                prev = None
                prev_i = None
            elif maze[y][x] == '^':
                only_up = True
            elif maze[y][x] == 'v':
                only_down = True
            
            if not is_junction(x,y):
                continue

            node = (x,y)
            node_i = nodes_i[node]
            if prev and not only_up:
                nodes_1[prev_i].append((node_i, y-prev[1]))
            if prev and not only_down:
                nodes_1[node_i].append((prev_i, y-prev[1]))
            if prev:
                nodes_2[prev_i].append((node_i, y-prev[1]))
                nodes_2[node_i].append((prev_i, y-prev[1]))
            prev = node
            prev_i = node_i
            only_up = False
            only_down = False

    return nodes_1, nodes_2, nodes_pos

def remove_nodes(nodes):
    in_nodes = [[] for _ in range(len(nodes))]
    def is_removable(node):
        return len(nodes[node]) == 2 and len(in_nodes[node]) == 2 and all(adj in in_nodes[node] for adj in nodes[node])
    
    for node, adjacents in enumerate(nodes):
        for adj, cost in adjacents:
            in_nodes[adj].append((node, cost))

    for node in range(1, len(nodes)-1):
        if not is_removable(node):
            continue
        (adj1, cost1), (adj2, cost2) = nodes[node]

        nodes[adj1].remove((node, cost1))
        nodes[adj2].remove((node, cost2))
        nodes[adj1].append((adj2, cost1+cost2))
        nodes[adj2].append((adj1, cost1+cost2))

        in_nodes[adj1].remove((node, cost1))
        in_nodes[adj2].remove((node, cost2))
        in_nodes[adj1].append((adj2, cost1+cost2))
        in_nodes[adj2].append((adj1, cost1+cost2))

        in_nodes[node] = None
        nodes[node] = None
        
    # for node in range(1, len(nodes)-1):
    #     if nodes[node] is None or len(in_nodes[node]) != 1:
    #         continue
    #     in_node, in_cost = in_nodes[node][0]
        
    #     nodes[in_node].remove((node, in_cost))
    #     if (node, in_cost) in in_nodes[in_node]:
    #         in_nodes[in_node].remove((node, in_cost))
    #     for out_node, out_cost in nodes[node]:
    #         if out_node == in_node:
    #             continue
    #         nodes[in_node].append((out_node, in_cost+out_cost))
    #         in_nodes[out_node].remove((node, out_cost))
    #         in_nodes[out_node].append((in_node, in_cost+out_cost))

    #     in_nodes[node] = None
    #     nodes[node] = None

    # for node in range(1, len(nodes)-1):
    #     if nodes[node] is None or len(nodes[node]) != 1:
    #         continue
    #     out_node, out_cost = nodes[node][0]

    #     in_nodes[out_node].remove((node, out_cost))
    #     if (node, out_cost) in nodes[out_node]:
    #         nodes[out_node].remove((node, out_cost))
    #     for in_node, in_cost in in_nodes[node]:
    #         if out_node == in_node:
    #             continue
    #         in_nodes[out_node].append((in_node, in_cost+out_cost))
    #         nodes[in_node].remove((node, in_cost))
    #         nodes[in_node].append((out_node, in_cost+out_cost))

    #     in_nodes[node] = None
    #     nodes[node] = None
    
def rename_nodes(nodes, nodes_pos):
    new_node_i = 0
    old_to_new = [None for _ in range(len(nodes))]
    new_nodes = []
    new_nodes_i = {}
    new_nodes_pos = []

    for i, adjacents in enumerate(nodes):
        if adjacents is None:
            continue

        old_to_new[i] = new_node_i
        new_nodes.append(adjacents)
        new_nodes_pos.append(nodes_pos[i])
        new_nodes_i[nodes_pos[i]] = new_node_i
        new_node_i += 1
    
    for adjacents in new_nodes:
        for i, (adj, cost) in enumerate(adjacents):
            adjacents[i] = (old_to_new[adj], cost)

    return new_nodes, new_nodes_i, new_nodes_pos

def pprint(maze, nodes, nodes_i):
    for y in range(len(maze)):
        row = ""
        for x in range(len(maze[0])):
            if (x,y) in nodes_i and nodes[nodes_i[(x,y)]]:
                row += str(nodes_i[(x,y)]).ljust(2).rjust(3)
            else:
                row += maze[y][x].ljust(2).rjust(3)
        print(row)

def get_start_goal(maze):
    h = len(maze)

    x=0
    while maze[0][x] != '.':
        x += 1
    start = (x, 0)

    x=0
    while maze[h-1][x] != '.':
        x += 1
    goal = (x, h-1)

    return start, goal

def part1(data):
    nodes, start, goal = data[0]
    visited = set()
    def backtracker(node, steps, longest_path):
        if node == goal:
            return max(steps, longest_path)
        if node in visited:
            return 0
        visited.add(node)
        longest_path = max(longest_path, *(backtracker(next, steps+cost, longest_path) for next, cost in nodes[node]))
        visited.remove(node)
        return longest_path
    return backtracker(start, 0, 0)

def part2(data):
    nodes, start, goal = data[1]
    visited = set()
    def backtracker(node, steps, longest_path):
        if node == goal:
            return max(steps, longest_path)
        if node in visited:
            return 0
        visited.add(node)
        longest_path = max(longest_path, *(backtracker(next, steps+cost, longest_path) for next, cost in nodes[node]))
        visited.remove(node)
        return longest_path
    return backtracker(start, 0, 0)