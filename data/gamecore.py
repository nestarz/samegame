#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import *
from copy import *


class Color:
    """
    Color Class
    """

    def __init__(self, color, name):
        self.color = color
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.color


class GameCore:
    """
    The heart of the game, you set the speed, the number of color, the number of row
    number of col, and the number of board here

    All the board are stocked in the array : boards
    """

    def __init__(
        self,
        speed=1,
        num_color=6,
        num_row=10,
        num_col=10
        ):
        super().__init__()
        self.num_col = num_col
        self.num_row = num_row
        self.num_color = num_color
        self.speed = speed
        self.boards = []

    def generate_board(self):
        """ Generate new board, stock and return it """
        board = Board(self.speed, self.num_color, self.num_row, self.num_col)
        self.boards.append(board)
        return board

    def num_board(self):
        return len(self.boards)

class Board:
    """
    Board Class, all method are explained in help(Board)
    """

    def __init__(
        self,
        speed=1,
        num_color=6,
        num_row=10,
        num_col=6,
        ):
        """
        Create a playable board

        Set the speed, the number of color, number of row etc...
        Call the generate_board function
        Apply gravity
        Create the cursor
        """
        self.speed = speed  # game's speed, int, the higher, the faster
        self.pause = 0   #amount of time during which the game is frozen after a combo
        #               (i.e the board isn't going upward)
        self.num_color = num_color  # the number of color used in the game
        self.num_col = num_col  # width of the board
        self.num_row = num_row  # length of the board
        self.size = (self.num_row, self.num_col)
        self.destroy = []
        self.color = [  # VALUES MUST BE IN THE CONSTANTS COLORS_DICT!!
            'blue',
            'green',
            'orange',
            'grey',
            'purple',
            'yellow',
            ]
        self.board = []
        self.generate_board()
        self.gravity()
        self.cursor = Cursor(num_row, num_col)

    def generate_board(self):
        """Generate a board, of num_col*num_row case, filled with 24 colored case, rest is set to False
        6 different color by default

        row index start at 1 because we need a 'hidden' row

        board[1][0] is bottom left, board[1][num_col-1] is bottom right
        board[num_row-1][0] is top left, board[num_row-1][num_col-1] is top right
        """

        for row in range(self.num_row):
            self.board.append([])
            for col in range(self.num_col):
                self.board[row].append(Case(False,False,False, self.board))

        i = 0

        while i < (self.num_col - 1) * self.num_row / 2:
            row = randrange(1, self.num_row)
            col = randrange(0, self.num_col)

            if self.board[row][col].color is False:
                self.board[row][col].color = self.color[randrange(0,
                        self.num_color)]
                i += 1

        self.generate_hidden()
        self.gravity()

    def __str__(self):
        case_length = len(max(self.color))
        a = '*'+ '-' * (case_length + 1) * self.num_col + '*\n'
        string = ''

        for row in reversed(range(self.num_row)):
            string += a
            for col in range(self.num_col):
                string += '|'
                if self.board[row][col].color is False:
                    string += ' ' * case_length
                else:
                    color = str(self.board[row][col].color)
                    string += (color + ' ' * (case_length
                               - len(color)) if len(color)
                               < case_length else color[:case_length])
            string += '| \n'
        string += a

        return string
        # return(str(self.board))

    def top_row_empty(self):
        """
        Check if the top line is empty case by case, return True if the top line is empty, False elsewise
        """
        return not(True in [isinstance(x.color,str) for x in self.board[self.num_row-1]])

    def up(self):
        """
        All rows are going upward, and generate a new hidden line
        """
        for row in reversed(range(1,(self.num_row))):
            for col in range(self.num_col):
                self.board[row][col] = self.board[row-1][col]
        self.generate_hidden()


    def check_destroy(self):
        """
        The function check if at least 3 block are lined vertically or horizontally (no diagonal)
        destroy them if so
        """

        destroy = []

        def destroy_local(self, combo, row, col, temp_case, temp_cor, destroy):
            """
            Function called by destroy_block
            Check if the actual case is relevant to the precedent case :
            If so : increment combo
            If not : Destroy case if combo is >= 3  and reset combo

            Return the number of destroyed cases
            """

            if self.board[row][col].color:
                if self.board[row][col].color == temp_case:
                    combo += 1
                    temp_cor.append((row, col))
                else:
                    if combo >= 3:
                        destroy.append(temp_cor)

                    temp_cor = [(row, col)]
                    combo = 1
                    temp_case = self.board[row][col].color

            else:
                if combo >= 3:
                    destroy.append(temp_cor)

                combo = 1
                temp_core = [(row, col)]
                temp_case = False

            return(combo, temp_case, temp_cor, destroy)

        for row in reversed(range(1, self.num_row)):  # check per line
            combo = 1
            temp_case = False
            temp_cor = []

            for col in range(self.num_col):
                combo, temp_case, temp_cor, destroy = destroy_local(
                    self, combo, row, col, temp_case, temp_cor, destroy)

            if combo >= 3:
                destroy.append(temp_cor)

        for col in range(self.num_col):  # check per column
            combo = 1
            temp_col = False
            temp_cor = []


            for row in reversed(range(1, self.num_row)):
                combo, temp_case, temp_cor, destroy = destroy_local(
                    self, combo, row, col, temp_case, temp_cor, destroy)

            if combo >= 3:
                destroy.append(temp_cor)

        self.destroy = destroy
        return len(destroy) > 1

    def destroy_block(self):
        combo = 0
        for line in self.destroy:
            for case in line:
                if not self.board[case[0]][case[1]].color == 'bad':
                    self.board[case[0]][case[1]] = Case(False,False,False, self.board)
                    combo += 1
        self.destroy = []

        return combo

    def gravity(self):
        """
        Makes sure there is no empty space between a case and the bottom
        Bad Blocks works as unit of singles cases, so they don't fall if all cases under them are free

        The function works in 2 parts :
            - Apply gravity on everything, even bad block (which is separated piece by piece during this
            step)
            - Get the back block back together

        This way you get the nice illusion that the block is a unit
        So, the block won't fall unless all the case under his components are empty
        """

        def local_check(self):
            """
            The goal of this function is to get back all part of the bad block together

            You do this by checking if there is an other part of the bad block on his left (prev)
            or on his right (next)

            If the part on the left or right is missing, you send the column upward and you re-iterate
            through the board

            """
            if self.board[row][col].color == 'bad':
                    if (self.board[row][col].nex and not(self.board[row][col+1].color == 'bad') \
                    or self.board[row][col].prev and not(self.board[row][col-1].color == 'bad')):
                            for temp_row in reversed(range(row,self.num_row)):
                                self.board[temp_row][col] = copy(self.board[temp_row-1][col])
                            self.board[row][col] = Case(False,False,False, self.board)


        for col in range(self.num_col):  #First Routine, Makes everything fall down even Bad block
                row = 1                  #Bad block are separated
                i = 1
                done = False
                while row < self.num_row:
                    if self.board[row][col].color is False:
                        done = True
                    elif done is True:
                        self.board[i][col] = self.board[row][col]
                        self.board[row][col] = Case(False,False,False, self.board)
                        i += 1
                    else:
                        i += 1
                    row += 1


        for row in range(1,self.num_row):      #Get the bad blocks together
            for col in range(self.num_col):
                local_check(self)
            for col in reversed(range(self.num_col)):
                local_check(self)

    def can_fall(self,row,col):
        """
        Check if a case/block can fall one row down, need to have an empty space between all his case
        """
        Done = False
        while not Done:
            if self.board[row-1][col].color:
                return False
            elif self.board[row][col].nex:
                col += 1
            else:
                Done = True
        return True


    def generate_bad_block(self, pos, size):
        """
        Create a 'blocker' case, suppose to bother you during the game
        """

        for i in range(0,size):
            self.board[self.num_row-1][pos+i] = Case('bad',i!=0,i!=size-1, self.board)



    def generate_hidden(self):
        """
        Fill the first row with colored cases
        """

        for i in range(0, self.num_col):
            self.board[0][i] = Case(self.color[randrange(0, self.num_color)], False,False, self.board)
        return self.board[0]

    def swap(self):
        """
        Swap the actual case, pointed by cursor, with the one on his right
        since you can only swap a case with the one on his right
        """
        if self.board[self.cursor.pos_row][self.cursor.pos_col].can_swap \
           and self.board[self.cursor.pos_row][self.cursor.pos_col+1].can_swap:
            (self.board[self.cursor.pos_row][self.cursor.pos_col],
             self.board[self.cursor.pos_row][self.cursor.pos_col + 1]) = \
                (self.board[self.cursor.pos_row][self.cursor.pos_col + 1],
                 self.board[self.cursor.pos_row][self.cursor.pos_col])
            return (self.board[self.cursor.pos_row][self.cursor.pos_col],
                    self.board[self.cursor.pos_row][self.cursor.pos_col + 1])
        else:
            print("Can't swap those cases")


