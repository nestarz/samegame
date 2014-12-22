#!/bin/python3
# -*- coding: utf-8 -*-
import pygame as pg

import samegame.constants as c
from samegame.graphics.general_sprites import Sprite
from samegame.graphics.gfx import Image
from samegame.screen import Screen
from samegame.tools import render_text


class Home(Screen):

    """ Intro scene """

    def __init__(self):
        # Call the parent class (Screen) constructor
        super().__init__()

        # Set screen name (defined in constants.py)
        self.name = c.HOME

        # Set default next screen name
        self.next = c.MAIN_MENU

        self.sprites = pg.sprite.LayeredDirty()
        self.all_groups = (self.sprites,)

    def start(self, window, persist):
        super().start(window, persist)
        self.setup_images(window)
        self.setup_input()

    def setup_images(self, window):
        """ Setup raw images used for home """

        # Panels constants
        MOVE_EFFECT_NAME = 'move'
        FADE_EFFECT_NAME = 'fade_alpha'  # WARNING: Unused, why ? TODO
        WAIT_EFFECT_NAME = 'wait'
        BLINK_EFFECT_NAME = 'blink'
        FONT_SIZE = 20

        window_rect = window.get_rect()
        # Create/decorate first panel sprite with logo and sublogo
        logo_img = Sprite(Image(c.LOGOGFXNAME))
        logo_img.setup_effect(MOVE_EFFECT_NAME, 1000, (0, -30))
        #logo_img.setup_effect(FADE_EFFECT_NAME, 1600)
        logo_img.rect.center = window_rect.center
        logo_img.rect.move_ip(0, 25)

        # Create/decorate first panel sprite with logo and sublogo
        sublogo_img = Sprite(render_text(c.SUBLOGO_TEXT))
        sublogo_img.setup_effect(WAIT_EFFECT_NAME, 800)
        #sublogo_img.setup_effect(FADE_EFFECT_NAME, 1500)
        sublogo_img.rect.center = window_rect.center
        sublogo_img.rect.move_ip(0, 30)

        # Create/decorate first panel sprite with logo and sublogo
        start_img = Sprite(render_text(c.START_TEXT, FONT_SIZE, bg_color=c.BLACK_RGB))
        start_img.setup_effect(BLINK_EFFECT_NAME, 500)
        start_img.setup_effect(WAIT_EFFECT_NAME, 1200)
        start_img.rect.centerx = window_rect.centerx
        start_img.rect.y = window_rect.bottom - 90

        # Add images to General Sprite DirtyLayer Group (sprites)
        for img in (start_img, logo_img, sublogo_img):
            img.add(self.sprites)

    def set_done(self, next, **kwargs):

        # Call parent class (Screen) set_done function
        # Pass in next screen's name to display and
        # persistant data through kwargs dictionary
        super().set_done(next, **kwargs)

        # Set a countdown before state flip and apply effects
        # on sprites, with same duration as countdown
        self.final_countdown = 1000
        for spr in self.sprites:
            distance = (0, spr.rect.h)  # WARNING : UNUSED, WHY? TODO
            #spr.setup_effect('fadeout', self.final_countdown)
            #spr.setup_effect('move', self.final_countdown, distance)

    def setup_input(self):
        """ Setup event related action for menu navigation """

        # Each of self.action item is a function
        # which start when key (like K_RETURN) is pressed. TODO : Must it be put in the doc?
        self.actions[pg.K_RETURN] = lambda: self.set_done(self.next)

    def update(self, window, keys, elapsed):
        super().clear(window)
        super().update(window, keys, elapsed)
        self.sprites.update(elapsed)
        super().draw(window)
