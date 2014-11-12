#!/bin/python3

import pygame as pg
from . import cache
from . import constants as c
from . import tools as t
from .gamecore import GameCore, Cursor

class Party(GameCore, t.Screen):
    def __init__(self):
        super().__init__()
        self.timer = 0

class Arcade(Party):
    def __init__(self):
        super().__init__()
        self.name = 'arcade'
        self.next = 'home'
        self.board1 = self.all_board[0]
        self.cursor = self.board1.cursor

    def setup_images(self, screen):
        HEIGHT = screen.get_rect().h
        WIDTH = screen.get_rect().w

        panel1 = pg.Surface((WIDTH-150,HEIGHT-110), pg.SRCALPHA)
        panel1 = t.Panel(panel1, screen, (0,0,0,210), False)
        panel1.rect.midbottom = screen.get_rect().midbottom
        self.images['panel1'] = panel1

    def check_for_input(self, keys):
        if self.allow_input:
            if keys[pg.K_UP]:
                self.cursor.move_up()
            elif keys[pg.K_DOWN]:
                self.cursor.move_down()
            elif keys[pg.K_RIGHT]:
                self.cursor.move_right()
            elif keys[pg.K_LEFT]:
                self.cursor.move_left()
            elif keys[pg.K_RETURN] or keys[pg.K_SPACE]:
                self.board1.swap()
            elif keys[pg.K_ESCAPE]:
                self.set_done(self.next)
        self.allow_input = False
        if (not keys[pg.K_DOWN]
            and not keys[pg.K_UP]
            and not keys[pg.K_RIGHT]
            and not keys[pg.K_LEFT]
            and not keys[pg.K_RETURN]
            and not keys[pg.K_SPACE]
            and not keys[pg.K_ESCAPE]
            or (self.allow_input_timer > 6 and keys[pg.K_RIGHT])
            or (self.allow_input_timer > 6 and keys[pg.K_LEFT])
            or (self.allow_input_timer > 6 and keys[pg.K_DOWN])
            or (self.allow_input_timer > 6 and keys[pg.K_UP])):
                self.allow_input = True
                self.allow_input_timer = 0

    def set_done(self, next):
        super().set_done(next)
        self.to_set_done = 20
        self.bg.setup_effect('fadeout', 100)

    def update(self, window, keys):
        Party.update(self, window, keys)
        self.timer += 1
        img = t.Image(t.text_to_surface(' {:04d} '.format(self.timer), 'joystix', 22, c.WHITE_RGB), window)
        start_img = pg.Surface(img.surface.get_size(), pg.SRCALPHA)
        start_img.fill((0,0,0,150))
        start_img.blit(img.surface, img.rect)
        start_img = t.Image(start_img, window)
        start_img.rect.right = window.get_rect().right
        start_img.rect.x = start_img.rect.x - 80
        start_img.rect.y = start_img.rect.y + 80
        window.blit(start_img.surface, start_img.rect)
        board = self.board1
        for row in reversed(range(board.num_row)):
            for col in range(board.num_col):
                if not board.board[row][col] is False:
                    pg.draw.rect(self.images['panel1'].surface,
                                     board.board[row][col].color+(235,),
                                     [(5+38)*col+5,
                                      (5+38)*(board.num_row-row)-30+5,
                                      38,
                                      38])
                else:
                    pg.draw.rect(self.images['panel1'].surface,
                                     (255,255,255,50),
                                     [(5+38)*col+5,
                                      (5+38)*(board.num_row-row)-30+5,
                                      38,
                                      38])
                pg.draw.rect(self.images['panel1'].surface,
                                     (0,0,0),
                                     [(5+38)*col+5,
                                      (5+38)*(board.num_row-row)-30+5,
                                      38,
                                      38],3)
        pg.draw.rect(self.images['panel1'].surface,
                                         (255,255,255),
                                         [(5+38)*self.cursor.pos_col+5,
                                          (5+38)*(board.num_row-self.cursor.pos_row)-30+5,
                                          38,
                                          38],3)
        pg.draw.rect(self.images['panel1'].surface,
                                         (255,255,255),
                                         [(5+38)*(self.cursor.pos_col+1)+5,
                                          (5+38)*(board.num_row-self.cursor.pos_row)-30+5,
                                          38,
                                          38],3)
        self.board1.gravity()
