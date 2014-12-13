#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from . import cache
from . import constants as c

class EffectList(list):

    def resumeall(self):
        for e in self:
            e.resume()

    def stopall(self):
        for e in self:
            e.stop()

    def ongoing(self):
        for e in self:
            if not e.pause:
                return True
        return False

    def backup(self, img, rect):
        for e in self:
            if not e.first_apply:
                return e.backup()
        return (img, rect)

class State:

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
        self.elapsed = 0
        self.allow_input = False
        self.to_set_done = False
        self.to_set_done_timer = 0
        self.allow_input_timer = 0
        self.sprites = pg.sprite.LayeredDirty()
        self.killed = pg.sprite.LayeredDirty()
        self.rects = []

    def reinitialize(self):
        self.__init__()

    def start(self, window):
        """Set the window"""
        self.setup_background(window)
        self.setup_images(window)
        self.setup_buttons(window)

    def setup_background(self, window):
        """Set background and its effects"""
        bg_img = cache._cache.images[self.name] #retrieve bg_img from cache
        self.bg = Image(bg_img, window) #create background to apply on window
        self.bg.resize(*c.SCREEN_SIZE) #resize bg to window size
        self.bg.setup_effect('fadein2', 1000) #'ll apply effect fadein during 1s

    def setup_images(self, window):
        pass

    def setup_buttons(self, window):
        pass

    def set_done(self, next):
        self.next = next
        self.to_set_done_timer = 0

    def update(
        self,
        window,
        keys,
        elapsed,
    ):
        self.elapsed = elapsed #on récup le temps passé depuis le dernier up
        self.check_for_input(keys) #on check les evenements de l'user
        self.bg.update(elapsed)
        rects1 = self.bg.draw(window)
        self.sprites.clear(window, self.bg.image)
        self.sprites.update(elapsed, self.rects, self.killed)
        self.killed.update(elapsed, self.rects, self.killed)
        rects2 = self.sprites.draw(window) #on affiche sur la fenetre les sprites
        self.rects = rects1 + rects2 if rects1 else rects2
        if self.to_set_done:
            #si on a demandé à ce que l'event se termine
            #on up puis check le timer de fin
            self.to_set_done_timer -= self.elapsed
            self.done = max(0, self.to_set_done_timer) == 0

    def do_action(self, index):
        """Lance l'action du boutton ciblé par par l'index"""
        if index in range(0, len(self.buttons)):
            self.buttons[index].callback()

class Surface:
    def __init__(self, ref):
        self.image = ref
        self.rect = self.image.get_rect()
        self.effect = EffectList()
        self.display = True
        self.wait = False
        self.wait_effect = None
        self.previous_groups = []

    def setup_effect(self, name, *args):
        from .effect import EFFECTS_DICT
        Effect = EFFECTS_DICT[name]
        self.effect.append(Effect(*args))
        if name == 'wait':
            self.wait = True
            self.wait_effect = self.effect[-1]

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

    def update(self, *args):
        if self.wait:
            self.display = self.wait_effect.apply(args[0])
            if self.wait_effect.done:
                self.effect.remove(self.wait_effect)
                self.wait = False
        if not self.wait:
            for effect in self.effect:
                if not effect.pause:
                    (self.image,
                     self.rect) = effect.apply(args[0],
                                               self.image,
                                               self.rect)
                    self.display = effect.display
                    if effect.done:
                        self.effect.remove(effect)


class Image(Surface):

    def __init__(self, ref, surfaceToDrawTo):
        super().__init__(ref)
        self.imageToDrawTo = surfaceToDrawTo
        self.need_draw = True

    def update(self, elapsed):
        self.need_draw = bool(self.effect) # Vrai si j'ai des effets à appliquer
        Surface.update(self, elapsed)

    def draw(self, dest=None):
        if self.display and self.need_draw:
            # Redessine limage uniquement si effet appliqué
            dest = dest if dest else self.imageToDrawTo
            dest.blit(self.image, self.rect)
            return [self.rect]

class Sprite(pg.sprite.DirtySprite, Surface):
    def __init__(self, *args):
        pg.sprite.DirtySprite.__init__(self)
        Surface.__init__(self, *args)

    def update(self, *args):
        self.dirty = 1
        Surface.update(self, *args)
        up_rects = args[1]
        killed = args[2]
        if not self.display and not self in killed:
            self.previous_groups = self.groups()
            self.kill()
            self.add(killed)
        elif self.display and self.previous_groups:
            self.add(*self.previous_groups)
            self.remove(killed)
            self.previous_groups = []
        if self.effect:
            self.dirty = 1

class Button(Sprite):

    def __init__(
        self,
        txt,
        stylename='default',
        callback=None,
        parent=None
    ):
        self.style = c.BTN[stylename]
        self.txt = txt
        ref = text_to_surface(
            txt,
            self.style['font'],
            self.style['size'],
            self.style['default']['color'],
            self.style['AA'],
            self.style['bold'],
        )
        pg.sprite.DirtySprite.__init__(self)
        Surface.__init__(self, ref)
        self.callback = callback
        self.parent = parent
        self.targeted = False
        if self.parent:
            self.rect.topright = self.parent.rect.topright
        self.setup_effect('txt_effect1', 300, 2, self.style, self.txt)

    def update(self, *args):
        elapsed = args[0]
        up_rects = args[1]
        if self.parent:
            self.rect.right = self.parent.rect.right - 25
        if not self.targeted and self.effect.ongoing():
            self.effect.stopall()
            pack = self.effect.backup(self.image, self.rect)
            self.image, self.rect = pack
        elif self.targeted:
            self.effect.resumeall()
        Sprite.update(self, *args)
        self.dirty = 1 if self.targeted else 0
        self.targeted = False


def text_to_surface(
    text,
    name,
    size,
    color,
    AA=0,
    bold=False,
    italic=False,
):
    font = Font(name, size)
    font.set_bold(bold)
    font.set_italic(italic)
    return font.render(text, AA, color)

class Panel(Sprite):

    def __init__(
        self,
        size,
        RGBA=(0, 0, 0, 0)
    ):
        # call DirtySprite initializer
        ref = pg.Surface(size, pg.SRCALPHA)
        pg.sprite.DirtySprite.__init__(self)
        Surface.__init__(self, ref)
        self.RGBA = RGBA
        self.image.fill(RGBA)
        self.i = 0

    def update(self, *args):
        elapsed = args[0]
        up_rects = args[1]
        Sprite.update(self, *args)


class Font(pg.font.Font):

    def __init__(self, name, size):
        self.name = name
        self.size = size
        super().__init__(
            cache._cache.fonts.get(
                name,
                pg.font.get_default_font()),
            size)

class Block(Sprite):
    """ Bloc de couleur """

    size = (38,38)

    def __init__(self, color, pos, panel):
        print(color, pos)
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(Block.size)
        self.image.fill(color)
        self.rect = pos

    def update(self, *args):
        super().update(*args)
        self.dirty = 0
