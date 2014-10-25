#!/bin/python3

import pygame as pg
from . import cache
from . import constants as ct

class State():
    def __init__(self):
        self.done = False
        self.quit = False

    def reinitialize(self):
        self.done = False

class Background():
    def __init__(self, surface):
        self.surface = surface
        self.rect = surface.get_rect()
        self.h = self.rect.height
        self.w = self.rect.width

    def resize(self, w, h):
        self.surface = pg.transform.scale(self.surface,(int(w),int(h)))

class Button(pg.sprite.Sprite):
    INDEX = 0
    def __init__(self, text, size, callback=None, dest=(0,0), style='default'):
        Button.INDEX += 1
        self.index = Button.INDEX
        super().__init__()
        self.dest = dest
        self.rect = pg.Rect(0, 0, size[0], size[1])
        self.size = size
        self.text = text
        self.style = ct.BUTTON_STYLE.get(style, 'default')
        self.font = Font(self.style['fontname'], self.style['fontsize'])
        self.surface = self.font.render(
            text, 1, self.style['default']['text_color'])
        self.callback = callback

    def update(self, index):
        if index == self.index:
            text = self.text + ' *'
            self.surface = self.font.render(
            text, 1, self.style['hover']['text_color'])
        else:
            self.surface = self.font.render(
            self.text, 1, self.style['default']['text_color'])

class Font(pg.font.Font):
    def __init__(self, name, size):
        self.name = name
        self.size = size
        super().__init__(cache._cache.fonts.get(name, pg.font.get_default_font()),
            size)

class CustomButton(Button):
    def __init__(self, text, customstyle):
        super().__init__(text)
