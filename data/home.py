#!/bin/python3

import pygame as pg
from . import cache
from . import constants as c
from . import tools as t

class Home(t.Screen):
    """ Enfant de l'objet State """
    def __init__(self):
        super().__init__()
        self.name = c.HOME
        self.next = c.MAIN_MENU

    def setup_images(self, screen):
        logo_img = t.Image(cache._cache.images['logo'], screen)
        logo_img.setup_effect('move', 25, c.UP)
        logo_img.setup_effect('fadein1', 50)
        logo_img.center(screen, 0, -5)

        sublogo_img = t.Image(t.text_to_surface(c.AUTHOR, 'joystix', 10, c.WHITE_RGB), screen)
        sublogo_img.setup_effect('wait', 25)
        sublogo_img.setup_effect('fadein1', 50, True)
        sublogo_img.center(screen, 0, 30)

        text1 = 'Press Start Button'
        img = t.Image(t.text_to_surface(text1, 'joystix', 20, c.WHITE_RGB), screen)
        start_img = pg.Surface(img.surface.get_size(), pg.SRCALPHA)
        start_img.fill((0,0,0,255))
        start_img.blit(img.surface, img.rect)
        start_img = t.Image(start_img, screen)
        start_img.setup_effect('blink', 15)
        start_img.setup_effect('wait', 70)
        start_img.center(screen, 0, 220)

        self.images['start'] = start_img
        self.images['logo'] = logo_img
        self.images['sublogo'] = sublogo_img

    def set_done(self, next):
        super().set_done(next)
        self.to_set_done = 10
        self.bg.setup_effect('fadeout', 50)

    def check_for_input(self, keys):
        self.allow_input_timer += 1
        if self.allow_input:
            if keys[pg.K_RETURN]:
                self.allow_input_timer = 0
                self.set_done(self.next)
        self.allow_input = False
        if (not keys[pg.K_RETURN]
            and self.allow_input_timer > 100):
                self.allow_input = True
