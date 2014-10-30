#!/bin/python3

import pygame as pg
from . import cache
from . import constants as ct

class State():
    def __init__(self):
        self.done = False
        self.quit = False
        self.previous = None

    def reinitialize(self):
        self.done = False

    def check_for_input(self, keys):
        pass

class Effect():
    def __init__(self, ref, name='default', delay=0):
        self.name = ref.get('name', name)
        self.init_delay = ref.get('delay', delay)
        self.direction = ref.get('direction', ct.STATIC)
        self.set_alpha = ref.get('set_alpha', False)
        self.speed = ref.get('speed', 1)
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
                if self.set_alpha:
                    # /!\ marche seulement si AA=0
                    surface.set_alpha(int(self.alpha))
                else:
                    # /!\ marche seulement si AA=1
                    self.apply_alpha(surface, self.alpha)
                self.current_delay -= 1
        if self.name == 'move2':
            if self.current_delay == 0:
                rect = self.init_rect
                self.done = True
            elif self.current_delay > 0:
                if self.current_delay == self.init_delay:
                    self.init_rect = rect
                    rect = rect.move(-surface.get_width(),0)
                rect = rect.move(
                    self.direction[0]*self.speed,
                    self.direction[1]*self.speed)
                self.current_delay -= 1
        if self.name == 'move3':
            if self.current_delay == 0:
                rect = self.init_rect
                self.done = True
            elif self.current_delay > 0:
                if self.current_delay == self.init_delay:
                    self.init_rect = rect
                    rect = rect.move(0,0)
                rect = rect.move(
                    self.direction[0]*self.speed,
                    self.direction[1]*self.speed)
                self.current_delay -= 1
        if self.name == 'fadein2':
            ratio = (self.current_delay / self.init_delay)
            self.alpha = int(ratio*255)
            if self.current_delay == self.init_delay:
                panel = pg.Surface(surface.get_size(), pg.SRCALPHA)
                self.panel = Panel(panel, surface, (0,0,0,20), False)
            elif self.current_delay == 0:
                self.panel.fill((0,0,0,0))
                self.done = True
            else:
                self.panel.fill((0,0,0,20))
                self.panel.draw()
            self.current_delay -= 1
        if self.name == 'fadeout2':
            ratio = (self.current_delay / self.init_delay)
            self.alpha = int(ratio*255)
            if self.current_delay == self.init_delay:
                self.surface_init = surface.copy()
            if self.current_delay == 0:
                surface = self.surface_init.copy()
                self.done = True
            else:
                surface = self.surface_init.copy()
                panel = pg.Surface(surface.get_size(), pg.SRCALPHA)
                self.panel = Panel(panel, surface, (0,0,0,self.alpha), False)
                self.panel.fill((0,0,0,self.alpha))
                self.panel.draw()
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
    def __init__(self, ref, surfaceToDrawTo):
        self.surface = ref
        self.rect = self.surface.get_rect()
        self.effect = list()
        self.display = True
        self.surfaceToDrawTo = surfaceToDrawTo

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
        self.draw()

    def draw(self):
        if self.display:
            self.surfaceToDrawTo.blit(self.surface, self.rect)

    def resize(self, w, h):
        self.surface = pg.transform.scale(self.surface,(int(w),int(h)))
        self.rect = self.surface.get_rect()


class Button(Image):
    def __init__(self, surfaceToDrawTo, txt, stylename='default', callback=None):
        self.style = ct.BTN[stylename]
        self.txt = txt
        ref = text_to_surface(
            txt,
            self.style['font'],
            self.style['size'],
            self.style['default']['color'],
            self.style['AA'],
            self.style['bold'])
        super().__init__(ref, surfaceToDrawTo)
        self.callback = callback
        self.original = self.surface
        self.arrow_txt = ''
        self.start = True
        self.i = 0

    def update(self, arrow_index, index):
        if arrow_index == index:
            style_hover = self.style.get('hover', 'default')
            if self.arrow_txt == '* ':
                self.arrow_txt = '+ '
            else:
                self.arrow_txt = '* '
            if self.start:
                self.color = self.temp_c = style_hover['color']
                self.start = False
            else:
                if 0 <= self.i < 15:
                    self.temp_c = tuple([x-4 for x in self.temp_c])
                    self.color = tuple([max(0,min(x-4,255)) for x in self.temp_c])
                    self.i += 1
                elif 15 <= self.i < 30:
                    self.temp_c = tuple([x+4 for x in self.temp_c])
                    self.color = tuple([min(max(0,x+4),255) for x in self.temp_c])
                    self.i += 1
                else:
                    self.i = 0
            self.surface = text_to_surface(
                self.txt + self.arrow_txt,
                self.style['font'],
                self.style['size'],
                self.color,
                self.style['AA'],
                self.style['bold'])
        else:
            self.surface = self.original
            self.effect = []
            self.start = True
        Image.update(self)

def text_to_surface(text, name, size, color, AA=0, bold=False, italic=False):
    font = Font(name, size)
    font.set_bold(bold)
    font.set_italic(italic)
    return font.render(
        text, AA, color)

class Panel(Image):
    def __init__(self, ref, surfaceToDrawTo, RGBA=(0,0,0,0), refill=False):
        super().__init__(ref, surfaceToDrawTo)
        self.RGBA = RGBA
        self.fill(RGBA)
        self.refill = refill

    def fill(self, RGBA=None):
        if RGBA != None:
            self.RGBA = RGBA
        self.surface.fill(self.RGBA)

    def update(self):
        Image.update(self)
        if self.refill:
            self.fill()

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
