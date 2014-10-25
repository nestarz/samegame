#!/bin/python3

import pygame
import pygame.locals as pg
from . import constants as ct
import os
import sys

class Window():
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.caption =  ct.NAME
        self.surface = pygame.display.set_mode(ct.SCREEN_SIZE, pg.DOUBLEBUF)
        pygame.display.set_caption(ct.NAME)
        self.screen = pygame.display.get_surface()

    def exit(self):
        pygame.quit()
        sys.exit()