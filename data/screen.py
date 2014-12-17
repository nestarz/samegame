#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from . import constants as c
from .graphics.surface import Image

class State:
    """Base class for all game states"""
    def __init__(self):
        self.done = False
        self.quit = False
        self.previous = None
        self.persist = {}

    def reinitialize(self):
        self.done = False

    def check_for_input(self, keys):
        pass


class Screen(State):
    """ Base class for all screen of the game """
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
        """ Reset screen to init """
        self.__init__()

    def start(self, window, persist):
        """Set the window"""
        self.persist = persist
        self.setup_background(window)
        self.setup_images(window)
        self.setup_buttons(window)

    def setup_background(self, window):
        """Set background and its effects"""
        img_name = self.name #retrieve bg_img from cache
        self.bg = Image(img_name) #create background to apply on window
        self.bg.resize(*c.SCREEN_SIZE) #resize bg to window size
        self.bg.setup_effect('fadein2', 1000) #'ll apply effect fadein during 1s

    def setup_images(self, window):
        """ Setting up all images of the screen """
        pass

    def setup_buttons(self, window):
        """ Setting up all buttons of the screen """
        pass

    def set_done(self, next, **kwargs):
        """ Setting up the end of the screen. """
        self.next = next #name of the next screen
        self.persist = kwargs #dict of persistent variable through screen flipping
        self.final_countdown = 0 #time until screen will flip is 0
        self.bg.setup_effect('fadeout', self.final_countdown)

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
