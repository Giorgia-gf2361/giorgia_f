import numpy as np
import time
from tqdm import tqdm


ROW = "ABCDEFGHI"
COL = "123456789"

def get_box(key):
    for r_idx, r in enumerate(ROW):
        for c_idx, c in enumerate(COL):
            if (key[0] == r) and (key[-1] == c):
                return boxes[r_idx][c_idx]

def check_cols(n, col, input_board):
    for key in input_board.keys():
        if key[-1] == col:
            if input_board[key] == n:
                return False
    return True

def check_rows(n, row, input_board):
    for key in input_board.keys():
        if key[0] == row:
            if input_board[key] == n:
                return False
    return True

def check_box(n, box):
    global box_to_vals
    if n in box_to_vals[box]:
        return False
    return True

def is_legal(n, coord, input_board):
    return (check_cols(n, coord[-1], input_board) and check_rows(n, coord[0], input_board) and check_box(n, get_box(coord)) and (n > 0) and (n < 10))


def is_complete(input_board):
    return (not 0 in input_board.values())


def all_legal_vals(coord, input_board):
    legal_vals = []
    for n in range(1, 10):
        if is_legal(n, coord, input_board):
            legal_vals.append(n)
    return legal_vals


def get_mrv(open_coords, input_board):
    possible_moves = [(all_legal_vals(coord, input_board), coord) for coord in open_coords]
    n_moves_per_box = [len(moves[0]) for moves in possible_moves]
    idx = np.argmin(n_moves_per_box)
    return open_coords[idx], possible_moves[idx][0]


def solve_mrv(input_board):
    b = input_board.copy()


    # If soduku is complete return it.
    if is_complete(b):
        return b

    # Select the MRV variable to fill
    '''
    get coordinates of available spaces to fill
    '''
    open_moves = [key for key, value in b.items() if value == 0]

    coord, vals = get_mrv(open_moves, b)

    for value in vals:
        b[coord] = value
        result = solve_mrv(b)
        if result:
            return result
        else:
            b[coord] = 0
    return False


def to_np(input_board):
    bd = np.array(list(input_board.values())).reshape((9, 9))
    return bd


def to_dict(line):
    global ROW
    global COL
    return {ROW[r] + COL[c]: int(line[9*r+c]) for r in range(9) for c in range(9)}



with open('starter/sudokus_start.txt', 'r+') as f:
    sudokus = [to_dict(i.strip()) for i in f.readlines()]

boxes = [[(i // 3, j // 3) for i in range(9)] for j in range(9)]
box_to_vals = dict()
solution_data = dict()

for idx, board in tqdm(enumerate(sudokus)):
    # Reset pertinent globals:
    box_to_vals = dict()
    solution_data = dict()

    # board = sudokus[16]

    # Prep grid reference:
    for key in board.keys():
        val = board[key]
        box = get_box(key)
        if box_to_vals.get(box):
            box_to_vals[box].append(val)
        else:
            box_to_vals[box] = [val]

    start = time.time()
    solution = solve_mrv(board)
    end = time.time()

    time_to_solve = end - start

    solution_data[idx] = {'solution': solution, 'time': time_to_solve}

    if solution:
        print(to_np(solution))
    else:
        print('No solution found.')

    print(f'{(time_to_solve)} sec')

