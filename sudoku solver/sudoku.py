def find_next_empty(puzzle):
    # finds the next row, col on the puzzle that's not filled yet --> rep with -1
    # return rol, col tuple (or (None, None))
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == - 1:
                return r, c

    return None, None # when there's no spaces left

def is_valid(puzzle, guess, row, col):
    # figures out whether the guess at the row/col of the puzzle is a valid guess
    # check row:
    row_vals = puzzle[row]
    if guess in row_vals:
        return False

    # check col:
    # col_vals = []
    # for i in range(9):
    #     col.vals.append(puzzle[i][col])
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    # check 3x3 squares
    # check where the 3x3 square starts and iterate over the 3 values in the row/col
    row_start = (row // 3) * 3 # 0, 3, 6
    col_start = (col // 3) * 3

    for r in range(row_start, row_start+3):
        for c in range(col_start, col_start+3):
            if puzzle[r][c] == guess:
                return False
    
    # if we get here, these checks pass
    return True

def solve_sudoku(puzzle):
    # solves sudoku using backtracking
    # our puzzle is a list of lists, each inner list is a row
    # returns whether a solution exists
    # mutates puzzle to be the solution (if solution exists)

    # 1: choose somewhere on the puzzle to make a guess
    row, col = find_next_empty(puzzle)

    # 1a: if there's nowhere left, then we're done because we've only allowed valid inputs
    if row is None:
        return True
    
    # 2: if there is a place to put a number, then make a guess between 1 - 9
    for guess in range(1, 10): 
        # 3: check if this is a valid guess
        if is_valid(puzzle, guess, row, col):
            # 3a: if valid, then place guess on the puzzle by mutating
            puzzle[row][col] = guess
            # 4: recursively call our function
            if solve_sudoku(puzzle):
                return True
            
        # 5: if not valid OR if our guess does not solve the puzzle, then backtrack
        puzzle[row][col] = -1 # reset the guess
    
    # 6: none of the numbers we've tried work, unsolvable puzzle
    return False

if __name__ == '__main__':
    example_board = [
        [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [6, 7, -1,   1, -1, 5,   -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    ]
    print(solve_sudoku(example_board))
    print(example_board)