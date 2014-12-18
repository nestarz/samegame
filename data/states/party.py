#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from .. import cache
from .. import constants as c
from ..screen import Screen
from ..graphics.sprites import Panel, BlockGFX, CursorGFX, InfoGFX
from ..gamecore import GameCore, Cursor
from ..player import Player


class Party(Screen):

    def __init__(self):

        # Call the parent class (Screen) constructor
        super().__init__()

        # Time since party start
        self.timer = 0

        # List that contains players objects
        self.players = []

class Arcade(Party):

    def __init__(self):

        # Call the parent class (Party) constructor
        super().__init__()

        # Set screen name and next default screen
        self.name = c.ARCADE
        self.next = c.HOME

    def start(self, screen, persist):

        # Game constants
        SPEED = persist.get('speed', 1)
        NB_PLAYER = persist.get('nb_player', 1)
        NB_COLOR = 6
        NB_ROW = 10
        NB_COL = 7

        # Set players
        self.players = [Player(i) for i in range(NB_PLAYER)]

        # Set GameCore
        self.game = GameCore(SPEED, NB_COLOR, NB_ROW, NB_COL)

        # Generate logic then graphic board for each player
        for player in self.players:
            board = self.generate_board()
            gfx_board = self.setup_board(board)
            player.setup_game(board, gfx_board)

    def add_information(self, name, info=''):
        for player in self.players:
            sprite = InfoGFX(name, info)
            sprite.add(player.info_group)

    def setup_information(self, player):

        info = "Player {}".format(player.index)
        info = "Speed x{}".format(self.speed)

        self.add_information('nom', player_id)
        self.add_information('mode', mode_id)
        self.add_information('new_row')
        self.add_information('pause')
        self.add_information('score')


    def setup_panel(self, screen):

        # Window size
        HEIGHT = screen.get_rect().h
        WIDTH = screen.get_rect().w

        # Create panel that will contain boards
        panel = Panel((WIDTH - 150, HEIGHT - 110), (0, 0, 0, 210))
        panel.rect.midbottom = screen.get_rect().midbottom + panel.rect.h
        panel.setup_effect('move', 2000, (-panel.rect.h, 0))
        panel.add(self.panels_group)

    def setup_board(self, board):

        # Create graphic board thanks to logic board
        board = BoardGFX(board)
        board.setup_effect('fadein', 1500)
        board.add(self.boards_group)
        return board

    def check_input(self, keys):
        for (i, player) in enumerate(self.players):
            if keys[pg.K_ESCAPE]:
                self.set_done(c.SELECT_CHAR, speed=self.speed)
            if player.alive:
                player.allow_input_timer += self.elapsed
                if player.allow_input and len([key for key in keys if key != 0]):
                    if keys[player.keys['UP']]:
                        player.cursor.move_up()
                    if keys[player.keys['DOWN']]:
                        player.cursor.move_down()
                    if keys[player.keys['RIGHT']]:
                        player.cursor.move_right()
                    if keys[player.keys['LEFT']]:
                        player.cursor.move_left()
                if player.allow_swap and keys[player.keys['SWAP']]:
                    case1, case2 = player.board.swap()
                    case1.swap_ongoing = True
                    case2.swap_ongoing = True
                if player.allow_up_row and keys[player.keys['GENERATE']]:
                    self.up_row(player, player.board)

                player.allow_input = False
                player.allow_swap = False
                player.allow_up_row = False

                no_key_pressed = not sum(keys[key] for key in player.keys_move)

                if player.allow_input_timer > 70:
                    player.allow_input = True
                    player.allow_input_timer = 0
                elif no_key_pressed:
                    player.allow_input = True
                    player.allow_input_timer = -170

                if not keys[player.keys['SWAP']]:
                    player.allow_swap = True
                if not keys[player.keys['GENERATE']]:
                    player.allow_up_row = True

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
