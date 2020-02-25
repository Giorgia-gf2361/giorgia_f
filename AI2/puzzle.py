from __future__ import division
from __future__ import print_function
import queue as q
import sys
import math
import time
from abc import ABC, abstractmethod

class searchStruct(ABC):
    @abstractmethod
    def put(self, initial_state):
        pass
    
    def get(self):
        pass
    
    def getNeighbors(self, board):
        pass
    
class bfsStruct(searchStruct): #uses queue
    def __init__(self):
        self.struct = q.Queue()
        
    def put(self, initial_state):
        self.struct.put(initial_state)
    
    def get(self):
        return self.struct.get()
    
    def getNeighbors(self, board):
        return board.expand()

#basic stack class, referenced: https://docs.python.org/2/tutorial/datastructures.html
class Stack(): #uses Stack
    def __init__(self):
        self.elems = list()
    
    def push(self, item):
        self.elems.append(item)

    def pop(self):
        return self.elems.pop()
    
class dfsStruct(searchStruct): #uses Stack
    def __init__(self):
        self.struct = Stack()
    
    def put(self, initial_state):
        self.struct.push(initial_state)
    
    def get(self):
        return self.struct.pop()  

    def getNeighbors(self, board):
        return board.expand()[::-1]

#used for weighting for the A* algorithm, cost from source + approximate cost to target

class Pair(object):
    def __init__(self, idx, state):
        self.state = state
        self.weight = total_cost(state)
        self.index = idx

    #referenced https://docs.python.org/3/howto/sorting.html for how to compare weights
    def __gt__(self, obj):
        if self.weight > obj.weight:
            return True
        elif self.weight == obj.weight and self.index > obj.index:
            return True
        else:
            return False

# The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n #move
        self.cost     = cost #cost of path
        self.parent   = parent
        self.action   = action #where you're moving
        self.config   = config #what the board looks like
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)
        #added
        self.blank_row = self.blank_index // self.n
        self.blank_col = self.blank_index % self.n
        #print(self.blank_row, self.blank_col)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_row == 0:
            return None
        else:
            dest = self.blank_index - self.n
            new_board = list(self.config)
            new_board[self.blank_index], new_board[dest] = new_board[dest], new_board[self.blank_index]
            return PuzzleState(tuple(new_board), self.n, parent = self, action = "Up", cost = (self.cost + 1))

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.blank_row == self.n-1:
            return None
        else:
            dest = self.blank_index + self.n
            new_board = list(self.config)
            new_board[self.blank_index], new_board[dest] = new_board[dest], new_board[self.blank_index]
            return PuzzleState(tuple(new_board), self.n, parent=self, action="Down", cost=(self.cost + 1))

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_col == 0:
            return None
        else:
            dest = self.blank_index - 1
            new_board = list(self.config)
            new_board[self.blank_index], new_board[dest] = new_board[dest], new_board[self.blank_index]
            return PuzzleState(tuple(new_board), self.n, parent=self, action="Left", cost=(self.cost + 1))

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if self.blank_col == self.n - 1:
            return None
        else:
            dest = self.blank_index + 1
            new_board = list(self.config)
            new_board[self.blank_index], new_board[dest] = new_board[dest], new_board[self.blank_index]
            return PuzzleState(tuple(new_board), self.n, parent=self, action="Right", cost=(self.cost + 1))
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

def search(initial_state, struct):

    explored = set()
    frntrset = set()
    max_sd, nodes_exp = 0, 0
    start_time = time.time()

    struct.put(initial_state)
    frntrset.add(initial_state.config)

    while struct.struct:

        board = struct.get()
        explored.add(board)

        if is_goal(board):
            writeOutput(path_to_goal(board),
                        board.cost,
                        nodes_exp,
                        max_sd,
                        time.time() - start_time)
            return

        neighbors = []
        
        if len(board.children) == 0:
            neighbors = struct.getNeighbors(board)
            nodes_exp += 1

        max_sd = neighbors[0].cost if neighbors[0].cost > max_sd else max_sd

        for idx, n in enumerate(neighbors):
            if n.config not in explored and n.config not in frntrset:
                struct.put(idx, n)
                frntrset.add(n.config)
                explored.add(n.config)

    return  


def bfs(initial_state):
    struct = bfsStruct()
    search(initial_state, struct)

def dfs(initial_state):
    struct = dfsStruct()
    search(initial_state, struct)


#https://docs.python.org/2/library/queue.html#Queue.PriorityQueue referenced
def A_star_search(initial_state):

    frontier, explored = q.PriorityQueue(), set()
    frntrset = set()
    max_sd, nodes_exp = 0, 0
    start_time = time.time()

    frontier.put(Pair(0, initial_state))
    frntrset.add(initial_state.config)

    while frontier:

        board = frontier.get().state #Weighted object's state
        explored.add(board)

        if is_goal(board):
            writeOutput(path_to_goal(board),
                        board.cost,
                        nodes_exp,
                        max_sd,
                        time.time() - start_time)
            return

        neighbors = []
        
        if len(board.children) == 0:
            neighbors = board.expand()
            nodes_exp += 1

        max_sd = neighbors[0].cost if neighbors[0].cost > max_sd else max_sd

        for idx, n in enumerate(neighbors):
            if n.config not in explored and n.config not in frntrset:
                frontier.put(Pair(idx, n))
                frntrset.add(n.config)
                explored.add(n.config)

    return

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    #Take the sum of the absolute values of the differences of the coordinates.
    return abs(idx // n - value // n) + abs(idx % n - value % n)

def total_cost(state):
    """calculate the total estimated cost of a state"""
    tc = 0

    for idx, val in enumerate(state.config):
        if val:
            tc += calculate_manhattan_dist(idx, val, state.n)

    return tc + state.cost

def path_to_goal(state):

    path = list()

    while state.parent:
        path.append(state.action)
        state = state.parent

    return path[::-1]

def is_goal(puzzle_state):

    return puzzle_state.config == (0,1,2,3,4,5,6,7,8)

def calc_ram():
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1e-9

def writeOutput(path, cost, nodes_exp, max_sd, runtime):
    path = str(path) + "\n"
    cost = str(cost) + "\n"
    nodes_exp = str(nodes_exp) + "\n"
    depth = cost
    max_sd = str(max_sd) + "\n"
    runtime = str(runtime) + "\n"

    f = open("output.txt", "w")

    f.write("path_to_goal: " + path)
    f.write("cost_of_path: " + cost)
    f.write("nodes_expanded: " + nodes_exp)
    f.write("search_depth: " + depth)
    f.write("max_search_depth: " + max_sd)
    f.write("running_time:  " + runtime)
    f.write("max_ram_usage:  " + str(calc_ram()))

    f.close()

# Main Function that reads in Input and Runs corresponding Algorithm
def main():

    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    
    if   search_mode == "bfs": bfs(hard_state)
    elif search_mode == "dfs": dfs(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else:
        print("Enter valid command arguments!")

if __name__ == '__main__':
    main()
    
    