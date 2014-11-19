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

    def setup_images(self, screen):
        HEIGHT = screen.get_rect().h
        PANEL1_HEIGHT = HEIGHT / 5 + 5
        PANEL2_HEIGHT = HEIGHT / 13 + 5
        PANEL3_HEIGHT = HEIGHT - (PANEL1_HEIGHT + PANEL2_HEIGHT)

        panel1 = pg.Surface((435, PANEL1_HEIGHT), pg.SRCALPHA)
        panel1 = t.Panel(panel1, screen, (0, 0, 0, 135), False)
        logo = t.Image(cache._cache.images['logo'], panel1.surface)
        logo.rect.centerx = panel1.rect.centerx
        logo.rect.y = 30
        sublogo = t.Image(t.text_to_surface(c.AUTHOR, 'joystix', 10,
                          c.WHITE_RGB), panel1.surface)
        sublogo.rect.centerx = panel1.rect.centerx
        sublogo.rect.y = 85
        logo.draw()
        sublogo.draw()
        panel1.setup_effect('move', 700, (-panel1.surface.get_width(),
                            0))

        panel2 = pg.Surface((435 + 10, PANEL2_HEIGHT), pg.SRCALPHA)
        panel2 = t.Panel(panel2, screen, (253, 84, 72, 190), False)
        menu_img = t.Image(t.text_to_surface(
            self.description.upper(),
            'larabiefont',
            23,
            c.WHITE_RGB,
            1,
            True,
            False,
            ), panel2.surface)
        menu_img.rect.midright = panel2.rect.midright
        menu_img.rect.x = menu_img.rect.x - 20
        menu_img.draw()
        panel2.rect.y = PANEL1_HEIGHT
        panel2.setup_effect('move', 700, (-panel2.surface.get_width(),
                            0))

        panel3 = pg.Surface((435, PANEL3_HEIGHT), pg.SRCALPHA)
        panel3 = t.Panel(panel3, screen, (0, 0, 0, 120), True)
        panel3.rect.y = PANEL1_HEIGHT + PANEL2_HEIGHT
        panel3.setup_effect('move', 700, (-panel3.surface.get_width(),
                            0))

        self.images.append(panel1)
        self.images.append(panel2)
        self.images.append(panel3)

    def setup_buttons(self, screen):
        y = 15
        for button in self.buttons:
            if button.surfaceToDrawTo == self.images[2].surface:
                button.rect.right = self.images[2].rect.right
                button.rect = button.rect.move(-25, y)
                y += 48

    def set_done(self, next):
        super().set_done(next)
        self.to_set_done = True
        self.to_set_done_timer = 700
        for panel in self.images:
            panel.setup_effect('move', 700,
                               (-panel.surface.get_width(), 0), True)
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
        self.allow_input = False
        if not keys[pg.K_DOWN] and not keys[pg.K_UP] \
            and not keys[pg.K_RETURN] and not keys[pg.K_SPACE] \
            and not keys[pg.K_ESCAPE] or self.allow_input_timer > 500 \
            and keys[pg.K_DOWN] or self.allow_input_timer > 500 \
            and keys[pg.K_UP]:
            self.allow_input = True
            self.allow_input_timer = 0

    @property
    def arrow_index(self):
        return self.__arrow_index

    @arrow_index.setter
    def arrow_index(self, value):
        """On cap l'index du curseur au nombre de choix"""

        if value in range(0, 5):
            self.__arrow_index = value


class Main(Menu):

    def __init__(self):
        super().__init__()
        self.name = c.MAIN_MENU
        self.next = c.SELECT_MODE
        self.description = 'Main Menu'

    def setup_buttons(self, screen):
        surface_to_draw_to = self.images[2].surface
        btn_style_name = 'menu'
        btns = []

        btns.extend((('Continue', lambda : \
                    self.set_done(c.SELECT_MODE)), ('New Game',
                    lambda : self.set_done(c.SELECT_MODE)), ('Load Game'
                    , lambda : self.set_done(c.SELECT_MODE)), ('quit',
                    lambda : self.set_done(c.HOME))))

        for btn in btns:
            self.buttons.append(t.Button(surface_to_draw_to, btn[0],
                                btn_style_name, btn[1]))

        super().setup_buttons(screen)


class ModeSelection(Menu):

    def __init__(self):
        super().__init__()
        self.name = c.SELECT_MODE
        self.next = c.SELECT_CHAR
        self.description = 'Selection du Mode'

    def setup_buttons(self, screen):
        surface_to_draw_to = self.images[2].surface
        btn_style_name = 'menu'
        btns = []

        btns.extend((('story', lambda : self.set_done(c.SELECT_CHAR)),
                    ('arcade', lambda : self.set_done(c.SELECT_CHAR)),
                    ('versus', lambda : self.set_done(c.SELECT_CHAR)),
                    ('back', lambda : self.set_done(self.previous))))

        for btn in btns:
            self.buttons.append(t.Button(surface_to_draw_to, btn[0],
                                btn_style_name, btn[1]))

        super().setup_buttons(screen)


class CharacterSelection(Menu):

    def __init__(self):
        super().__init__()
        self.name = c.SELECT_CHAR
        self.next = c.ARCADE
        self.description = 'Choose your Hero'

    def setup_buttons(self, screen):
        surface_to_draw_to = self.images[2].surface
        btn_style_name = 'menu'
        btns = []

        btns.extend((('Perso1', lambda : self.set_done(self.next)),
                    ('Perso2', lambda : self.set_done(self.next)),
                    ('Perso3', lambda : self.set_done(self.next)),
                    ('back', lambda : self.set_done(self.previous))))

        for btn in btns:
            self.buttons.append(t.Button(surface_to_draw_to, btn[0],
                                btn_style_name, btn[1]))

        super().setup_buttons(screen)




