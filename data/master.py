#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from . import setup
from . import cache


class Master(setup.Window):

    def __init__(self):
        super().__init__()
        self.done = False  # etat du programme
        self.clock = pg.time.Clock()  # horloge du programme
        self.fps = 120  # frequence d'update
        self.current_time = 0.0  # valeur du chronometre
        self.keys = pg.key.get_pressed()
        self.state_name = None
        self.state_dict = {}
        self.elapsed = 0.0

    def setup_state(self, state_dict, initial_state):
        self.state_dict = state_dict
        self.state_name = initial_state
        self.state = self.state_dict[self.state_name]
        self.state.start(self.surface, self.state.persist)

    def update(self):
        """Met a jour le programme"""

        self.current_time = pg.time.get_ticks()  # maj du chronometre
        if self.state.quit:  # prog doit se terminer?
            self.done = True  # le prog est termine
        elif self.state.done:
            self.flip_state()  # changement d'etat
        self.state.update(
            self.surface,
            self.keys,
            self.elapsed)  # maj de l'etat
        #if self.state.rects:
        #    pg.draw.rect(self.surface, (255,0,0), self.state.rects[0], 1)

    def event_loop(self):
        """Boucle des evenements"""

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

    def main_loop(self):
        """Boucle principale du programme"""

        while not self.done:
            self.event_loop()  # controle evenements ihm
            self.update()  # maj du prog
            pg.display.update(self.state.rects)  # maj de la fenetre
            fps = self.clock.get_fps()
            with_fps = '{} - {:.2f} FPS'.format(self.caption, fps)
            pg.display.set_caption(with_fps)
            self.elapsed = self.clock.tick_busy_loop(self.fps)

    def flip_state(self):
        """Change l'etat du programme"""

        previous = self.state_name
        self.state_name = self.state.next
        self.persist = self.state.persist
        self.state.reinitialize()
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        self.state.start(self.surface, self.persist)
