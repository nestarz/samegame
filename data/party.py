#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from . import cache
from . import constants as c
from .tools import Screen, Panel, BlockGFX, CursorGFX, InfoGFX
from .gamecore import GameCore, Cursor


class Player:

    INDEX = 0

    def __init__(self):
        Player.INDEX += 1
        self.index = Player.INDEX
        self.hidden_timer = 0

    def setup_game(self, board, board_gfx, keys):
        self.board = board
        self.cursor = self.board.cursor
        self.keys = keys
        self.board_gfx = board_gfx
        self.pause = 0
        self.blocks_gfx = pg.sprite.LayeredDirty()
        self.cursor_gfx = pg.sprite.LayeredDirty()
        self.info_gfx = pg.sprite.LayeredDirty()
        self.info = {}
        cursor = CursorGFX(self.cursor, board_gfx)
        cursor.add(self.cursor_gfx)
        self.alive = True
        self.score = 0
        self.setup_blocks()
        self.keys_move = [keys['UP'], keys[
            'DOWN'], keys['LEFT'], keys['RIGHT']]

    def setup_blocks(self):
        board = self.board
        for row in reversed(range(board.num_row)):
            for col in range(board.num_col):
                if board.board[row][col].color:
                    block = BlockGFX(board.board[row][col], self)
                    block.add(self.blocks_gfx)

class Party(Screen):

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
        self.allow_up_row = [True for player in self.players]

    def reinitialize(self):
        Player.INDEX = 0
        super().reinitialize()

    def start(self, screen, persist):
        """ Creation des plateaux de jeu, des touches et
        attribution des plateaux de jeu aux joueurs """

        nb_color = 6
        nb_col = 7
        (self.case_w, self.case_h) = (38, 38)
        (self.margin_x, self.margin_y) = (5, 5)
        self.speed = persist.get('speed', 2)
        self.game = GameCore(self.speed, nb_color, 10, nb_col, len(self.players))
        super().start(screen, persist)
        for (i, player) in enumerate(self.players):
            player.setup_game(self.game.all_board[i], self.img_boards[i], c.CONTROLS[i])
            self.setup_info_gfx(player)
            print("Player {} : {}".format(i+1, c.CONTROLS[i]))

    def setup_info_gfx(self, player):
        info = "Player {}".format(player.index)
        a = InfoGFX(info,  player, 0)
        a.add(player.info_gfx)
        player.info["nom"] = a
        info = "Speed x{}".format(self.speed)
        e = InfoGFX(info,  player, 1)
        e.add(player.info_gfx)
        player.info["mode"] = e
        info = ""
        b = InfoGFX(info,  player, 2)
        b.add(player.info_gfx)
        player.info["new_row"] = b
        c = InfoGFX(info,  player, 3)
        c.add(player.info_gfx)
        player.info["pause"] = c
        d = InfoGFX(info,  player, 4)
        d.add(player.info_gfx)
        player.info["score"] = d

    def setup_images(self, screen):
        HEIGHT = screen.get_rect().h
        WIDTH = screen.get_rect().w

        panel = Panel((WIDTH - 150, HEIGHT - 110), (0, 0, 0, 210))
        panel.rect.midbottom = screen.get_rect().midbottom
        panel.add(self.sprites)
        for (i, player) in enumerate(self.players):
            size = (self.margin_x +
                                (self.case_w +
                                 self.margin_x) *
                                self.game.num_col + 10, self.margin_y +
                                (self.case_h +
                                 self.margin_y) *
                                self.game.num_row +
                                10)
            board = Panel(size, (255, 255, 255, 30))
            if i == 0:
                board.rect.bottomleft = panel.rect.bottomleft
            else:
                board.rect.bottomright = panel.rect.bottomright
            self.img_boards.append(board)
            board.add(self.sprites)

    def check_for_input(self, keys):
        for (i, player) in enumerate(self.players):
            if keys[pg.K_ESCAPE]:
                self.set_done(c.SELECT_CHAR, speed=self.speed)
            if player.alive:
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
                if self.allow_swap[i] and keys[player.keys['SWAP']]:
                    case1, case2 = player.board.swap()
                    case1.swap_ongoing = True
                    case2.swap_ongoing = True
                if self.allow_up_row[i] and keys[player.keys['GENERATE']]:
                    self.up_row(player, player.board)

                self.allow_input[i] = False
                self.allow_swap[i] = False
                self.allow_up_row[i] = False

                no_key_pressed = not sum(keys[key] for key in player.keys_move)

                if self.allow_input_timer[i] > 70:
                    self.allow_input[i] = True
                    self.allow_input_timer[i] = 0
                elif no_key_pressed:
                    self.allow_input[i] = True
                    self.allow_input_timer[i] = -170

                if not keys[player.keys['SWAP']]:
                    self.allow_swap[i] = True
                if not keys[player.keys['GENERATE']]:
                    self.allow_up_row[i] = True

    def set_done(self, next, **kwargs):
        super().set_done(next, **kwargs)
        self.to_set_done = True
        self.to_set_done_timer = 0.5
        self.bg.setup_effect('fadeout', 2)

    def up_row(self, player, board):
        if board.top_row_empty():
            board.up()
            player.cursor.move_up()
            cases = board.generate_hidden()
            for c in cases:
                block = BlockGFX(c, player)
                block.add(player.blocks_gfx)
        else:
            player.alive = False
            info = "Game Over"
            b = InfoGFX(info, player, 5)
            b.add(player.info_gfx)
            player.info["alive"] = b

    def game_event(self, elapsed, player, board, destroy):
        if player.alive:
            player.pause += destroy*1000
            info = "Pause={}s".format(str(int((player.pause)/600)))
            player.info['pause'].change_txt(info)
            info = "Up in {:.0f}s".format(int(self.game.speed + player.pause - player.hidden_timer)/600)
            player.info['new_row'].change_txt(info)
            if destroy:
                player.score += destroy
                info = "Score={:.0f}".format(player.score)
                player.info['score'].change_txt(info)
            if player.pause > 0:
                player.pause -= elapsed
            elif player.hidden_timer > self.game.speed:
                self.up_row(player, board)
                player.hidden_timer = 0
            else:
                player.pause = 0
                player.hidden_timer += elapsed

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
            board.check_destroy()
            player.blocks_gfx.update(elapsed, board)
            player.cursor_gfx.update(elapsed, board)
            player.info_gfx.update(elapsed)
            self.rects += player.cursor_gfx.draw(window)
            self.rects += player.blocks_gfx.draw(window)
            self.rects += player.info_gfx.draw(window)
            destroy = board.destroy_block()
            board.gravity()
            self.game_event(elapsed, player, board, destroy)
