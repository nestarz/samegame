#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from .gfx import SuperSurface, Image
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

    def __init__(
        self,
        width,
        height,
        RGB=(0, 0, 0),
        alpha=255
    ):
        # call DirtySprite initializer
        ref = pg.Surface((width, height), pg.HWSURFACE | pg.SRCALPHA)
        pg.sprite.DirtySprite.__init__(self)
        SuperSurface.__init__(self, ref)
        self.RGBA = RGB + (alpha,)
        self.image.fill(self.RGBA)

    def update(self, elapsed):
        Sprite.update(self, elapsed)

class InformationGFX(Sprite):

    def __init__(self, information_obj):
        pg.sprite.DirtySprite.__init__(self)
        player = information_obj.player
        self.information_obj = information_obj
        self.right = bool(player.index)
        self.height = sum([spr.rect.h for spr in player.information_group])
        self.style = information_obj.style
        self.text = information_obj.text
        ref = render_text(self.text, 12, style=self.style)
        SuperSurface.__init__(self, ref)

    def position_information(self, board_gfx):
        if self.right:
            self.rect.right = board_gfx.rect.right + self.rect.w
        else:
            self.rect.left = board_gfx.rect.left - self.rect.w
        self.rect.y = board_gfx.rect.top + self.rect.h + self.height + 10

    def change_text(self, text):
        if self.text != text:
            self.image = render_text(text, 12, style=self.style)
            self.rect.size = self.image.get_rect().size
            self.text = text

    def update(self, elapsed, player):
        self.position_information(player.board_gfx)
        self.information_obj.update()
        self.change_text(self.information_obj.text)
        self.dirty = 1
        Sprite.update(self, elapsed)

class CursorGFX(Sprite):

    size = (43*2+1,42+2)

    def __init__(self, cursor, panel):
        pg.sprite.DirtySprite.__init__(self)
        ref = pg.Surface(CursorGFX.size, pg.HWSURFACE | pg.SRCALPHA)
        SuperSurface.__init__(self, ref)
        pg.draw.rect(self.image, (255,255,255), self.rect, 5)
        self.image = self.image.convert()
        self.rect.size = CursorGFX.size
        self.cursor = cursor
        self.pos_row = cursor.pos_row
        self.pos_col = cursor.pos_col

    def move(self, board):
        cursor = self.cursor
        if cursor.pos_row-self.pos_row != 0 or cursor.pos_col-self.pos_col != 0:
            self.rect.move_ip(0, -43*(cursor.pos_row-self.pos_row))
            self.rect.move_ip(43*(cursor.pos_col-self.pos_col), 0)
            self.pos_row, self.pos_col = cursor.pos_row, cursor.pos_col

    def update(self, elapsed, player):
        Sprite.update(self, elapsed)
        if not player.alive:
            self.image.set_alpha(70)
        self.move(player.board)
        self.rect.bottom = player.board_gfx.rect.bottom - (self.cursor.pos_row*43 + 2)
        self.rect.x = 7 + player.board_gfx.rect.x + self.cursor.pos_col*43
        self.dirty = 1

