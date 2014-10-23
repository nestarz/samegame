#!/bin/python3

import pygame
import pygame.locals as pg

NAME = "SAMEGAME"

class Window():
    def __init__(self):
        pygame.init()
        self.caption =  NAME
        self.surface = pygame.display.set_mode((1024, 574), pg.DOUBLEBUF)
        pygame.display.set_caption(NAME)
        self.screen = pg.display.get_surface()