class Cursor:
    """
    The cursor is an object that focuses two cases, in order to swap them
    Create a cursor that point only one case, no need to specify the 2nd case since it's the one its right
    You can use .move_up, .move_down, .move_left, .move_right
    """

    def __init__(self, num_row, num_col):
        self.max_row = num_row - 1
        self.max_col = num_col - 1
        self.pos_row = 1
        self.pos_col = 0

    def move_up(self):
        if self.pos_row + 1 <= self.max_row:
            self.pos_row += 1
        else:
            print("Can't move up")

    def move_down(self):
        if self.pos_row - 1 > 0:
            self.pos_row -= 1
        else:
            print("Can't move down")

    def move_left(self):
        if self.pos_col - 1 >= 0:
            self.pos_col -= 1
        else:
            print("Can't move left")

    def move_right(self):
        if self.pos_col < self.max_col - 1:
            self.pos_col += 1
        else:
            print("Can't move right")


class Case:
    """
    Case Class
    """
    def __init__(self, color, prev, nex, board):
        self.color = color
        self.nex = nex
        self.prev = prev
        self.board = board
        self.swap_ongoing = False
        if color == 'bad':
            self.can_swap = False
        else:
            self.can_swap = True

    @property
    def pos(self):
        return find(self, self.board)

    def __repr__(self):
        return "Prev = %r, Next = %r, Color is %r" % (self.prev,self.nex,self.color)

def find(c, board):
    for i, case in enumerate(board):
        try:
            j = case.index(c)
        except ValueError:
            continue
        return i, j
