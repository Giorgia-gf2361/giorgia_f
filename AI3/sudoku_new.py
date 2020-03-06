#!/usr/bin/env python
#coding:utf-8
import numpy as np
import time
from itertools import product

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"

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
    
    return (check_cols(n, coord[-1], board) and check_rows(n, coord[0], board) \
            and check_box(n, get_box(coord)) and (n>0) and (n<10))\
            and (board[coord]==0)
            
def is_complete(board):
    return (not 0 in board.values())

def all_legal_vals(coord, board):
    legal_vals = []
    for n in range(1,10):
        if is_legal(n, coord, board):
            legal_vals.append(n)
    return legal_vals

def get_mrv_improved():
    #Sort list of available moves from global moveset dict.
    #return minimum.
    to_return = sorted([(len(v), v, k) for k,v in moveset.items() if v])
    if to_return:
        return to_return[0]
    else:
        return

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

def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
        
    b = board.copy()
    
    if is_complete(b):
        return b
    
    '''
    get coordinates of available spaces to fill
    '''
    mrv_result = get_mrv_improved()

    if mrv_result:
        _, vals, coord = mrv_result
        for value in vals:
                row_coords = [i+j for i,j in product(coord[0], COL)]
                col_coords = [j+i for i,j in product(coord[1], ROW)]
                box_coords = [i for i in box_to_coords[get_box(coord)]]
                impacted = set(row_coords+col_coords+box_coords)
                impacted.remove(coord)

                b[coord] = value
                old_moveset_values = moveset[coord]
                moveset[coord] = set()

                removed = []
                for c in impacted:
                    if value in moveset[c]:
                        moveset[c].remove(value)
                        removed.append(c)

                result = backtracking(b)
                if result:
                    return result
                else:
                    b[coord] = 0
                    moveset[coord] = old_moveset_values
                    for c in removed:
                        moveset[c].add(value)

    return False

def to_np(inp):
    bd = np.array(list(inp.values())).reshape((9,9))
    return bd

def to_dict(line):
    global ROW
    global COL
    return {ROW[r] + COL[c]: int(line[9*r+c]) for r in range(9) for c in range(9)}

def parse_grid(board):
    global box_to_vals
    for key in board.keys():
        val = board[key]
        box = get_box(key)
        if box_to_vals.get(box):
            box_to_vals[box].append(val)
        else:
            box_to_vals[box] = [val]
            
        
boxes = [[(i//3,j//3) for i in range(9)] for j in range(9)]
box_to_vals = dict()
solution_data = dict()
moveset = dict()

if __name__ == '__main__':
    #  Read boards from source.
    src_filename = 'sudokus_start.txt'
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
        board = { ROW[r] + COL[c]: int(line[9*r+c])
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
                
        coords = [i+j for i,j in product(ROW, COL)]
        box_to_coords = dict()
        for coord in board.keys():
            box = get_box(coord)
            if not box_to_coords.get(box):
                box_to_coords[box] = []
            box_to_coords[box].append(coord)
                
        moveset = {coord:set(all_legal_vals(coord, board)) for coord, val in board.items()}

            
    
        start = time.time()
        solution = backtracking(board)
        end = time.time()
        time_to_solve = end-start

        solution_data[line] = {'solution':solution, 'time':time_to_solve}
        print(solution_data[line]['time'])
        
        
        
        
        
        
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
