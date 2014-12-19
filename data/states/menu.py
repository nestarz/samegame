#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from .. import constants as c
from ..tools import render_text
from ..graphics.gfx import Image
from ..graphics.sprites import Panel, Button
from ..screen import Screen


class Menu(Screen):

    """Base class for all menu"""

    def __init__(self):
        # Call the parent class (Screen) constructor
        super().__init__()

        # Panel that will contain menu options
        self.option_panel = None

        # List that will contain menu options sprites
        self.option_list = []

        # Groups that will contain menu sprites
        self.panels = pg.sprite.LayeredDirty()
        self.buttons = pg.sprite.LayeredDirty()
        self.all_groups = (self.panels, self.buttons)

        # Dictionary that will contain action for user event
        self.actions = {}

        # Position of arrow, which focus button (0=first button)
        self.arrow_index = 0

    def start(self, window, persist):
        super().start(window, persist)
        self.setup_panels(window)
        self.setup_buttons()
        self.setup_input()

    def setup_panels(self, window):
        """ Setup raw panels used for menu options """

        # Panels constants
        HEIGHT = window.get_height()
        PANEL1_HEIGHT = HEIGHT / 5
        PANEL2_HEIGHT = HEIGHT / 13
        PANEL3_HEIGHT = HEIGHT - (PANEL1_HEIGHT + PANEL2_HEIGHT)
        PANEL_WIDTH = 435
        PANEL_COLOR1 = c.BLACK_RGB
        PANEL_COLOR2 = c.ORANGE_RGB

        # Create/decorate first panel sprite with logo and sublogo
        ALPHA = 135
        panel1 = Panel(PANEL_WIDTH, PANEL1_HEIGHT, PANEL_COLOR1, ALPHA)
        logo = Image(c.LOGOGFXNAME)
        logo.rect.centerx, logo.rect.y = panel1.rect.centerx, 30
        sublogo = Image(render_text(c.SUBLOGO_TEXT))
        sublogo.rect.centerx, sublogo.rect.y = panel1.rect.centerx, 85
        logo.draw(panel1.image); sublogo.draw(panel1.image)

        # Create/decorate second panel sprite with state description
        ALPHA = 190
        panel2 = Panel(PANEL_WIDTH + 10, PANEL2_HEIGHT, PANEL_COLOR2, ALPHA)
        desc = Image(render_text(self.description, 22, c.WHITE_RGB, c.FONT2, 1))
        desc.rect.midright = panel2.rect.midright
        desc.rect.x = desc.rect.x - 20
        desc.draw(panel2.image)

        # Create/decorate third panel sprite which'll contain choice option
        ALPHA = 120
        panel3 = Panel(PANEL_WIDTH, PANEL3_HEIGHT, c.BLACK_RGB, ALPHA)
        self.option_panel = panel3

        # Position pannels; Panels are next above each other
        panel1.rect.y = 0
        panel2.rect.y = PANEL1_HEIGHT
        panel3.rect.y = PANEL1_HEIGHT + PANEL2_HEIGHT

        # Each panel will move left to right using 'move' effect
        # Time duration is higher for lower panels (style effect)
        # Then, add panels to General Sprite DirtyLayer Group (sprites)
        for i, panel in enumerate((panel1, panel2, panel3)):
            panel.rect.x = -panel.image.get_width()
            EFFECT_TYPE = 'move'
            EFFECT_DURATION = 600 + i*10
            DISTANCE = (panel.image.get_width(), 0)
            panel.setup_effect(EFFECT_TYPE, EFFECT_DURATION, DISTANCE)
            panel.add(self.panels)

    def setup_buttons(self):
        """ Creating buttons """

        pass # Button creation is done by child menu

    def add_btn(self, text, callback):
        style = c.MENU_BTN_STYLE
        parent = self.option_panel
        btn = Button(text, style, callback, parent)
        btn.add(self.buttons)
        self.option_list.append(btn)

    def position_buttons(self):
        """ Place buttons on the right panel """

        MARGIN_Y = 15
        MARGIN_X = -25

        # Move each buttons above each other with
        # defined margin (MARGIN_X, MARGIN_Y)
        pos_y = 0 + MARGIN_Y
        pos_x = 0 + MARGIN_X
        for button in self.buttons:
            button.rect.move_ip(pos_x, pos_y)
            pos_y += button.rect.h + MARGIN_Y

    def set_done(self, next, **kwargs):
        """ Prepare the stop of the state and start a countdown """

        # Call parent class (Screen) set_done function
        # Pass in next screen's name to display and
        # persistant data through kwargs dictionary
        super().set_done(next, **kwargs)

        # Set a countdown before state flip and apply effects
        # on panels sprites, with same or less duration as countdown
        self.final_countdown = c.BG_FADE_TIME
        for i, p in enumerate(self.panels):
            EFFECT_TYPE = 'move'
            EFFECT_DURATION = 600 + i*10
            DISTANCE = (-p.image.get_width(), 0)
            p.setup_effect(EFFECT_TYPE, EFFECT_DURATION, DISTANCE)

    def move_arrow(self, direction):
        """ Move arrow to focus screen's button """

        # Warn button he will no more being targeted by the user
        button = self.option_list[self.arrow_index]
        button.targeted = False

        NB_BTN = len(self.option_list) # Button amount on screen
        i = self.arrow_index # Arrow position

        # Update arrow index as it never exceeds the number of button
        index = i+direction if -1 < i+direction < NB_BTN else NB_BTN-1-i
        self.arrow_index = index

        # Select focused button and warn he is targeted by the user
        button = self.option_list[self.arrow_index]
        button.targeted = True

        # Update action to add "press Return handling" with button
        # callback action when pressed. Nb: button.press is a method
        self.actions[pg.K_RETURN] = lambda: button.press()

    def setup_input(self):
        """ Setup event related action for menu navigation """

        # We warn first button he is focus
        button = self.option_list[self.arrow_index]
        button.targeted = True

        # K_UP is assigned to move arrow upward and
        # K_DOWN is assigned to move arrow downward
        self.actions[pg.K_UP] = lambda: self.move_arrow(-1)
        self.actions[pg.K_DOWN] = lambda: self.move_arrow(+1)

        # Each of self.action item is a function
        # which start when key (like K_RETURN) is pressed.
        button = self.option_list[self.arrow_index]
        self.actions[pg.K_RETURN] = lambda: button.press()

    def update(self, window, keys, elapsed):
        super().clear(window)
        super().update(window, keys, elapsed)
        self.panels.update(elapsed)
        self.buttons.update(elapsed)
        super().draw(window)

