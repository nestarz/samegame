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

        
    def generate_board(self):
        """Generate a board, of num_col*num_row case, filled with 24 colored case, rest is set to False
        6 different color by default
        y index start at 1 because we need a 'hidden' row

        board[0][1] is bottom left, board[size_x][1] is bottom right
        board[0][size_y] is top left, board[size_x][size_y] is top right 
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
        
        
    def swap(self,row,col):
        """Swap the actual case with the one on his right, since you can only swap a case with the one on his right, you only need 2 param, his row and column"""

        self.board[row][col], self.board[row][col+1] = self.board[row][col+1], self.board[row][col]


class Case():
    """may be useless, need to see     Will be used to create 'BAD' block in versus mode"""
    
    def __init__(self):  #need getter, setter
        self.color = color


