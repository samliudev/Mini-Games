import random
import re

# create a board object to represent the minesweeper game
# this is here so we can "create a new board object" or "dig here" or "render this game for this object"

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create board
        self.board = self.make_new_board()
        self.assign_values_to_board()
        
        # row col tuples
        self.dug = set() # if we dig at 0,0, self.dug = {(0,0)}

    def make_new_board(self):
        # makes a new board based on dim size and num bombs
        # we should contrust the list of lists here for a 2D board

        # generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # Creates an array like this:
        #[[None, None, ..., None].
        # [None, None, ..., None],
        # ...
        # [None, None, ..., None]]

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1) # a random int that represents a space on the board
            row = loc // self.dim_size # how many times dim_size goes into loc
            col = loc % self.dim_size # remainder is the index in that row

            if board[row][col] == '*':
                # we've already planted a bomb there
                continue
            
            board[row][col] = '*'
            bombs_planted += 1

        return board
    
    def assign_values_to_board(self):
        # bombs have been planted, now assign a number 0 - 8 for all the empty spaces that
        # represents how many neighboring bombs there are. We can precompute these and it'll save us
        # effort checking what's around the board later on
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue # already a bomb
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size - 1, row+1) + 1):
            for c in range(max(0, col-1), min(self.dim_size - 1, col+1) + 1):
                if r == row and c == col:
                    continue # this is our original location
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def dig(self, row, col):
        # true if successful dig, false if bomb dug
        self.dug.add((row, col)) # tuple to keep track of where we've dug
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0 
        for r in range(max(0, row-1), min(self.dim_size - 1, row+1) + 1):
            for c in range(max(0, col-1), min(self.dim_size - 1, col+1) + 1):
                if (r, c) in self.dug:
                    continue # we've already dug here
                self.dig(r, c)
        return True # keeps diggin while board = 0

    def __str__(self): # returns a str representation of an object
        # magic function where if you call print on this object, it'll print out what
        # this function returns
        # returns a string that shows the board to the player
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col]) 
                else:
                    visible_board[row][col] = ' ' # haven't dug here yet

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

def play(dim_size = 10, num_bombs = 10): 
    # 1: Create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # 2: Show the user the board and ask for where they want to dig
    # 3a: if location is bomb, game over
    # 3b: if location is not a bomb, dig recursively until each square is at least next to a bomb
    # 4: repeat 2 and 3a/b until there are no more places to dig => Victory!
    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs: # still have empty, non-bomb spaces
        print(board)
        # , check for commas, (\\s) check for empty space, * is 0 or more of those
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row, col: ")) # '0, 3' or '0,    0'
        row, col = int(user_input[0]), int(user_input[-1]) # re.split sometimes has some fluff, this takes last item
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again. ")
            continue

        # if it's valid, we dig and returns True/False
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb
            break

    # 2 ways to end loop, no more bombs or you hit a bomb
    if safe:
        print("CONGRATULATIONS!!!!! YOU ARE VICTORIOUS!")
    else:
        print("SORRY GAME OVER :(")
        # reveal the whole board!
        # this takes every possible (r,c) value and puts it into this list
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__':
    play()

