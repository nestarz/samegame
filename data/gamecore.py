#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import *
from copy import *


class Color:

    def __init__(self, color, name):
        self.color = color
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.color


class GameCore:

    """The heart of the game, at the moment, it only generates 1 board, but later, will generate 2 or more board, if you wish"""

    def __init__(  # need getter, setter, later.
        self,
        speed=1,
        num_color=6,
        num_row=10,
        num_col=10,
        num_board=2,
        ):
        super().__init__()
        self.all_board = []
        for i in range(0, num_board):
            self.all_board.append(Board(speed, num_color, num_row,
                                  num_col))


class Board:

    def __init__(  # need getter, setter, later.
        self,
        speed=1,
        num_color=6,
        num_row=10,
        num_col=6,
        ):
        self.speed = speed  # game's speed, int, the higher, the faster
        self.num_color = num_color  # the number of color used in the game
        self.num_col = num_col  # width of the board
        self.num_row = num_row  # length of the board
        self.size = (self.num_row, self.num_col)
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

        board[1][0] is bottom left, board[1][num_col] is bottom right
        board[num_row][0] is top left, board[num_row][num_col] is top right
        """

        for row in range(self.num_row):
            self.board.append([])
            for col in range(self.num_col):
                self.board[row].append(False)

        i = 0

        while i < (self.num_col - 1) * self.num_row / 2:
            row = randrange(1, self.num_row)
            col = randrange(0, self.num_col)

            if self.board[row][col] is False:
                self.board[row][col] = self.color[randrange(0,
                        self.num_color)]
                i += 1

        self.generate_hidden()
        self.gravity()

    def __str__(self):
        case_length = len(max(self.color))
        a = '-' * (case_length + 1) * self.num_col + '*\n'
        string = ''

        for row in reversed(range(self.num_row)):
            string += a
            for col in range(self.num_col):
                string += '|'
                if self.board[row][col] is False:
                    string += ' ' * case_length
                else:
                    color = str(self.board[row][col])
                    string += (color + ' ' * (case_length
                               - len(color)) if len(color)
                               < case_length else color[:case_length])
            string += '| \n'
        string += a

        return string

        # return(str(self.board))

    def update_board(self):
        pass

    def destroy_block(self):  # ultra ugly, need one loop to do all work instead of 2 look-alike
        """
        The function check if at least 3 block are lined vertically or horizontally (no diagonal), destroy them if so
        """

        destroy = []

        def destroy_local(self, combo, row, col, temp_case, temp_cor, destroy):

            if self.board[row][col]:
                if self.board[row][col] == temp_case:
                    combo += 1
                    temp_cor.append((row, col))
                else:
                    if combo >= 3:
                        destroy.append(temp_cor)

                    temp_cor = [(row, col)]
                    combo = 1
                    temp_case = self.board[row][col]

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

        for line in destroy:
            for case in line:
                self.board[case[0]][case[1]] = False

    def gravity(self):
        """Makes sure there is no empty space between a case and the bottom"""

        for col in range(self.num_col):
            row = 1
            i = 1
            done = False
            while row < self.num_row:
                if self.board[row][col] is False:
                    done = True
                elif done is True:
                    self.board[i][col] = self.board[row][col]
                    self.board[row][col] = False
                    i += 1
                else:
                    i += 1
                row += 1

    def generate_hidden(self):
        """generate the hidden row"""

        for i in range(0, self.num_col):
            self.board[0][i] = self.color[randrange(0, self.num_color)]

    def swap(self):
        """Swap the actual case, pointed by cursor, with the one on his right, since you can only swap a case with the one on his right"""

        (self.board[self.cursor.pos_row][self.cursor.pos_col],
         self.board[self.cursor.pos_row][self.cursor.pos_col + 1]) = \
            (self.board[self.cursor.pos_row][self.cursor.pos_col + 1],
             self.board[self.cursor.pos_row][self.cursor.pos_col])


class Cursor:

    """The cursor is an object that focuses two cases, in order to swap them
        Create a cursor that point only one case, no need to specify the 2nd case since it's the one its right
        You can use .move_up, .move_down, .move_left, .move_right"""

    def __init__(self, num_row, num_col):  # find it ugly to push parameters that already exist everywhere, num_row, num_col, need better solution
        self.max_row = num_row - 1
        self.max_col = num_col - 1
        self.pos_row = 0
        self.pos_col = 0

    def move_up(self):
        if self.pos_row + 1 <= self.max_row:
            self.pos_row += 1
        else:
            print("Can't move up")

    def move_down(self):
        if self.pos_row - 1 >= 0:
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

    """may be useless, need to see, MAYBE    Will be used to create bad giant block in versus mode"""

    def __init__(self):
        self.color = color



			