class BlockGFX(Sprite):
    """ Bloc de couleur """

    W, H = 38, 38
    size = (W,H)

    def __init__(self, case, player):
        pg.sprite.DirtySprite.__init__(self)
        ref = pg.Surface(BlockGFX.size, pg.HWSURFACE | pg.SRCALPHA)
        SuperSurface.__init__(self, ref)
        self.player = player
        self.image.fill(c.COLORS_DICT[case.color] + (245,))
        self.image = self.image.convert()
        self.board_gfx = player.board_gfx
        self.case = case
        self.pos = case.pos
        self.set_position(player.board_gfx)
        self.time_stacker = 0
        self.alive = True
        self.case.dying = False
        self.dying_time = 0
        self.frozen = False

    def set_position(self, surface):
        """ Positioning block relative to a surface """

        self.rect.bottom = surface.rect.bottom - (self.pos[0]*43 + 5)
        self.rect.x = 10 + surface.rect.x + self.pos[1]*43


    def color_update(self):
        if not self.player.alive:
            self.image.set_alpha(70)
        elif self.alive and not self.case.dying:
            if self.case.pos[0] == 0:
                self.image.set_alpha(110)
            else:
                self.image.set_alpha(255)

    def is_block_dying(self, dying_blocks):
        for line in dying_blocks:
            if self.case.pos in line:
                self.setup_effect('blink', 100)
                self.dying_timer = 1700
                self.board_gfx.freeze_col(self.case.pos[1], 1700)
                return True
        return False

    def move(self, board):
        case = self.case
        if case.pos[1]-self.pos[1] != 0:
            #self.rect.move_ip(43*(case.pos[1]-self.pos[1]), 0)
            self.setup_effect('move', 70, (43*(case.pos[1]-self.pos[1]), 0), 1)
        if case.pos[0]-self.pos[0] != 0:
            #self.rect.move_ip(0, -43*(case.pos[0]-self.pos[0]))
            self.setup_effect('move', 70, (0, -43*(case.pos[0]-self.pos[0])), 1)
        self.pos = case.pos

    def update(self, elapsed, player, dying_blocks):
        super().update(elapsed)
        self.color_update()
        if self.alive and not self.case.dying:
            self.case.dying = self.is_block_dying(dying_blocks)
            if self.case.on_swap or not self.frozen:
                self.move(player.board)
            elif self.case.dying and self.frozen:
                self.move(player.board)
        elif self.dying_timer < 0:
            self.case.dying = False
            self.alive = False
            self.kill()
            player.board_gfx.array[self.pos[0]][self.pos[1]] = None
        elif self.case.dying:
            self.dying_timer -= elapsed

class BoardGFX(Sprite):

    MARGIN_X = 5
    MARGIN_Y = 5
    COLOR = (0, 0, 0, 250)

    def __init__(self, board, index, panel):

        self.index = index

        # Calcul board size based on block size and board dimensions
        w = BoardGFX.MARGIN_X + (BoardGFX.MARGIN_X + BlockGFX.W) * board.num_col
        h = BoardGFX.MARGIN_Y + (BoardGFX.MARGIN_Y + BlockGFX.H) * board.num_row

        # Create surface that will welcome our board
        ref = pg.Surface((w, h), pg.HWSURFACE | pg.SRCALPHA)
        pg.sprite.DirtySprite.__init__(self)
        SuperSurface.__init__(self, ref)

        # Poisiton board
        self.position(panel)
        # Fill our board image with board color
        self.image.fill(BoardGFX.COLOR)
        # Array that will contain gfx block
        self.array = [[False for c in line] for line in board]
        # Array that contain frozen blocks by col
        self.frozen_cases = {}
        # Array that contain freeze timer by col
        self.freeze_timer = {}

    def __iter__(self):
        return self.array.__iter__()

    def position(self, panel):
        # Position board
        self.rect.bottom = panel.rect.bottom
        self.rect.x = panel.rect.left if self.index else panel.rect.right - self.rect.w

    def get_frozen_col(self):
        return self.frozen_cases.get(col, [])

    def freeze_col(self, col, duration):
        self.frozen_cases[col] = []
        for line in self.array:
            if line[col]:
                line[col].frozen = True
                self.freeze_timer[col] = duration
                self.frozen_cases[col].append(line[col])

    def defreeze_col(self, col):
        for case in self.frozen_cases[col]:
            case.frozen = False

    def freeze_update(self, elapsed):
        for col, timer in self.freeze_timer.items():
            if timer < 0:
                self.freeze_timer[col] = 0
                self.defreeze_col(col)
            else:
                self.freeze_timer[col] -= elapsed

    def update(self, elapsed, panel):
        # Position board
        self.position(panel)
        Sprite.update(self, elapsed)
        self.freeze_update(elapsed)
