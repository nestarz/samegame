#!/bin/python3

import pygame
import pygame.locals as pg
from . import constants as c
import os
import sys


class Window():

    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.caption = c.NAME
        self.surface = pygame.display.set_mode(c.SCREEN_SIZE, pg.DOUBLEBUF)
        pygame.display.set_caption(self.caption)
        self.screen = pygame.display.get_surface()

    def exit(self):
        pygame.quit()
        sys.exit()
