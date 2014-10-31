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
        self.to_set_done = -1
        self.time = 0

    def start(self, screen):
        self.setup_background(screen)
        self.setup_buttons(screen)
        self.setup_images(screen)

    def setup_background(self, screen):
        bg_img = cache._cache.images[self.name]
        self.bg = t.Image(bg_img, screen)
        self.bg.resize(*ct.SCREEN_SIZE)
        self.bg.setup_effect({'name':'fadeout2',
                'delay':20})

    def setup_buttons(self, screen):
        pass

    def setup_images(self, screen):
        logo_img = t.Image(cache._cache.images['logo'], screen)
        logo_img.setup_effect(ct.EFFECT['moveup25'],ct.EFFECT['fadein50'])
        logo_img.center(screen, 0, -5)
        sublogo_img = t.Image(t.text_to_surface(ct.AUTHOR, 'joystix', 10, ct.WHITE_RGB), screen)
        sublogo_img.setup_effect({
        'name': 'fadein',
        'delay': 45,
        'set_alpha':True
    }, ct.EFFECT['wait25'])
        sublogo_img.center(screen, 0, 30)

        text1 = 'Press Start Button'
        img = t.Image(t.text_to_surface(text1, 'joystix', 20, ct.WHITE_RGB), screen)
        start_img = pg.Surface(img.surface.get_size(), pg.SRCALPHA)
        start_img.fill((0,0,0,255))
        start_img.blit(img.surface, img.rect)
        start_img = t.Image(start_img, screen)
        start_img.setup_effect(ct.EFFECT['blink'], ct.EFFECT['wait70'])
        start_img.center(screen, 0, 220)

        self.images['start'] = start_img
        self.images['logo'] = logo_img
        self.images['sublogo'] = sublogo_img

    def set_done(self, next):
        self.next = next
        self.bg.setup_effect({'name':'fadein2',
                'delay':50})
        self.to_set_done = 10

    def check_for_input(self, keys):
        if self.allow_input:
            if keys[pg.K_RETURN]:
                self.set_done(self.next)
        self.allow_input = False
        if (not keys[pg.K_RETURN]
            and self.time > 70):
                self.allow_input = True

    def update(self, window, keys):
        self.time += 1
        self.check_for_input(keys)
        images = list()
        images.append(self.bg)
        images.extend(list(self.images.values()))
        for img in images:
            img.update()
        self.to_set_done -= 1
        if self.to_set_done == 0:
            self.done = True
