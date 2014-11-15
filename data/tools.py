#!/bin/python3

import pygame as pg
from . import cache
from . import constants as c

class State():
    def __init__(self):
        self.done = False
        self.quit = False
        self.previous = None

    def reinitialize(self):
        self.done = False

    def check_for_input(self, keys):
        pass

class Screen(State):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.next = ''
        self.bg = None
        self.images = list()
        self.buttons = list()
        self.allow_input = False
        self.to_set_done = -1
        self.allow_input_timer = 0

    def reinitialize(self):
        super().reinitialize()
        self.bg = None
        self.images = list()
        self.buttons = list()

    def start(self, screen):
        self.setup_background(screen)
        self.setup_images(screen)
        self.setup_buttons(screen)

    def setup_background(self, screen):
        bg_img = cache._cache.images[self.name]
        self.bg = Image(bg_img, screen)
        self.bg.resize(*c.SCREEN_SIZE)
        self.bg.setup_effect('fadein2', 20)

    def setup_images(self, screen):
        pass

    def setup_buttons(self, screen):
        pass

    def set_done(self, next):
        self.next = next
        self.to_set_done = 0

    def update(self, window, keys):
        self.check_for_input(keys)
        images = list()
        images.append(self.bg)
        images.extend(self.images)
        for img in images:
            img.update()
        for btn in self.buttons:
            btn.update(self.arrow_index, self.buttons.index(btn))
        self.to_set_done -= 1
        self.done = self.to_set_done == 0

    def do_action(self, index):
        if index in range(0, len(self.buttons)):
            self.buttons[index].callback()


class Image():
    def __init__(self, ref, surfaceToDrawTo):
        self.surface = ref
        self.rect = self.surface.get_rect()
        self.effect = list()
        self.display = True
        self.surfaceToDrawTo = surfaceToDrawTo
        self.wait = False
        self.wait_effect = None

    def setup_effect(self, name, *args):
        from .effect import EFFECTS_DICT
        Effect = EFFECTS_DICT[name]
        self.effect.append(Effect(*args))
        if name == 'wait':
            self.wait = True
            self.wait_effect = self.effect[-1]

    def center(self, screen, x=0, y=0):
        self.rect.centerx = screen.get_rect().centerx + x
        self.rect.centery = screen.get_rect().centery + y

    def update(self):
        if self.wait:
            self.display = self.wait_effect.apply()
            if self.wait_effect.done:
                self.effect.remove(self.wait_effect)
                self.wait = False
        if not self.wait:
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
        self.style = c.BTN[stylename]
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
