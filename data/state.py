#!/bin/python3

import pygame as pg
from . import cache
from . import constants as ct

class State():
    def __init__(self):
        self.done = False
        self.quit = False

class HomeScreen(State):
    def __init__(self):
        State.__init__(self)
        self.buttons = list()
        self.bg = None
        self.start()

    def start(self):
        self.setup_background()
        self.setup_buttons()

    def setup_background(self):
        bg_img = cache._cache.images['home screen']
        self.bg = Background(bg_img)
        self.bg.resize(1024, 574)

    def setup_buttons(self):
        self.buttons.append(Button('[S]START', (15,36), (25,475)))
        self.buttons.append(Button('[Q]QUIT', (15,36), (25,500)))

    def update(self, window):
        #shitty code - debug only
        window.blit(self.bg.surface, (0,0))
        b = []
        for button in self.buttons:
            b.append(window.blit(button.rtext, button.dest))
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    if b[-1].collidepoint(pos):
                        self.done = True
        #endofshittycode


class Background():
    def __init__(self, surface):
        self.surface = surface
        self.rect = surface.get_rect()
        self.h = self.rect.height
        self.w = self.rect.width

    def resize(self, w, h):
        self.surface = pg.transform.scale(self.surface,(int(w),int(h)))

class Button(pg.sprite.Sprite):
    def __init__(self, text, size, dest=(0,0), style='default'):
        super().__init__()
        self.dest = dest
        self.rect = pg.Rect(0, 0, size[0], size[1])
        self.size = size
        self.text = text
        self.style = ct.BUTTON_STYLE.get(style, 'default')
        self.font = Font(self.style['fontname'], self.style['fontsize'])
        self.rtext = self.font.render(
            text, 1, self.style['default']['text_color'])

class Font(pg.font.Font):
    def __init__(self, name, size):
        self.name = name
        self.size = size
        super().__init__(cache._cache.fonts.get(name, pg.font.get_default_font()),
            size)

class CustomButton(Button):
    def __init__(self, text, customstyle):
        super().__init__(text)
