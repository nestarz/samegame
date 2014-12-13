#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from . import cache
from . import constants as c
from . import tools as t
from .gamecore import GameCore, Cursor
from time import sleep


class Player:

    INDEX = 0

    def __init__(self):
        Player.INDEX += 1

    def setup_game(self, board, keys):
        self.board = board
        self.cursor = self.board.cursor
        self.keys = keys
        self.blocks = pg.sprite.LayeredDirty()
        self.keys_move = [keys['UP'], keys[
            'DOWN'], keys['LEFT'], keys['RIGHT']]


class Party(t.Screen):

    def __init__(self):
        super().__init__()
        self.timer = 0


class Arcade(Party):

    def __init__(self):
        super().__init__()
        self.name = 'arcade'
        self.next = 'home'
        self.players = [Player(), Player()]
        self.img_boards = list()
        self.allow_input = [True for player in self.players]
        self.allow_swap = [True for player in self.players]
        self.allow_input_timer = [0
                                  for player in self.players]

    def start(self, screen):
        """ Creation des plateaux de jeu, des touches et
        attribution des plateaux de jeu aux joueurs """

        nb_color = 6
        nb_col = 7
        (self.case_w, self.case_h) = (38, 38)
        (self.margin_x, self.margin_y) = (5, 5)
        self.game = GameCore(1, nb_color, 10, nb_col, len(self.players))
        for (i, player) in enumerate(self.players):
            player.setup_game(self.game.all_board[i], c.CONTROLS[i])
        super().start(screen)
        self.setup_blocks(screen)

    def setup_blocks(self, screen):
        for (i, player) in enumerate(self.players):
            board = player.board
            dest = self.img_boards[i].image
            margin_x = 20
            for row in reversed(range(board.num_row)):
                for col in range(board.num_col):
                    if board.board[row][col].color:
                        pos = [margin_x + (5 + 38) * col + 5, (5 + 38) *
                             (board.num_row - row) - 30 - 5, 38, 38]
                        color = c.COLORS_DICT[board.board[row][col].color] + (235,)
                        block = t.Block(color, pos, dest)
                        block.add(player.blocks)

    def setup_images(self, screen):
        HEIGHT = screen.get_rect().h
        WIDTH = screen.get_rect().w

        panel = t.Panel((WIDTH - 150, HEIGHT - 110), (0, 0, 0, 210))
        panel.rect.midbottom = screen.get_rect().midbottom
        panel.add(self.sprites)
        margin_x = 30
        for (i, player) in enumerate(self.players):
            size = (self.margin_x +
                                (self.case_w +
                                 self.margin_x) *
                                player.board.num_col, self.margin_y +
                                (self.case_h +
                                 self.margin_y) *
                                player.board.num_row +
                                10)
            board = t.Panel(size, (255, 255, 255, 30))
            board.rect.y = panel.rect.h - board.rect.h
            board.rect.x = (panel.rect.w - board.rect.w + margin_x if i
                            > 0 else margin_x)
            margin_x = -margin_x
            self.img_boards.append(board)
            board.add(self.sprites)

    def check_for_input(self, keys):
        for (i, player) in enumerate(self.players):
            self.allow_input_timer[i] += self.elapsed
            if self.allow_input[i] and len([key for key in keys if key != 0]):
                if keys[player.keys['UP']]:
                    player.cursor.move_up()
                if keys[player.keys['DOWN']]:
                    player.cursor.move_down()
                if keys[player.keys['RIGHT']]:
                    player.cursor.move_right()
                if keys[player.keys['LEFT']]:
                    player.cursor.move_left()
                if keys[pg.K_ESCAPE]:
                    self.set_done(self.next)
            if self.allow_swap[i] and keys[player.keys['SWAP']]:
                player.board.swap()

            self.allow_input[i] = False
            self.allow_swap[i] = False

            no_key_pressed = not sum(keys[key] for key in player.keys_move)

            if self.allow_input_timer[i] > 70:
                self.allow_input[i] = True
                self.allow_input_timer[i] = 0
            elif no_key_pressed:
                self.allow_input[i] = True
                self.allow_input_timer[i] = -170

            if not keys[player.keys['SWAP']]:
                self.allow_swap[i] = True

    def set_done(self, next):
        super().set_done(next)
        self.to_set_done = True
        self.to_set_done_timer = 0.5
        self.bg.setup_effect('fadeout', 2)

    def update(
        self,
        window,
        keys,
        elapsed,
    ):
        super().update(window, keys, elapsed)
        self.timer += 1
        for (i, player) in enumerate(self.players):
            board = player.board
            cursor = player.cursor
            board.gravity()
            destroy = board.destroy_block()
            board.gravity()
            player.blocks.draw(window)
            if destroy:  # debug only
                print(destroy)
                print(board)
