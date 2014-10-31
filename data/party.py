#!/bin/python3

import pygame as pg
from . import cache
from . import constants as ct
from . import tools as t

class Party(t.State):
    def __init__(self):
        super().__init__()
        self.name = 'arcade'
        self.buttons, self.images = dict(), dict()
        self.bg = None
        self.allow_input = False
        self.next = 'arcade'
        self.__arrow_index = 0
        self.time_down = 0
        self.to_set_done = -1

    def start(self, screen):
        self.setup_background(screen)
        self.setup_images(screen)
        self.setup_buttons(screen)

    def setup_background(self, screen):
        bg_img = cache._cache.images[self.name]
        self.bg = t.Image(bg_img, screen)
        self.bg.resize(*ct.SCREEN_SIZE)
        self.bg.setup_effect({'name':'fadeout2',
                'delay':20})

    def setup_images(self, screen):
        HEIGHT = screen.get_rect().h
        PANEL1_HEIGHT = HEIGHT/5 + 5
        PANEL2_HEIGHT = HEIGHT/13 + 5
        PANEL3_HEIGHT = HEIGHT - (PANEL1_HEIGHT + PANEL2_HEIGHT)


        panel1 = pg.Surface((435,PANEL1_HEIGHT), pg.SRCALPHA)
        panel1 = t.Panel(panel1, screen, (0,0,0,125), False)
        logo = t.Image(cache._cache.images['logo'], panel1.surface)
        logo.rect.centerx = panel1.rect.centerx
        logo.rect.y = 30
        sublogo = t.Image(t.text_to_surface(ct.AUTHOR, 'joystix', 10, ct.WHITE_RGB), panel1.surface)
        sublogo.rect.centerx = panel1.rect.centerx
        sublogo.rect.y = 85
        logo.draw()
        sublogo.draw()
        effect = {'name':'move2',
        'direction':ct.RIGHT,
        'delay':7,
        'speed':40}

        panel2 = pg.Surface((435,PANEL2_HEIGHT), pg.SRCALPHA)
        panel2 = t.Panel(panel2, screen, (255,255,255,70), False)
        menu_txt = 'Choose your Hero'.upper()
        menu_img = t.Image(t.text_to_surface(menu_txt, 'larabiefont', 20, ct.GREY_RGB, 1, True, True), panel2.surface)
        menu_img.rect.midright = panel2.rect.midright
        menu_img.rect.x = menu_img.rect.x - 20
        menu_img.draw()
        panel2.rect.y = PANEL1_HEIGHT
        panel2.setup_effect(effect)

        panel3 = pg.Surface((435,PANEL3_HEIGHT), pg.SRCALPHA)
        panel3 = t.Panel(panel3, screen, (0,0,0,50), True)
        panel3.rect.y = PANEL1_HEIGHT + PANEL2_HEIGHT
        panel3.setup_effect(effect)

        self.images['panel1'] = panel1
        self.images['panel2'] = panel2
        self.images['panel3'] = panel3

    def setup_buttons(self, screen):
        panel = self.images['panel3']

        txt = 'Perso1'.upper()
        callback = lambda : self.set_done(self.previous)
        arcade_btn = t.Button(panel.surface, txt, 'menu', callback)
        arcade_btn.rect.right = panel.rect.right
        arcade_btn.rect = arcade_btn.rect.move(-25,15)

        txt = 'Perso2'.upper()
        callback = lambda : self.set_done(self.previous)
        story_btn = t.Button(panel.surface, txt, 'menu', callback)
        story_btn.rect.right = panel.rect.right
        story_btn.rect = story_btn.rect.move(-25,63)

        txt = 'Perso3'.upper()
        callback = lambda : self.set_done(self.previous)
        versus_btn = t.Button(panel.surface, txt, 'menu', callback)
        versus_btn.rect.right = panel.rect.right
        versus_btn.rect = versus_btn.rect.move(-25,110)


        txt = 'Back'.upper()
        callback = lambda : self.set_done(self.previous)
        quit_btn = t.Button(panel.surface, txt, 'menu', callback)
        quit_btn.rect.right = panel.rect.right
        quit_btn.rect = quit_btn.rect.move(-25,155)


        self.buttons['arcade'] = arcade_btn
        self.buttons['story'] = story_btn
        self.buttons['versus'] = versus_btn
        self.buttons['quit'] = quit_btn
        self.btn_order = [arcade_btn, story_btn, versus_btn, quit_btn]

    def set_done(self, next):
        self.next = next
        panels = (self.images['panel2'], self.images['panel3'])
        for panel in panels:
            panel.setup_effect({'name':'move3',
        'direction':ct.LEFT,
        'delay':20,
        'speed':40})
        self.bg.setup_effect({'name':'fadein2',
                'delay':100})
        self.to_set_done = 20

    def check_for_input(self, keys):
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
        if (not keys[pg.K_DOWN]
            and not keys[pg.K_UP]
            and not keys[pg.K_RETURN]
            and not keys[pg.K_SPACE]
            and not keys[pg.K_ESCAPE]
            or (self.time_down > 4 and keys[pg.K_DOWN])
            or (self.time_down > 4 and keys[pg.K_UP])):
                self.allow_input = True
                self.time_down = 0
        else:
            self.time_down += 1
    @property
    def arrow_index(self):
        return self.__arrow_index

    @arrow_index.setter
    def arrow_index(self, value):
        """On cap l'index du curseur au nombre de choix"""
        if value in range(0,5):
            self.__arrow_index = value

    def do_action(self, index):
        if index in range(0, len(self.buttons)):
            self.btn_order[index].callback()

    def update(self, window, keys):
        self.check_for_input(keys)
        images = list()
        images.append(self.bg)
        images.extend(list(self.images.values()))
        for img in images:
            img.update()
        for btn in list(self.buttons.values()):
            btn.update(self.arrow_index, self.btn_order.index(btn))
        self.to_set_done -= 1
        if self.to_set_done == 0:
            self.done = True
