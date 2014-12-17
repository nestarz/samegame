#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from . import constants as c
from .effect import *
import cache.cache

class Surface:

    def __init__(self, surface):
        self.image = surface
        self.rect = self.image.get_rect()
        self.effectdict = EffectDict()
        self.visible = 1

    def setup_effect(self, name, *args):
        Effect = EFFECTS_DICT[name]
        if self.effectdict.get(name, False) == False:
            self.effectdict[name] = EffectList()
        self.effectdict[name].append(Effect(*args))

    def resize(self, w, h):
        self.image = pg.transform.scale(self.image, (int(w),
                                                         int(h)))
        self.rect = self.image.get_rect()

    def center(
        self,
        window,
        x=0,
        y=0,
    ):
        self.rect.centerx = window.get_rect().centerx + x
        self.rect.centery = window.get_rect().centery + y

    def update(self, elapsed):
        if self.effectdict.display:
            for n, elist in self.effectdict.items():
                for e in elist:
                    if not e.pause:
                        (self.image, self.rect) = e.apply(elapsed, self.image,
                                                           self.rect)
                        self.display = e.display
                        if e.done:
                            elist.remove(e)
                        if e.priority == 1:
                            break


class Image(Surface):
    """ Is not a sprite ! Usefull for once upon time blit and background """

    def __init__(self, img_filename):
        # Load the image
        image = cache.get_image(img_filename)
        # Call the parent class (Surface) constructor
        super().__init__(image)

    def update(self, elapsed):
        self.rect = self.image.get_rect()
        self.need_draw = not self.effectdict.is_empty() # Vrai si j'ai des effets à appliquer
        Surface.update(self, elapsed)

    def draw(self, dest):
        if self.display and self.need_draw:
            # Redessine limage uniquement si effet appliqué
            dest.blit(self.image, self.rect)
            return [self.rect]
