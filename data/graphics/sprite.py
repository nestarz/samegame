#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from .surface import Surface
from .tools import render_text

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

class Panel(Sprite):

    def __init__(
        self,
        width,
        height,
        RGB=(0, 0, 0),
        alpha=255
    ):
        # call DirtySprite initializer
        ref = pg.Surface((width, height), pg.SRCALPHA)
        pg.sprite.DirtySprite.__init__(self)
        Surface.__init__(self, ref)
        self.RGBA = RGB + (alpha,)
        self.image.fill(self.RGBA)

    def update(self, elapsed):
        Sprite.update(self, elapsed)

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
            self.rect.move_ip(43*(case.pos[1]-self.pos[1]), 0)
            #self.setup_effect('move', 50, (43*(case.pos[1]-self.pos[1]), 0), 1)
        if case.pos[0]-self.pos[0] != 0:
            self.rect.move_ip(0, -43*(case.pos[0]-self.pos[0]))
            #self.setup_effect('move', 100, (0, -43*(case.pos[0]-self.pos[0])), 1)
        self.pos = case.pos

    def update(self, elapsed, board):
        Sprite.update(self, elapsed)
        swap_ongoing = self.case.swap_ongoing
        if self.case in self.player.board.destroy:
            self.move(board)
        if self.pos[0] == 0:
            self.image.set_alpha(30)
        elif not self.player.alive:
            self.image.set_alpha(45)
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
