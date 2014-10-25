#!/bin/python3

import pygame as pg
from . import cache
from . import constants as ct
from . import tools as t

class Party(t.State):
    def __init__(self):
        super().__init__()
        self.name = 'party'
        self.buttons = list()
        self.bg = None
        self.__arrow_index = 0
        self.allow_input = False
        self.k_return = False
        self.next = 'party'
        self.start()

    def start(self):
        self.setup_background()
        self.setup_buttons()

    def setup_background(self):
        bg_img = cache._cache.images[self.name]
        self.bg = t.Background(bg_img)
        self.bg.resize(*ct.SCREEN_SIZE)

    def setup_buttons(self):
        pass

    def check_for_input(self, keys):
        pass

    def update(self, window, keys):
        window.blit(self.bg.surface, (0,0))

