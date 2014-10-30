#!/bin/python3

import pygame as pg
from . import cache
from . import constants as ct
from . import tools as t

class Home(t.State):
    def __init__(self):
        super().__init__()
        self.name = 'home'
        self.buttons, self.images = dict(), dict()
        self.bg = None
        self.allow_input = False
        self.next = 'main_menu'

    def start(self, screen):
        self.setup_background(screen)
        self.setup_buttons(screen)
        self.setup_images(screen)

    def setup_background(self, screen):
        bg_img = cache._cache.images[self.name]
        self.bg = t.Image(bg_img, screen)
        self.bg.resize(*ct.SCREEN_SIZE)

    def setup_buttons(self, screen):
        pass

    def setup_images(self, screen):
        logo_img = t.Image(cache._cache.images['logo'], screen)
        logo_img.setup_effect(ct.EFFECT['moveup25'], ct.EFFECT['shake50'])
        logo_img.center(screen)
        sublogo_img = t.Image(t.text_to_surface(ct.AUTHOR, 'joystix', 10, ct.WHITE_RGB), screen)
        sublogo_img.setup_effect(ct.EFFECT['fadein100'], ct.EFFECT['wait25'])
        sublogo_img.center(screen, 0, 35)

        text1 = 'Press Start Button'
        start_img = t.Image(t.text_to_surface(text1, 'joystix', 10, ct.WHITE_RGB), screen)
        start_img.setup_effect(ct.EFFECT['blink'], ct.EFFECT['wait50'])
        start_img.center(screen, 0, 220)

        self.images['start'] = start_img
        self.images['logo'] = logo_img
        self.images['sublogo'] = sublogo_img

    def check_for_input(self, keys):
        if self.allow_input:
            if keys[pg.K_RETURN]:
                self.done = True
        self.allow_input = False
        if (not keys[pg.K_RETURN]):
                self.allow_input = True

    def update(self, window, keys):
        self.check_for_input(keys)
        images = list()
        images.append(self.bg)
        images.extend(list(self.images.values()))
        for img in images:
            img.update()
