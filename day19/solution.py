from functools import cache, cmp_to_key
from queue import Queue, PriorityQueue
from heapq import heappush, heappop
import re
from copy import deepcopy
from math import *


def parse(file_name):
    with open(file_name, "r") as file:
        workflows_str, ratings_str = file.read().split("\n\n")

    workflows = {}
    for workflow in workflows_str.splitlines():
        i = workflow.index("{")
        name = workflow[:i]
        conditions = workflow[i+1:-1].split(",")
        conditions[-1] = ("x>0:"+conditions[-1])
        for i, condition in enumerate(conditions):
            conditions[i] = (condition[0], condition[1], *condition[2:].split(":"),)
        workflows[name] = conditions

    ratings_pattern = re.compile("{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")
    ratings = [
        [
            int(x) 
            for x in re.fullmatch(ratings_pattern, line).groups()
        ]
        for line in ratings_str.splitlines()
    ]

    return workflows, ratings



def part1(data):
    workflows, ratings = data
    def eval_rating(rating, start):
        x,m,a,s = rating
        workflow = start
        while True:
            for var, op, val, dest in workflows[workflow]:
                res = eval(var+op+val)
                if not res:
                    continue
                if dest == "A":
                    return True
                if dest == "R":
                    return False
                workflow = dest
                break

    sum_total = 0
    for rating in ratings:
        accepted = eval_rating(rating, "in")
        if accepted:
            sum_total += sum(rating)
    return sum_total


def part2(data):
    workflows, _ = data
    dfs = [("in", 1, 4000, 1,4000, 1,4000, 1,4000)]
    combinations = 0

    while dfs:
        workflow, x1, x2, m1, m2, a1, a2, s1, s2 = dfs.pop()

        if workflow == "R":
            continue
        if workflow == "A":
            combinations += (x2-x1+1) * (m2-m1+1) * (a2-a1+1) * (s2-s1+1)
            continue
        
        for var, op, val, dest in workflows[workflow]:
            val = int(val)

            if var == "x" and op == ">":
                if x2 <= val:
                    continue

                if x1 > val:
                    dfs.append((
                        dest, x1,x2,m1,m2,a1,a2,s1,s2
                    ))
                    break
                else:
                    dfs.append((
                        dest, val+1,x2,m1,m2,a1,a2,s1,s2
                    ))
                    x2 = val

            elif var == "x" and op == "<":
                if x1 >= val:
                    continue

                if x2 < val:
                    dfs.append((
                        dest, x1,x2,m1,m2,a1,a2,s1,s2
                    ))
                    break
                else:
                    dfs.append((
                        dest, x1,val-1,m1,m2,a1,a2,s1,s2
                    ))
                    x1 = val

            elif var == "m" and op == ">":
                if m2 <= val:
                    continue

                if m1 > val:
                    dfs.append((
                        dest, x1,x2,m1,m2,a1,a2,s1,s2
                    ))
                    break
                else:
                    dfs.append((
                        dest, x1,x2,val+1,m2,a1,a2,s1,s2
                    ))
                    m2 = val

            elif var == "m" and op == "<":
                if m1 >= val:
                    continue

                if m2 < val:
                    dfs.append((
                        dest, x1,x2,m1,m2,a1,a2,s1,s2
                    ))
                    break
                else:
                    dfs.append((
                        dest, x1,x2,m1,val-1,a1,a2,s1,s2
                    ))
                    m1 = val

            elif var == "a" and op == ">":
                if a2 <= val:
                    continue

                if a1 > val:
                    dfs.append((
                        dest, x1,x2,m1,m2,a1,a2,s1,s2
                    ))
                    break
                else:
                    dfs.append((
                        dest, x1,x2,m1,m2,val+1,a2,s1,s2
                    ))
                    a2 = val

            elif var == "a" and op == "<":
                if a1 >= val:
                    continue

                if a2 < val:
                    dfs.append((
                        dest, x1,x2,m1,m2,a1,a2,s1,s2
                    ))
                    break
                else:
                    dfs.append((
                        dest, x1,x2,m1,m2,a1,val-1,s1,s2
                    ))
                    a1 = val

            elif var == "s" and op == ">":
                if s2 <= val:
                    continue

                if s1 > val:
                    dfs.append((
                        dest, x1,x2,m1,m2,a1,a2,s1,s2
                    ))
                    break
                else:
                    dfs.append((
                        dest, x1,x2,m1,m2,a1,a2,val+1,s2
                    ))
                    s2 = val

            elif var == "s" and op == "<":
                if s1 >= val:
                    continue

                if s2 < val:
                    dfs.append((
                        dest, x1,x2,m1,m2,a1,a2,s1,s2
                    ))
                    break
                else:
                    dfs.append((
                        dest, x1,x2,m1,m2,a1,a2,s1,val-1
                    ))
                    s1 = val

    return combinations