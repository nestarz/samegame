#!/bin/python3

import pygame as pg
from . import cache
from . import constants as ct
from . import tools as t

class MainMenu(t.State):
    def __init__(self):
        super().__init__()
        self.name = 'home'
        self.buttons = list()
        self.bg = None
        self.__arrow_index = 0
        self.allow_input = False
        self.next = 'main_menu'

    def start(self):
        self.setup_background()
        self.setup_buttons()

    def setup_background(self):
        bg_img = cache._cache.images[self.name]
        self.bg = t.Background(bg_img)
        self.bg.resize(*ct.SCREEN_SIZE)

    def setup_buttons(self):
        text1 = 'START'
        text2 = 'QUIT '
        dest = (470,265)
        DO_START = lambda : setattr(self, 'done', True)
        DO_QUIT = lambda : setattr(self, 'quit', True)
        self.buttons.append(
            t.Button(text1, (15,36), DO_START, dest))
        self.buttons.append(
            t.Button(text2, (15,36), DO_QUIT, (dest[0], dest[1]+30)))

    def check_for_input(self, keys):
        if self.allow_input:
            if keys[pg.K_UP]:
                self.arrow_index -= 1
                if self.arrow_index == 0:
                    self.arrow_index = 2
            elif keys[pg.K_DOWN]:
                self.arrow_index += 1
                if self.arrow_index == 3:
                    self.arrow_index = 0
            elif keys[pg.K_RETURN] or keys[pg.K_SPACE]:
                self.do_action(self.arrow_index)
        self.allow_input = False
        if (not keys[pg.K_DOWN]
            and not keys[pg.K_UP]
            and not keys[pg.K_RETURN]
            and not keys[pg.K_SPACE]):
                self.allow_input = True

    def do_action(self, index):
        if index-1 in range(0, t.Button.INDEX+1):
            self.buttons[index-1].callback()

    def update(self, window, keys):
        self.check_for_input(keys)
        window.blit(self.bg.surface, (0,0))
        for button in self.buttons:
            button.update(self.arrow_index)
            window.blit(button.surface, button.dest)

    @property
    def arrow_index(self):
        return self.__arrow_index

    @arrow_index.setter
    def arrow_index(self, value):
        """On cap l'index du curseur au nombre de choix"""
        if value in range(0,4):
            self.__arrow_index = value
