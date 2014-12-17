#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from . import constants as c
from .tools import Panel, Image, render_text
from .screen import Screen


class Menu(Screen):
    """Base class for all menu"""

    def __init__(self):
        # Call the parent class (Screen) constructor
        super().__init__()

        # Groups that will contain menu sprites
        self.panels = pg.sprite.LayeredDirty()
        self.buttons = pg.sprite.LayeredDirty()

        # Dictionary that will contain action for user event
        self.action = {}

    def setup_panels(self, screen):
        """ Setup raw panels used for menu options """

        # Panels constants
        HEIGHT = screen.get_rect().h
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
        sublogo = render_text(c.SUBLOGOTEXT, c.FONT1, 10)
        sublogo.rect.centerx, sublogo.rect.y = panel1.rect.centerx, 85
        logo.draw(panel1); sublogo.draw(panel1)

        # Create/decorate second panel sprite with state description
        ALPHA = 190
        panel2 = Panel(PANELWIDTH + 10, PANEL2_HEIGHT, PANEL_COLOR2, ALPHA)
        desc = render_text(self.description, c.FONT2, 23)
        desc.rect.midright = panel2.rect.midright
        desc.rect.x = desc.rect.x - 20
        desc.draw(panel2)

        # Create/decorate third panel sprite which'll contain choice option
        ALPHA = 120
        panel3 = Panel(PANEL_WIDTH, PANEL3_HEIGHT, c.BLACK_RGB, ALPHA)

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

    def setup_buttons(self, screen):
        """ Creating buttons """

        pass # Button creation is done by child menu

    def add_btn(self, text, callback):
        style = c.MENU_BTN_STYLE
        parent = self.panels[2]
        btn = Button(text, style, callback, parent)
        btn.add(self.buttons)

    def position_buttons(self):
        """ Place buttons on the right panel """

        MARGIN_Y = 15
        MARGIN_X = -25

        # Move each buttons above each other with
        # defined margin (MARGIN_X, MARGIN_Y)
        pos_y = 0 + MARGIN_Y
        pos_x = 0 + MARGIX_X
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
        # on panels sprites with same or less duration as countdown
        self.final_countdown = 600
        for i, p in enumerate(self.panels):
            EFFECT_TYPE = 'move'
            EFFECT_DURATION = self.final_countdown - i*10
            DISTANCE = (-p.image.get_width(), 0)
            p.setup_effect(EFFECT_TYPE, EFFECT_DURATION, DISTANCE)

    def move_arrow(self, direction):
        """ Move arrow to focus screen's button """

        NB_BTN = len(self.buttons) # Button amount on screen
        i = self.arrow_index # Arrow position

        # Update arrow index as it never exceeds the number of button
        self.arrow_index = max(0, min(i+direction, NB_BTN))

        # Warn button he is targeted by the user
        button = self.buttons[self.arrow_index]
        button.targeted = True

        # Update action to add "press Return handling" with button
        # callback action when pressed. Nb: button.press is a method
        self.action[pg.K_RETURN] = lambda: button.press()

    def setup_input_action(self):
        """ Setup event related action for menu navigation """

        # K_UP is assigned to move arrow upward and
        # K_DOWN is assigned to move arrow downward
        self.action[pg.K_UP] = lambda: self.move_arrow(1)
        self.action[pg.K_DOWN] = lambda: self.move_arrow(-1)

        # Each of self.action item is a function
        # which start when key (like K_RETURN) is pressed.
        button = self.buttons[self.arrow_index]
        self.action[pg.K_RETURN] = lambda: button.press()

    def check_for_input(self, keys, elapsed):
        """ Check for user events """

        # Check 70ms after last key press if self.actions keys
        # are pressed then launches the corresponding action
        if self.input_timer > 70:
            for index, function in dic.items():
                if keys[index]:
                    actions[index]()
                    self.input_timer = 0
        self.input_timer += elapsed


class Main(Menu):

    def __init__(self):
        super().__init__()
        self.name = c.MAIN_MENU
        self.next = c.SELECT_MODE
        self.back = c.HOME
        self.description = c.MAIN_MENU_DESCRIPTION

    def setup_buttons(self, screen):
        super().add_btn(c.BTN_TEXT_CONTINUE, lambda: self.set_done(c.SELECT_MODE))
        super().add_btn(c.BTN_TEXT_NEWGAME, lambda: self.set_done(c.SELECT_MODE))
        super().add_btn(c.BTN_TEXT_LOADGAME, lambda: self.set_done(c.SELECT_MODE))
        super().add_btn(c.BTN_TEXT_QUIT, lambda: self.set_done(c.HOME))
        super().position_buttons()


class ModeSelection(Menu):

    def __init__(self):
        super().__init__()
        self.name = c.SELECT_MODE
        self.next = c.SELECT_CHAR
        self.back = c.MAIN_MENU
        self.description = c.SELECT_MODE_DESCRIPTION

    def setup_buttons(self, screen):
        super().add_btn(c.BTN_TEXT_EASY, lambda: self.set_done(c.SELECT_CHAR, speed=1))
        super().add_btn(c.BTN_TEXT_NORMAL, lambda: self.set_done(c.SELECT_CHAR, speed=2))
        super().add_btn(c.BTN_TEXT_HARD, lambda: self.set_done(c.SELECT_CHAR, speed=3))
        super().add_btn(c.BTN_TEXT_INFERNO, lambda: self.set_done(c.SELECT_CHAR, speed=4))
        super().add_btn(c.BTN_TEXT_BACK, lambda: self.set_done(c.MAIN_MENU))
        super().position_buttons()


class CharacterSelection(Menu):

    def __init__(self):
        super().__init__()
        self.name = c.SELECT_CHAR
        self.next = c.ARCADE
        self.back = c.SELECT_MODE
        self.description = c.SELECT_CHAR_DESCRIPTION

    def setup_buttons(self, screen):
        super().add_btn(c.BTN_TEXT_DEV, lambda: self.set_done(self.next, speed=self.persist.get('speed',2)))
        super().add_btn(c.BTN_TEXT_BACK, lambda: self.set_done(c.SELECT_MODE))
        super().position_buttons()
