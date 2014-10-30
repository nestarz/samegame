#!/bin/python3

from random import *

class GameCore:
    """The heart of the game, at the moment, it only generates 1 board, but later, will generate 2 or more board, if you wish"""
    def __init__(self,speed=1,num_color=6,num_row=10,num_col=6, num_board=1): #need getter, setter, later.
        all_board = []
        for i in range(0,num_board):
            all_board.append(Board(speed, num_color, num_row, num_col))
            

class Board:

    def __init__(self,speed=1,num_color=6,num_row=10,num_col=6):  #need getter, setter, later.
        self.speed = speed  #game's speed, int, the higher, the faster
        self.num_color = num_color #the number of color used in the game
        self.num_col = num_col #width of the board
        self.num_row = num_row #length of the board
        self.color = ['blu','gre','bla','red','pin','yel']
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

        while i < 24:
            row = randrange(1,self.num_row)
            col = randrange(0,self.num_col)

            if self.board[row][col] is False:
                self.board[row][col] = self.color[randrange(0,self.num_color)]
                i += 1

        self.generate_hidden()
        self.gravity()
                
    def __str__(self):
        a = "*---"*self.num_col+"*\n"
        string = ''
        
        for row in reversed(range(self.num_row)):
            string += a
            for col in range(self.num_col):
                string += "|"
                if self.board[row][col] is False:
                    string += '   '
                else:
                    string += str(self.board[row][col])
            string += "| \n"
        string += a

        return(string)
        
        #return(str(self.board))
        
    def update_board(self):
        pass

    def gravity(self):
        """Makes sure there is no empty space between a case and the bottom"""

        for col in range(self.num_col):
            row = 1
            i = 1
            done = False
            while row < self.num_row:
                if self.board[row][col] is False:
                    done = True
                elif done is True :
                    self.board[i][col] = self.board[row][col]
                    self.board[row][col] = False
                    i += 1
                else:
                    i +=1
                row += 1

    def generate_hidden(self):
        """generate the hidden row"""

        for i in range(0,self.num_col):
            self.board[0][i] = self.color[randrange(0,self.num_color)]
        
        
    def swap(self):
        """Swap the actual case, pointed by cursor, with the one on his right, since you can only swap a case with the one on his right"""

        self.board[self.cursor.pos_row][self.cursor.pos_col], self.board[self.cursor.pos_row][self.cursor.pos_col+1]\
        = self.board[self.cursor.pos_row][self.cursor.pos_col+1], self.board[self.cursor.pos_row][self.cursor.pos_col]

class Cursor():
    """The cursor is an object that focuses two cases, in order to swap them
        Create a cursor that point only one case, no need to specify the 2nd case since it's the one its right
        You can use .move_up, .move_down, .move_left, .move_right"""

    def __init__(self, num_row, num_col): #find it ugly to push parameters that already exist everywhere, num_row, num_col, need better solution
        self.max_row = num_row
        self.max_col = num_col-1
        self.pos_row = 1
        self.pos_col = 0
        
    def move_up(self):
        if self.pos_row+1 <= self.max_row:
            self.pos_row += 1
        else:
            print("Can't move up")
            
    def move_down(self):
        if self.pos_row-1 >= 1:
            self.pos_row -= 1
        else:
            print("Can't move down")
            
    def move_left(self):
        if self.pos_col-1 >= 0:
            self.pos_col -= 1
        else:
            print("Can't move left")
        
    def move_right(self):
        if self.pos_col+1 <= max_col:
            self.pos_col += 1
        else:
            print("Can't move right")


class Case():
    """may be useless, need to see, MAYBE    Will be used to create bad giant block in versus mode"""
    
    def __init__(self):
        self.color = color