#!/usr/bin/env python
"""
Name of the author(s):
- Auguste Burlats <auguste.burlats@uclouvain.be>
"""
import time
import sys
from copy import deepcopy
from search import *


#################
# Problem class #
#################
class TowerSorting(Problem):
    
    def __init__(self, max_height, colors, initial_state=None):
        self.max_height = max_height
        self.colors = colors
        self.initial_state = self.get_initial_state() if initial_state is None else initial_state

    def get_initial_state(self):
        towers = [[] for _ in range(len(self.colors))]
        for i, color in enumerate(self.colors):
            for j in range(0, len(color), self.max_height):
                tower = color[j:j+self.max_height]
                if tower:
                    towers[i].append(tower)
        return State(towers)

    def is_goal_state(self, state):
        for tower in state.towers:
            if not tower:
                continue
            if len(tower) != self.max_height or len(set(tower)) != 1:
                return False
        return True

    def get_successors(self, state):
        successors = []
        for i, tower in enumerate(state.towers):
            if not tower:
                continue
            for j, other_tower in enumerate(state.towers):
                if i == j or len(other_tower) == self.max_height:
                    continue
                new_state = state.copy()
                disk = new_state.towers[i][-1]
                new_state.towers[i] = tower[:-1]
                new_state.towers[j].append(tower[-1])
                successors.append((j, State(new_state.towers), (i, j)))
        return successors


###############
# State class #
###############
class State:

    def __init__(self, number, size, grid, move="Init"):
        self.number = number
        self.size = size
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for i in reversed(range(self.size)):
            for tower in self.grid:
                if len(tower) > i:
                    s += "".join(tower[i]) + " "
                else:
                    s += ". "
            s += "\n"
        return s

    def __eq__(self, other):
        pass

    def __hash__(self):
        pass


######################
# Auxiliary function #
######################
def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()

    number_tower, size_tower = tuple([int(i) for i in lines[0].split(" ")])
    initial_grid = [[] for i in range(number_tower)]
    for row in lines[1:size_tower+1]:
        elems = row.split(" ")
        for index in range(number_tower):
            if elems[index] != '.':
                initial_grid[index].append(elems[index])

    for tower in initial_grid:
        tower.reverse()

    return number_tower, size_tower, initial_grid


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./sort_tower.py <path_to_instance_file>")
    filepath = sys.argv[1]

    number, size, initial_grid = read_instance_file(filepath)

    init_state = State(number, size, initial_grid, "Init")
    problem = TowerSorting(init_state)
    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = depth_first_tree_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)
