#!/bin/python3

import pygame as pg
from . import cache
from . import constants as ct
from . import tools as t


class GameCore(speed, num_color=6, size_x=4, size_y=9):

    def __init__(self):  #need getter, setter, later.
        self.speed = speed  #game's speed, int, the higher, the faster
        self.num_color = num_color #the number of color used in the game
        self.size_x = size_x #width of the board
        self.size_y = size_y #length of the board
        self.board = []

    def generate_board(self): #24 case full, rest empty
        for i in range(0,size_y + 5):
            for j in range(0,size_x):
                pass

    def swap(self, case1, case2):
        pass


class case(color):

    def __init__(self):  #need getter, setter
        self.color = color
        
