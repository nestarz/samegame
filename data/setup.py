#!/bin/python3

import pygame
import pygame.locals as pg
import os

NAME = "SAMEGAME"

class Window():
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.caption =  NAME
        self.surface = pygame.display.set_mode((1024, 574), pg.DOUBLEBUF)
        pygame.display.set_caption(NAME)
        self.screen = pygame.display.get_surface()
