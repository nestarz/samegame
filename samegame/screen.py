#!/bin/python3
# -*- coding: utf-8 -*-

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
        self.all_groups = ()
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
        img_name = self.name
        self.bg = Image(img_name)
        self.bg.resize(*window.get_size())
        self.bg.setup_effect('fadein', Screen.BG_FADE_TIME)

    def do_action(self, index):
        """Lance l'action du boutton ciblé par par l'index"""
        if index in range(0, len(self.buttons)):
            self.buttons[index].callback()

    def set_done(self, next_, **kwargs):
        """ Setting up the end of the screen. """
        self.next = next_
        self.persist = kwargs
        self.final_countdown = 0
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

    def draw(self, window):
        rect = self.bg.draw(window)  # draw only if effects apply
        if rect:
            self.rects.append(rect)
        for group in self.all_groups:
            self.rects.extend(group.draw(window))  # get rects where sprites have blitted

    def clear(self, window):
        for group in self.all_groups:
            group.clear(window, self.bg.image)
            break

    def update(self, window, keys, elapsed):
        self.rects = []
        self.elapsed = elapsed
        self.check_input(keys, elapsed)
        self.bg.update(elapsed)
        if self.final_countdown:
            self.final_countdown -= self.elapsed
            self.done = max(0, self.final_countdown) == 0
