import sys
import numpy as np
from functools import reduce

# Instructions:
# Linux>> python3 driver_3.py <soduku_str>
# Windows py3\> python driver_3.py <soduku_str>

# Inputs
print("input was:", sys.argv)
soduku_str=sys.argv[1]

def str2arr(soduku_str):
    "Converts soduku_str to 2d array"
    return np.array([int(s) for s in list(soduku_str)]).reshape((9,9))

soduku = str2arr(soduku_str)

slices = [slice(0,3), slice(3,6), slice(6,9)]
s1,s2,s3 = slices
allgrids=[(si,sj) for si in [s1,s2,s3] for sj in [s1,s2,s3]] # Makes 2d slices for grids

def var2grid(var):
    "Returns the grid slice (3x3) to which the variable's coordinates belong "
    row,col = var
    grid = ( slices[int(row/3)], slices[int(col/3)] )
    return grid

FULLDOMAIN = np.array(range(1,10)) #All possible values (1-9)


# Constraints
def unique_rows(soduku):
    for row in soduku:
        if not np.array_equal(np.unique(row),np.array(range(1,10))) :
            return False
    return True
def unique_columns(soduku):
    for row in soduku.T: #transpose soduku to get columns
        if not np.array_equal(np.unique(row),np.array(range(1,10))) :
            return False
    return True

def unique_grids(soduku):
    for grid in allgrids:
        if not np.array_equal(np.unique(soduku[grid]),np.array(range(1,10))) :
            return False
    return True

def isComplete(soduku):
    if 0 in soduku:
        return False
    else:
        return True


def checkCorrect(soduku):
    if unique_columns(soduku):
        if unique_rows(soduku):
            if unique_grids(soduku):
                return True
    return False


# Search
def getDomain(var, soduku):
    "Gets the remaining legal values (available domain) for an unfilled box `var` in `soduku`"
    row,col = var
    #ravail = np.setdiff1d(FULLDOMAIN, soduku[row,:])
    #cavail = np.setdiff1d(FULLDOMAIN, soduku[:,col])
    #gavail = np.setdiff1d(FULLDOMAIN, soduku[var2grid(var)])
    #avail_d = reduce(np.intersect1d, (ravail,cavail,gavail))

    '''
    used_d = numbers used for a given coord
    avail_d = numbers not used - i.e. available.
    '''
    used_d = reduce(np.union1d, (soduku[row,:], soduku[:,col], soduku[var2grid(var)]))
    avail_d = np.setdiff1d(FULLDOMAIN, used_d)
    #print(var, avail_d)
    return avail_d

def selectMRVvar(vars, soduku):
    """
    Returns the unfilled box `var` with minimum remaining [legal] values (MRV)
    and the corresponding values (available domain)
    """
    #Could this be improved?
    avail_domains = [getDomain(var,soduku) for var in vars]
    avail_sizes = [len(avail_d) for avail_d in avail_domains]
    index = np.argmin(avail_sizes)
    return vars[index], avail_domains[index]

def BT(soduku):
    "Backtracking search to solve soduku"
    # If soduku is complete return it.
    if isComplete(soduku):
        return soduku
    # Select the MRV variable to fill
    vars = [tuple(e) for e in np.transpose(np.where(soduku==0))]
    var, avail_d = selectMRVvar(vars, soduku)
    # Fill in a value and solve further (recursively),
    # backtracking an assignment when stuck
    for value in avail_d:
        soduku[var] = value
        result = BT(soduku)
        if np.any(result):
            return result
        else:
            soduku[var] = 0
    return False


# Solve
print("solved:\n", BT(soduku))
print("correct:", checkCorrect(soduku))


# Output
with open('output.txt','w') as f:
    output_str = np.array2string(soduku.ravel(), max_line_width=90, separator='').strip('[]') + ' Solved with BTS'
    f.write(output_str)