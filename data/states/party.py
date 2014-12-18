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
        # Get speed/player if passed in args with previous screens
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

        # Each player will set the new information box
        for player in self.players:
            player.add_information(name, info)

    def setup_information(self, player):

        info = "Player {}".format(player.index)
        info = "Speed x{}".format(self.speed)

        # Create useful information box for multiple usage
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

    def setup_input(self):

        # General input handling, game inputs are set in player object
        self.actions[pg.K_ESCAPE] = lambda: self.set_done(c.SELECT_CHAR, speed=self.speed)

    def set_done(self, next, **kwargs):

        # Call parent class (Screen) set_done function
        # Pass in next screen's name to display and
        # persistant data through kwargs dictionary
        super().set_done(next, **kwargs)

        # Set a countdown before state flip and apply effects
        # on panels sprites, with same or less duration as countdown
        self.final_countdown = c.BG_FADE_TIME

    def update(self, window, keys, elapsed):
        super().update(window, keys, elapsed)
        self.timer += elapsed
        for player in self.players:
            player.update(window, keys, elapsed)
