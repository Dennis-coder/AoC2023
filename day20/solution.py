from math import lcm
from queue import Queue
from copy import deepcopy


def parse(file_name):
    with open(file_name, "r") as file:
        types = {}
        flops = {}
        conjunctions = set()
        con_inputs_max = {}
        con_inputs = {}
        dests = {}
        for line in file.read().splitlines():
            module, dest_modules = line.split(" -> ")
            dest_modules = dest_modules.split(", ")
            if module[0] == "%":
                types[module[1:]] = "%"
                dests[module[1:]] = dest_modules
                flops[module[1:]] = 0
            elif module[0] == "&":
                types[module[1:]] = "&"
                dests[module[1:]] = dest_modules
                conjunctions.add(module[1:])
                con_inputs_max[module[1:]] = 0
                con_inputs[module[1:]] = set()
            else:
                types[module] = ""
                dests[module] = dest_modules

    for module, dests2 in dests.items():
        for dest in dests2:
            if dest in conjunctions:
                con_inputs_max[dest] += 1
    
    return types, dests, flops, con_inputs, con_inputs_max

def part1(data):
    types, dests, flops, con_inputs, con_inputs_max = deepcopy(data)
    signals = [0,0]
    for _ in range(1000):
        bfs = Queue()
        bfs.put(("button", "broadcaster", 0))
        while not bfs.empty():
            from_module, to_module, in_strength = bfs.get()
            signals[in_strength] += 1

            if to_module not in types:
                continue

            type = types[to_module]
            out_strength = in_strength

            if type == "%":
                if in_strength:
                    continue
                flops[to_module] = 1-flops[to_module]
                out_strength = flops[to_module]
            
            elif type == "&":
                if in_strength:
                    con_inputs[to_module].add(from_module)
                elif from_module in con_inputs[to_module]:
                    con_inputs[to_module].remove(from_module)
                out_strength = int(len(con_inputs[to_module]) != con_inputs_max[to_module])

            for dest in dests[to_module]:
                bfs.put((to_module, dest, out_strength))

    return signals[0] * signals[1]

def part2(data):
    types, outputs, flops, con_inputs, con_inputs_max = deepcopy(data)

    inputs = {}
    for module, destinations in outputs.items():
        for dest in destinations:
            if dest not in inputs:
                inputs[dest] = []
            inputs[dest].append(module)
    

    searching_for = inputs[inputs['rx'][0]]
    cycles = []
    i = 1
    done = False
    while not done:
        bfs = Queue()
        bfs.put(("button", "broadcaster", 0))
        while not bfs.empty():
            from_module, to_module, in_strength = bfs.get()

            if to_module not in types:
                continue

            type = types[to_module]
            out_strength = in_strength

            if type == "%":
                if in_strength:
                    continue
                flops[to_module] = 1-flops[to_module]
                out_strength = flops[to_module]
            
            elif type == "&":
                if in_strength:
                    con_inputs[to_module].add(from_module)
                elif from_module in con_inputs[to_module]:
                    con_inputs[to_module].remove(from_module)
                out_strength = int(len(con_inputs[to_module]) != con_inputs_max[to_module])


            if to_module in searching_for and out_strength:
                searching_for.remove(to_module)
                cycles.append(i)
            
            if len(searching_for) == 0:
                done = True

            for dest in outputs[to_module]:
                bfs.put((to_module, dest, out_strength))
        i += 1

    return lcm(*cycles)