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


class Effect():
    def __init__(self, ref, name='default', delay=0):
        self.name = ref.get('name', name)
        self.init_delay = ref.get('delay', delay)
        self.direction = ref.get('direction', ct.STATIC)
        self.current_delay = self.init_delay
        self.display = True
        self.done = False
        self.sign1 = 1
        self.sign2 = -1
    def apply(self, surface, rect, AA=0):
        if self.name == 'shake':
            self.sign1 = - self.sign1
            self.sign2 = - self.sign2
            rect = rect.move(self.sign1*1,self.sign2*1)
        if self.name == 'wait':
            if self.current_delay == 0:
                self.display = True
                self.done = True
            elif self.current_delay > 0:
                self.display = False
                self.current_delay -= 1
        if self.name == 'move':
            if self.current_delay == 0:
                rect = self.init_rect
                self.done = True
            elif self.current_delay > 0:
                if self.current_delay == self.init_delay:
                    self.init_rect = rect
                    rect = rect.move(0,self.init_delay)
                ratio = 1-(self.current_delay / self.init_delay)
                rect = rect.move(*self.direction)
                self.current_delay -= 1
        if self.name == 'blink':
            if self.current_delay == 0:
                self.display = not self.display
                self.current_delay = self.init_delay
            elif self.current_delay > 0:
                self.current_delay -= 1
        if self.name == 'fadein':
            if self.current_delay == 0:
                self.alpha = 255
                self.done = True
            elif self.current_delay > 0:
                ratio = 1-(self.current_delay / self.init_delay)
                self.alpha = ratio*255
                # /!\ marche seulement si AA=1
                self.apply_alpha(surface, self.alpha)
                # /!\ marche seulement si AA=0
                surface.set_alpha(int(self.alpha))
                self.current_delay -= 1
        return surface, rect

    def apply_alpha(self, surface, alpha):
        for x in range(surface.get_width()):
            for y in range(surface.get_height()):
                color = surface.get_at((x, y))
                if color.a != 0:
                    color.a = min(int(alpha+1),255)
                surface.set_at((x, y), color)


class Image():
    def __init__(self, ref):
        self.surface = ref
        self.rect = self.surface.get_rect()
        self.effect = list()
        self.display = True

    def setup_effect(self, *args):
        for item in args:
            self.effect.append(Effect(item))

    def center(self, screen, x=0, y=0):
        self.rect.centerx = screen.get_rect().centerx + x
        self.rect.centery = screen.get_rect().centery + y

    def update(self):
        for effect in self.effect:
            self.surface, self.rect = effect.apply(self.surface, self.rect)
            self.display = effect.display
            if effect.done:
                self.effect.remove(effect)

class Button(Image):
    INDEX = 0
    def __init__(self, text, callback=None, style='default'):
        Button.INDEX += 1
        self.index = Button.INDEX
        self.callback = callback
        self.text = text
        self.style = ct.BUTTON_STYLE.get(style, 'default')
        self.surface = text_to_surface(text, self.style['fontname'],
            self.style['fontsize'], self.style['default']['textcolor'])
        self.rect = self.surface.get_rect()
        self.display = True
        self.effect = list()

def text_to_surface(text, name, size, color):
    font = Font(name, size)
    return font.render(
        text, 0, color)


class Font(pg.font.Font):
    def __init__(self, name, size):
        self.name = name
        self.size = size
        super().__init__(
            cache._cache.fonts.get(name, pg.font.get_default_font()),
            size)

class CustomButton(Button):
    def __init__(self, text, customstyle):
        super().__init__(text)
