#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
import samegame.cache
import samegame.constants as c
from samegame.screen import Screen
from samegame.graphics.general_sprites import Panel
from samegame.graphics.party_sprites import BlockGFX, CursorGFX, InformationGFX
from samegame.gamecore import GameCore, Cursor
from samegame.player.player import Player


class Game(Screen):

    def __init__(self):

        # Call the parent class (Screen) constructor
        super().__init__()

        # Time since party start
        self.timer = 0

        # List that contains players objects
        self.players = []

        # Groups that will contain panel
        self.panel_group = pg.sprite.LayeredDirty()

        # Add groups to all_groups tuple
        self.all_groups = (self.panel_group,)


class Arcade(Game):

    def __init__(self):

        # Call the parent class (Party) constructor
        super().__init__()

        # Set screen name and next default screen
        self.name = c.ARCADE
        self.next = c.HOME

    def start(self, window, persist):

        # Call the parent class (Screen) start function
        super().start(window, persist)
        self.setup_panel(window)

        # Game constants
        # Get speed/player if passed in args with previous screens
        SPEED = persist.get('speed', c.SPEED[1])
        NB_PLAYER = persist.get('nb_player', 2)
        NB_COLOR = 6
        NB_ROW = 10
        NB_COL = 7

        # Set players
        self.players = [Player(i) for i in range(NB_PLAYER)]

        # Set GameCore
        self.game = GameCore(SPEED, NB_COLOR, NB_ROW, NB_COL)

        # Generate logic then graphic board for each player
        for player in self.players:
            board = self.game.generate_board()
            player.setup_game(board, self.panel)

        self.setup_input()

    def setup_panel(self, screen):

        # Window size
        HEIGHT = screen.get_rect().h
        WIDTH = screen.get_rect().w
        RECT = screen.get_rect()
        # Panel constants
        PANEL_COLOR = c.BLACK_RGB
        PANEL_ALPHA = 200
        PANEL_WIDTH = WIDTH - 70
        PANEL_HEIGHT = HEIGHT - 110

        # Create panel that will contain boards
        self.panel = Panel(PANEL_WIDTH, PANEL_HEIGHT, PANEL_COLOR, PANEL_ALPHA)
        self.panel.rect.midbottom = RECT.midbottom
        #self.panel.rect.move_ip(0, self.panel.rect.h)
        #self.panel.setup_effect('move', 2000, (0, -self.panel.rect.h))
        self.panel.add(self.panel_group)

    def setup_input(self):

        # General input handling, game inputs arnt set here but in player object
        self.actions[pg.K_ESCAPE] = lambda: self.set_done(c.SELECT_LEVEL, speed=self.game.speed)

    def set_done(self, next, **kwargs):

        # Call parent class (Screen) set_done function
        # Pass in next screen's name to display and
        # persistant data through kwargs dictionary
        super().set_done(next, **kwargs)

        # Set a countdown before state flip and apply effects
        # on panels sprites, with same or less duration as countdown
        self.final_countdown = c.BG_FADE_TIME

    def update(self, window, keys, elapsed):
        super().clear(window)
        super().update(window, keys, elapsed)
        self.panel_group.update(elapsed)
        self.all_groups = (self.panel_group,)
        for player in self.players:
            self.all_groups += player.update(self.panel, keys, elapsed)
        super().draw(window)
