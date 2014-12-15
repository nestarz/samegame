#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from . import cache
from . import constants as c

class EffectDict(dict):
    def resumeall(self):
        for l in self.values():
            l.resumeall()

    def stopall(self):
        for l in self.values():
            l.stopall()

    def ongoing(self):
        for l in self.values():
            if l.ongoing():
                return True
        return False

    def backup(self, img, rect):
        for l in self.values():
            for e in l:
                if not e.first_apply:
                    return e.backup()
        return (img, rect)

    def is_empty(self):
        for l in self.values():
            if l:
                return False
        return True

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
        self.sprites.update(elapsed)
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
        self.effectdict = EffectDict()
        self.display = True
        self.wait = False
        self.wait_effect = None
        self.previous_groups = []

    def setup_effect(self, name, *args):
        from .effect import EFFECTS_DICT
        Effect = EFFECTS_DICT[name]
        if self.effectdict.get(name, False) == False:
            self.effectdict[name] = EffectList()
        self.effectdict[name].append(Effect(*args))
        if name == 'wait':
            self.wait = True
            self.wait_effect = self.effectdict[name][-1]

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
        if self.wait:
            self.display = self.wait_effect.apply(elapsed)
            if self.wait_effect.done:
                self.effectdict['wait'].remove(self.wait_effect)
                self.wait = False
        if not self.wait:
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

    def __init__(self, ref, surfaceToDrawTo):
        super().__init__(ref)
        self.imageToDrawTo = surfaceToDrawTo
        self.need_draw = True

    def update(self, elapsed):
        self.need_draw = not self.effectdict.is_empty() # Vrai si j'ai des effets à appliquer
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

    def update(self, elapsed):
        self.dirty = 1
        Surface.update(self, elapsed)
        if not self.display:
            self.visible = 0
            self.dirty = 1
        elif self.display:
            self.visible = 1
            if not self.effectdict.is_empty():
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

    def update(self, elapsed):
        if self.parent:
            self.rect.right = self.parent.rect.right - 25
        if not self.targeted and self.effectdict.ongoing():
            self.effectdict.stopall()
            pack = self.effectdict.backup(self.image, self.rect)
            self.image, self.rect = pack
        elif self.targeted:
            self.effectdict.resumeall()
        Sprite.update(self, elapsed)
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

    def update(self, elapsed):
        Sprite.update(self, elapsed)


class Font(pg.font.Font):

    def __init__(self, name, size):
        self.name = name
        self.size = size
        super().__init__(
            cache._cache.fonts.get(
                name,
                pg.font.get_default_font()),
            size)

class InfoGFX(Sprite):

    def __init__(
        self,
        txt,
        player,
        level
    ):
        self.style = c.BTN['default']
        self.txt = txt
        self.level = level
        ref = text_to_surface(
            txt,
            self.style['font'],
            12,
            self.style['default']['color'],
            self.style['AA'],
            self.style['bold'],
        )
        pg.sprite.DirtySprite.__init__(self)
        Surface.__init__(self, ref)
        self.player = player
        if self.player.index == 1:
            self.rect.topright = self.player.board_gfx.rect.topright
        else:
            self.rect.topleft = self.player.board_gfx.rect.topleft

    def change_txt(self, txt):
        if self.txt != txt:
            self.image = text_to_surface(
                txt,
                self.style['font'],
                12,
                self.style['default']['color'],
                self.style['AA'],
                self.style['bold'],
            )
            self.rect.size = self.image.get_rect().size

    def update(self, elapsed):
        if self.player.index == 1:
            self.rect.right = self.player.board_gfx.rect.right + self.rect.w
        else:
            self.rect.left = self.player.board_gfx.rect.left - self.rect.w
        self.rect.y = self.player.board_gfx.rect.top + self.rect.h * self.level
        self.dirty = 1
        Sprite.update(self, elapsed)

class BlockGFX(Sprite):
    """ Bloc de couleur """

    size = (38,38)
    INDEX = 0
    pause = []

    def __init__(self, case, player):
        self.index = BlockGFX.INDEX
        BlockGFX.INDEX += 1
        if len(BlockGFX.pause) <= player.index:
            BlockGFX.pause.append(False)
        self.player = player
        pg.sprite.DirtySprite.__init__(self)
        ref = pg.Surface(BlockGFX.size, pg.SRCALPHA)
        Surface.__init__(self, ref)
        self.rect.size = BlockGFX.size
        self.rect.bottom = player.board_gfx.rect.bottom - (case.pos[0]*43 + 5)
        self.rect.x = 10 + player.board_gfx.rect.x + case.pos[1]*43
        self.image.fill(c.COLORS_DICT[case.color] + (245,))
        self.image = self.image.convert()
        self.case = case
        self.pos = case.pos
        self.time_stacker = 0
        self.alive = True

    def move(self, board):
        case = self.case
        if case.pos[1]-self.pos[1] != 0:
            self.setup_effect('move', 50, (43*(case.pos[1]-self.pos[1]), 0), 1)
        if case.pos[0]-self.pos[0] != 0:
            self.setup_effect('move', 100, (0, -43*(case.pos[0]-self.pos[0])), 1)
        self.pos = case.pos

    def update(self, elapsed, board):
        Sprite.update(self, elapsed)
        swap_ongoing = self.case.swap_ongoing
        if self.pos[0] == 0:
            self.image.set_alpha(30)
        else:
            self.image.set_alpha(255)
        if not self.case.pos:
            if self.alive:
                self.setup_effect('blink', 150)
                BlockGFX.pause[self.player.index] = True
            self.time_kill(elapsed)
        elif not BlockGFX.pause[self.player.index] or swap_ongoing :
            self.move(board)
            self.case.swap_ongoing = False
        self.dirty = 1

    def time_kill(self, elapsed):
        self.alive = False
        if self.time_stacker > 1700:
            self.kill()
            BlockGFX.pause[self.player.index] = False
        self.time_stacker += elapsed

class CursorGFX(Sprite):

    size = (43*2+1,42+2)

    def __init__(self, cursor, panel):
        pg.sprite.DirtySprite.__init__(self)
        ref = pg.Surface(CursorGFX.size, pg.SRCALPHA)
        Surface.__init__(self, ref)
        pg.draw.rect(self.image, (255,255,255), self.rect, 5)
        self.rect.size = CursorGFX.size
        self.cursor = cursor
        self.rect.bottom = panel.rect.bottom - (cursor.pos_row*43 + 2)
        self.rect.x = 7 + panel.rect.x + cursor.pos_col*43
        self.pos_row = cursor.pos_row
        self.pos_col = cursor.pos_col

    def move(self, board):
        cursor = self.cursor
        if cursor.pos_row-self.pos_row != 0 or cursor.pos_col-self.pos_col != 0:
            self.rect.move_ip(0, -43*(cursor.pos_row-self.pos_row))
            self.rect.move_ip(43*(cursor.pos_col-self.pos_col), 0)
            self.pos_row, self.pos_col = cursor.pos_row, cursor.pos_col

    def update(self, elapsed, board):
        Sprite.update(self, elapsed)
        self.move(board)
        self.dirty = 1
