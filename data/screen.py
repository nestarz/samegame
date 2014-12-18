#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from . import constants as c
from .graphics.gfx import Image

class State:
    """Base class for all game states"""
    def __init__(self):
        self.done = False
        self.quit = False
        self.previous = None
        self.persist = {}

    def reinitialize(self):
        self.done = False

    def check_input(self, keys):
        pass


class Screen(State):
    """ Base class for all screen of the game """

    BG_FADE_TIME = c.BG_FADE_TIME

    def __init__(self):
        super().__init__()
        self.name = ''
        self.next = ''
        self.bg = None

        # Dictionary that will contain action for user event
        self.actions = {}

        self.final_countdown = 0
        self.input_timer = 0
        self.sprites = pg.sprite.LayeredDirty()
        self.rects = []

    def reinitialize(self):
        """ Reset screen to init """
        self.__init__()

    def start(self, window, persist):
        """Set the window"""
        self.persist = persist
        self.setup_background(window)

    def setup_background(self, window):
        """Set background and its effects"""
        img_name = self.name #retrieve bg_img from cache
        self.bg = Image(img_name) #create background to apply on window
        self.bg.resize(*window.get_size()) #resize bg to window size
        self.bg.setup_effect('fadein', Screen.BG_FADE_TIME) #'ll apply effect fadein during 1s

    def set_done(self, next, **kwargs):
        """ Setting up the end of the screen. """
        self.next = next #name of the next screen
        self.persist = kwargs #dict of persistent variable through screen flipping
        self.final_countdown = 0 #time until screen will flip is 0
        self.bg.setup_effect('fadeout', Screen.BG_FADE_TIME)

    def check_input(self, keys, elapsed):
        """ Check for user events """

        # Check 70ms after last key press if self.actions keys
        # are pressed then launches the corresponding action
        if self.input_timer > 300:
            for index, function in self.actions.items():
                if keys[index]:
                    function()
                    self.input_timer = 0
        self.input_timer += elapsed

    def update(
        self,
        window,
        keys,
        elapsed,
    ):
        self.elapsed = elapsed #on récup le temps passé depuis le dernier up
        self.check_input(keys, elapsed) #on check les evenements de l'user
        self.bg.update(elapsed)
        rect = self.bg.draw(window)
        self.sprites.clear(window, self.bg.image)
        self.sprites.update(elapsed)
        self.rects = self.sprites.draw(window) #on affiche sur la fenetre les sprites
        if rect:
            self.rects.append(rect)
        if self.final_countdown:
            #si on a demandé à ce que l'event se termine
            #on up puis check le timer de fin
            self.final_countdown -= self.elapsed
            self.done = max(0, self.final_countdown) == 0

    def do_action(self, index):
        """Lance l'action du boutton ciblé par par l'index"""
        if index in range(0, len(self.buttons)):
            self.buttons[index].callback()
