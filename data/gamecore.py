#!/bin/python3

from random import *

class GameCore:
    """The heart of the game, at the moment, it only generates 1 board, but later, will generate 2 or more board, if you wish"""
    def __init__(self,speed=1,num_color=6,size_x=6,size_y=9, num_board=1): #need getter, setter, later.
        all_board = []
        for i in range(0,num_board):
            all_board.append(Board(speed, num_color, size_x, size_y))
            

    

class Board:

    def __init__(self,speed=1,num_color=6,size_col=6,size_row=9):  #need getter, setter, later.
        self.speed = speed  #game's speed, int, the higher, the faster
        self.num_color = num_color #the number of color used in the game
        self.size_col = size_col #width of the board
        self.size_row = size_row #length of the board
        self.color = ['blu','gre','bla','red','pin','yel']
        self.board = []
        self.generate_board()

        
    def generate_board(self):
        """Generate a board, of size_col*size_row case, filled with 24 colored case, rest is set to 0
        6 different color by default
        y index start at 1 because we need a 'hidden' row

        board[0][1] is bottom left, board[size_x][1] is bottom right
        board[0][size_y] is top left, board[size_x][size_y] is top right 
        """
        for row in range(self.size_row):
            self.board.append([])
            for col in range(self.size_col):
                self.board[row].append('000')

        for i in range(0,24):
            row = randrange(1,self.size_row)
            col = randrange(0,self.size_col)
            self.board[row][col] = self.color[randrange(0,self.num_color)]
                
    def __str__(self):

        ##return(str(self.board))

        a = "*---"*self.size_col+"*\n"
        string = ''
        
        for row in reversed(range(self.size_row)):
            string += a
            for col in (range(self.size_col)):
                string += "|"+str(self.board[row][col])
            string += "| \n"
        string += a

        return(string)
        
        
        

    def update_board(self):
        pass
                

    def generate_hidden(self):
        """generate the hidden row"""
        for i in range(0, size_x):
            self.board[i][0] = self.color[randrange(0,self.num_color)]
        
        
    def swap(self, case1, case2):
        pass


class Case():
    """may be useless, need to see"""
    
    def __init__(self):  #need getter, setter
        self.color = color



        
