#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from .. import cache
from .. import constants as c
from ..screen import Screen

class Home(Screen):

    """ Enfant de l'objet State """

    def __init__(self):
        super().__init__()
        self.name = c.HOME
        self.next = c.MAIN_MENU

    def setup_images(self, screen):
        logo_img = Sprite(cache._cache.images['logo'].copy())
        logo_img.setup_effect('move', 1000, (0, -25))
        logo_img.setup_effect('fadein1', 1600)
        logo_img.center(screen, 0, 25 - 5)

        sublogo_img = t.Sprite(t.text_to_surface(c.AUTHOR, 'joystix',
                                                10, c.WHITE_RGB))
        sublogo_img.setup_effect('wait', 600)
        sublogo_img.setup_effect('fadein1', 1500, True)
        sublogo_img.center(screen, 0, 30)

        text1 = 'Press Start Button'
        img = t.Image(t.text_to_surface(text1, 'joystix', 20,
                                        c.WHITE_RGB), screen)
        start_img = pg.Surface(img.image.get_size(), pg.SRCALPHA)
        start_img.fill((0, 0, 0, 255))
        start_img.blit(img.image, img.rect)
        start_img = t.Sprite(start_img)
        start_img.setup_effect('blink', 500)
        start_img.setup_effect('wait', 500)
        start_img.center(screen, 0, 220)

        for img in [start_img, logo_img, sublogo_img]:
            img.add(self.sprites)

    def set_done(self, next):
        super().set_done(next)
        self.to_set_done = True
        self.to_set_done_timer = 500
        self.bg.setup_effect('fadeout', 1000)
        for spr in self.sprites:
            spr.setup_effect('fadeout', 2000)

    def check_for_input(self, keys):
        self.allow_input_timer += self.elapsed

        # j'augmente a chaque fois le timer
        # du temps passe depuis le dernier tick

        if self.allow_input:
            if keys[pg.K_RETURN]:
                self.allow_input_timer = 0
                self.set_done(self.next)
        self.allow_input = False
        if not keys[pg.K_RETURN] and self.allow_input_timer > 900:

            # si le temps passe dans la home
            # est superieur a 3 seconde alors
            # j'autorise la personne a passer
            # l'intro

            self.allow_input = True
