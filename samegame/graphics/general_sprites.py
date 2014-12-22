#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from .gfx import SuperSurface, Image
from ..cache import cache
from ..tools import render_text
from .. import constants as c

class Sprite(pg.sprite.DirtySprite, SuperSurface):
    def __init__(self, surface):
        pg.sprite.DirtySprite.__init__(self)
        if isinstance(surface, Image):
            SuperSurface.__init__(self, surface.image)
        else:
            SuperSurface.__init__(self, surface)

    def update(self, elapsed):
        SuperSurface.update(self, elapsed)
        self.dirty = 1

class Button(Sprite):

    def __init__(
        self,
        txt,
        style=c.DEFAULT_BTN_STYLE,
        callback=None,
        parent=None
    ):
        self.style = style
        self.txt = txt
        ref = render_text(txt, style=self.style)
        pg.sprite.DirtySprite.__init__(self)
        SuperSurface.__init__(self, ref)
        self.callback = callback
        self.parent = parent
        self.targeted = False
        self.pause_text_effect = False
        if self.parent:
            self.rect.topright = self.parent.rect.topright
        WITH_ARROW = True
        self.setup_effect('hue_text_effect', 300, 2, style, txt, WITH_ARROW)

    def press(self):
        self.callback()

    def update(self, elapsed):
        if self.parent:
            self.rect.right = self.parent.rect.right - 25
        if not self.targeted and not self.pause_text_effect:
            self.pause_effect('hue_text_effect')
            self.pause_text_effect = True
        elif self.targeted and self.pause_text_effect:
            self.resume_effect('hue_text_effect')
            self.pause_text_effect = False
        Sprite.update(self, elapsed)
        self.dirty = 1

class Panel(Sprite):

    def __init__(self, width, height, RGB=(0, 0, 0), alpha=255):
        pg.sprite.DirtySprite.__init__(self)
        # call DirtySprite initializer
        ref = pg.Surface((width, height), pg.HWSURFACE | pg.SRCALPHA)
        SuperSurface.__init__(self, ref)
        self.RGBA = RGB + (alpha,)
        self.image.fill(self.RGBA)

    def update(self, elapsed):
        Sprite.update(self, elapsed)