class Main(Menu):

    def __init__(self):
        super().__init__()
        self.name = c.MAIN_MENU
        self.next = c.SELECT_MODE
        self.back = c.HOME
        self.description = c.MAIN_MENU_DESCRIPTION

    def setup_buttons(self):
        super().add_btn(c.BTN_TEXT_NEWGAME, lambda: self.set_done(self.next))
        #super().add_btn(c.BTN_TEXT_CONTINUE, lambda: self.set_done(self.next))
        #super().add_btn(c.BTN_TEXT_LOADGAME, lambda: self.set_done(self.next))
        super().add_btn(c.BTN_TEXT_QUIT, lambda: self.set_done(c.HOME))
        super().position_buttons()


class ModeSelection(Menu):

    def __init__(self):
        super().__init__()
        self.name = c.SELECT_MODE
        self.next = c.SELECT_LEVEL
        self.back = c.MAIN_MENU
        self.description = c.SELECT_MODE_DESCRIPTION

    def setup_buttons(self):
        super().add_btn(c.BTN_TEXT_1P, lambda: self.set_done(self.next, nb_player=1))
        super().add_btn(c.BTN_TEXT_2P, lambda: self.set_done(self.next, nb_player=2))
        super().add_btn(c.BTN_TEXT_BACK, lambda: self.set_done(c.MAIN_MENU))
        super().position_buttons()

class LevelSelection(Menu):

    def __init__(self):
        super().__init__()
        self.name = c.SELECT_LEVEL
        self.next = c.ARCADE
        self.back = c.SELECT_MODE
        self.description = c.SELECT_LEVEL_DESCRIPTION

    def setup_buttons(self):
        for speed, name in c.MODE_NAME.items():
            super().add_btn(name, lambda: self.set_done(self.next, speed=speed))
        super().add_btn(c.BTN_TEXT_BACK, lambda: self.set_done(c.SELECT_MODE))
        super().position_buttons()
