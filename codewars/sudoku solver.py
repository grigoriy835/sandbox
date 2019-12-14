puzzle = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]

import functools
temp = None


def sudoku(puzzle):
    global temp
    temp = puzzle
    while True:
        was_changed = False
        has_zero = False
        for x in range(0, 9):
            for y in range(0, 9):
                if puzzle[x][y] not in range(1, 10):

                    possible = get_by_coords(x, y)
                    if len(possible) == 1:
                        puzzle[x][y] = possible.pop()
                        was_changed = True
                    else:
                        puzzle[x][y] = possible
                        has_zero = True
        if not was_changed:
            return False

        if not has_zero:
            return puzzle


def get_by_coords(x, y):
    return get_by_line(x) & get_by_square(x, y) & get_by_column(y) & get_by_square_column(x,y) & get_by_square_line(x,y)


def get_by_line(x):
    return set(range(1, 10)) - set(i for i in temp[x] if type(i) is int)


def get_by_column(y):
    return set(range(1, 10)) - set(line[y] for line in temp if type(line[y]) is int)


def get_by_square(x, y):
    res = set(range(1, 10))
    for line in temp[x // 3 * 3:(x // 3 + 1) * 3]:
        res = res - set(i for i in line[y//3*3:(y//3+1)*3] if type(i) is int)
    return res

def get_by_square_line(x, y):
    # todo
    return set(range(1, 10))


def get_by_square_column(x, y):
    # todo
    return set(range(1, 10))


solution = [[5,3,4,6,7,8,9,1,2],
            [6,7,2,1,9,5,3,4,8],
            [1,9,8,3,4,2,5,6,7],
            [8,5,9,7,6,1,4,2,3],
            [4,2,6,8,5,3,7,9,1],
            [7,1,3,9,2,4,8,5,6],
            [9,6,1,5,3,7,2,8,4],
            [2,8,7,4,1,9,6,3,5],
            [3,4,5,2,8,6,1,7,9]]

res = sudoku(puzzle)
assert res == solution


#////////////////////---------------------------------------------best


from itertools import product

def possibles(puzzle, x, y):
    a, b = 3*(x/3), 3*(y/3)
    square = set([puzzle[r][c] for r, c in product(range(a,a + 3), range(b,b + 3))])
    row = set(puzzle[x])
    col = set(zip(*puzzle)[y])
    return set(range(1,10)).difference(square.union(row).union(col))

def sudoku(puzzle):
    z = [(r,c) for (r,c) in product(range(9),range(9)) if puzzle[r][c] == 0]
    if z == []:
        return puzzle
    for (r,c) in z:
        p = possibles(puzzle, r, c)
        if len(p) == 1:
            puzzle[r][c] = p.pop()
    return sudoku(puzzle)