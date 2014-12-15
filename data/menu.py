#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from . import cache
from . import constants as c
from . import tools as t


class Menu(t.Screen):

    def __init__(self):
        super().__init__()
        self.__arrow_index = 0
        self.panels = []
        self.buttons = []

    def setup_images(self, screen):
        HEIGHT = screen.get_rect().h
        PANEL1_HEIGHT = HEIGHT / 5 + 5
        PANEL2_HEIGHT = HEIGHT / 13 + 5
        PANEL3_HEIGHT = HEIGHT - (PANEL1_HEIGHT + PANEL2_HEIGHT)

        panel1 = t.Panel((435, PANEL1_HEIGHT), (0, 0, 0, 135))
        logo = t.Image(cache._cache.images['logo'], panel1.image)
        logo.rect.centerx = panel1.rect.centerx
        logo.rect.y = 30
        sublogo = t.Image(t.text_to_surface(c.AUTHOR, 'joystix', 10,
                                            c.WHITE_RGB), panel1.image)
        sublogo.rect.centerx = panel1.rect.centerx
        sublogo.rect.y = 85
        logo.draw()
        sublogo.draw()

        panel2 = t.Panel((435 + 10, PANEL2_HEIGHT), (253, 84, 72, 190))
        menu_img = t.Image(t.text_to_surface(
            self.description.upper(),
            'larabiefont',
            23,
            c.WHITE_RGB,
            1,
            True,
            False,
        ), panel2.image)
        menu_img.rect.midright = panel2.rect.midright
        menu_img.rect.x = menu_img.rect.x - 20
        menu_img.draw()
        panel2.rect.y = PANEL1_HEIGHT

        panel3 = t.Panel((435, PANEL3_HEIGHT), (0, 0, 0, 120))
        panel3.rect.y = PANEL1_HEIGHT + PANEL2_HEIGHT

        for panel in (panel1, panel2, panel3):
            panel.rect.x = -panel.image.get_width()
            panel.setup_effect('move', 600, (panel.image.get_width(), 0))
            self.panels.append(panel)
            panel.add(self.sprites)

    def setup_buttons(self, screen):
        """Création des bouttons (par les menu enfants)"""
        pass

    def position_buttons(self):
        """Place les bouttons sur le panel adéquat"""
        y = 15
        for button in self.buttons:
            button.rect = button.rect.move(-25, y)
            y += 48

    def set_done(self, next, **kwargs):
        super().set_done(next, **kwargs)
        self.to_set_done = True
        self.to_set_done_timer = 600
        for panel in self.panels:
            panel.setup_effect('move', 600,
                               (-panel.image.get_width(), 0), 0)
        self.bg.setup_effect('fadeout', 1000)

    def check_for_input(self, keys):
        self.allow_input_timer += self.elapsed
        if self.allow_input:
            if keys[pg.K_UP]:
                if self.arrow_index == 0:
                    self.arrow_index = len(self.buttons)
                self.arrow_index -= 1
            elif keys[pg.K_DOWN]:
                self.arrow_index += 1
                if self.arrow_index == len(self.buttons):
                    self.arrow_index = 0
            elif keys[pg.K_RETURN] or keys[pg.K_SPACE]:
                self.do_action(self.arrow_index)
            elif keys[pg.K_ESCAPE]:
                self.set_done(self.previous)
        self.buttons[self.arrow_index].targeted = True
        self.allow_input = False
        if not keys[pg.K_DOWN] and not keys[pg.K_UP] \
                and not keys[pg.K_RETURN] and not keys[pg.K_SPACE] \
                and not keys[pg.K_ESCAPE] or self.allow_input_timer > 500 \
                and keys[pg.K_DOWN] or self.allow_input_timer > 500 \
                and keys[pg.K_UP]:
            self.allow_input = True
            self.allow_input_timer = 0

    def add_btn(self, text, callback):
        style = 'menu'
        group = self.sprites
        parent = self.panels[2]
        btn = t.Button(text, style, callback, parent)
        self.buttons.append(btn)
        btn.add(group)

    @property
    def arrow_index(self):
        return self.__arrow_index

    @arrow_index.setter
    def arrow_index(self, value):
        """On cap l'index du curseur au nombre de choix + 1"""

        if value in range(0, len(self.buttons)+1):
            self.__arrow_index = value


class Main(Menu):

    def __init__(self):
        super().__init__()
        self.name = c.MAIN_MENU
        self.next = c.SELECT_MODE
        self.description = 'Main Menu'

    def setup_buttons(self, screen):
        super().add_btn('Continue', lambda: self.set_done(c.SELECT_MODE))
        super().add_btn('New Game', lambda: self.set_done(c.SELECT_MODE))
        super().add_btn('Load Game', lambda: self.set_done(c.SELECT_MODE))
        super().add_btn('Quit', lambda: self.set_done(c.HOME))
        super().position_buttons()


class ModeSelection(Menu):

    def __init__(self):
        super().__init__()
        self.name = c.SELECT_MODE
        self.next = c.SELECT_CHAR
        self.description = 'Selection du Mode'

    def setup_buttons(self, screen):
        super().add_btn('Easy', lambda: self.set_done(c.SELECT_CHAR, speed=1))
        super().add_btn('Normal', lambda: self.set_done(c.SELECT_CHAR, speed=2))
        super().add_btn('Hard', lambda: self.set_done(c.SELECT_CHAR, speed=3))
        super().add_btn('Inferno', lambda: self.set_done(c.SELECT_CHAR, speed=4))
        super().add_btn('Back', lambda: self.set_done(c.MAIN_MENU))
        super().position_buttons()


class CharacterSelection(Menu):

    def __init__(self):
        super().__init__()
        self.name = c.SELECT_CHAR
        self.next = c.ARCADE
        self.description = 'Choose your Hero'

    def setup_buttons(self, screen):
        super().add_btn('Developper', lambda: self.set_done(self.next, speed=self.persist.get('speed',2)))
        super().add_btn('Back', lambda: self.set_done(c.SELECT_MODE))
        super().position_buttons()
