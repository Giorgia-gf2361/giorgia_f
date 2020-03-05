#!/usr/bin/env python
#coding:utf-8
import numpy as np
import time

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def get_box(key):
    for r_idx, r in enumerate(ROW):
        for c_idx, c in enumerate(COL):
            if (key[0] == r) and (key[-1] == c):    
                return boxes[r_idx][c_idx]

def check_cols(n, col, board):
    for key in board.keys():
        if key[-1] == col:
            if board[key] == n:
                return False
    return True

def check_rows(n, row, board):
    for key in board.keys():
        if key[0] == row:
            if board[key] == n:
                return False
    return True

def check_box(n, box):
    global box_to_vals
    if n in box_to_vals[box]:
        return False
    return True

def is_legal(n, coord, board):
    return (check_cols(n, coord[-1], board) and check_rows(n, coord[0], board) and check_box(n, get_box(coord)))

def is_complete(board):
    return (not 0 in board.values())

def all_legal_vals(coord, board):
    legal_vals = []
    for n in range(1,10):
        if is_legal(n, coord, board):
            legal_vals.append(n)
    return legal_vals

def get_mrv(open_coords, board):
    possible_moves = [(all_legal_vals(coord, board), coord) for coord in open_coords]
    n_moves_per_box = [len(moves[0]) for moves in possible_moves]
    idx = np.argmin(n_moves_per_box)
    return open_coords[idx], possible_moves[idx][0]

def backtracking(board):

    b = board
    
    "Backtracking search to solve soduku"
    # If soduku is complete return it.
    if is_complete(b):
        return b
    
    # Select the MRV variable to fill
    '''
    get coordinates of available spaces to fill
    '''
    open_moves = [key for key,value in b.items() if value==0]
    
    coord, vals = get_mrv(open_moves, b)
    
    # Fill in a value and solve further (recursively), 
    # backtracking an assignment when stuck
    for value in vals:
        b[coord] = value
        result = backtracking(b)
        if result:
            return result
        else:
            b[coord] = 0
    return False

boxes = [[(i//3,j//3) for i in range(9)] for j in range(9)]
box_to_vals = dict()
solution_data = dict()

if __name__ == '__main__':
    #  Read boards from source.
    src_filename = 'starter/sudokus_start.txt'
    try:
        srcfile = open(src_filename, "r")
        sudoku_list = srcfile.read()
    except:
        print("Error reading the sudoku file %s" % src_filename)
        exit()

    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")

    # Solve each board using backtracking
    for line in sudoku_list.split("\n"):

        if len(line) < 9:
            continue

        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(line[9*r+c])
                  for r in range(9) for c in range(9)}

        #Reset pertinent globals:
        box_to_vals = dict()
        
        #Prep grid reference:
        for key in board.keys():
            val = board[key]
            box = get_box(key)
            if box_to_vals.get(box):
                box_to_vals[box].append(val)
            else:
                box_to_vals[box] = [val]
                
        start = time.time()
        solution = backtracking(board)
        end = time.time()
    
        time_to_solve = end-start
        print(time_to_solve)

        solution_data[line] = {'solution':solution, 'time':time_to_solve}
        
        # Print starting board. TODO: Comment this out when timing runs.
        print_board(board)

        # Solve with backtracking
        #solved_board = backtracking(board)

        # Print solved board. TODO: Comment this out when timing runs.
        print_board(solution)

        # Write board to file
        outfile.write(board_to_string(solution))
        outfile.write('\n')

    print("Finishing all boards in file.")
