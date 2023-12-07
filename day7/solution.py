from functools import cache, cmp_to_key
from queue import Queue, PriorityQueue
from heapq import heappush, heappop
import re
from copy import deepcopy
from math import *


def parse(file_name):
    with open(file_name, "r") as file:
        data = [
            (line.split()[0], int(line.split()[1]))
            for line in file.read().splitlines()
        ]
    return data

@cache
def type_p1(hand):
    freqs = dict()
    for card in hand:
        if card not in freqs:
            freqs[card] = 0
        freqs[card] += 1
    sorted_freqs = sorted(freqs.values(), reverse=True)

    if sorted_freqs[0] == 5: return 7
    if sorted_freqs[0] == 4: return 6
    if sorted_freqs[0] == 3 and sorted_freqs[1] == 2: return 5
    if sorted_freqs[0] == 3: return 4
    if sorted_freqs[0] == 2 and sorted_freqs[1] == 2: return 3
    if sorted_freqs[0] == 2: return 2
    return 1

def compare_p1(hand1, hand2):
    if type_p1(hand1) > type_p1(hand2):
        return 1
    
    if type_p1(hand1) < type_p1(hand2):
        return -1
    
    card_to_val = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

    for i in range(5):
        if card_to_val[hand1[i]] > card_to_val[hand2[i]]:
            return 1
        
        if card_to_val[hand1[i]] < card_to_val[hand2[i]]:
            return -1
    return 0

def part1(data):
    data = deepcopy(data)

    val = 0

    for i in range(len(data)):
        lowest = i

        for j in range(i+1, len(data)):
            if compare_p1(data[lowest][0], data[j][0]) == 1:
                lowest = j


        data[i], data[lowest] = data[lowest], data[i]

        val += data[i][1] * (i+1)

    return val

@cache
def type_p2(hand):
    jokers = 0
    freqs = dict()
    for card in hand:
        if card == "J":
            jokers += 1
            continue
        if card not in freqs:
            freqs[card] = 0
        freqs[card] += 1
    sorted_freqs = sorted(freqs.values(), reverse=True)

    sorted_freqs.append(0)
    sorted_freqs.append(0)

    if sorted_freqs[0] + jokers == 5: return 7
    if sorted_freqs[0] + jokers == 4: return 6
    if sorted_freqs[0] + jokers == 3 and sorted_freqs[1] == 2: return 5
    if sorted_freqs[0] + jokers == 3: return 4
    if sorted_freqs[0] + jokers == 2 and sorted_freqs[1] == 2: return 3
    if sorted_freqs[0] + jokers == 2: return 2
    return 1

def compare_p2(hand1, hand2):
    if type_p2(hand1) > type_p2(hand2):
        return 1
    
    if type_p2(hand1) < type_p2(hand2):
        return -1
    
    card_to_val = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 0, "Q": 12, "K": 13, "A": 14}

    for i in range(5):
        if card_to_val[hand1[i]] > card_to_val[hand2[i]]:
            return 1
        
        if card_to_val[hand1[i]] < card_to_val[hand2[i]]:
            return -1
    return 0

def part2(data):
    data = deepcopy(data)

    val = 0

    for i in range(len(data)):
        lowest = i

        for j in range(i+1, len(data)):
            if compare_p2(data[lowest][0], data[j][0]) == 1:
                lowest = j


        data[i], data[lowest] = data[lowest], data[i]

        val += data[i][1] * (i+1)

    return val
