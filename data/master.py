#!/bin/python3

import pygame as pg
from . import setup
from . import cache

from .state import HomeScreen

class Master(setup.Window):
    def __init__(self):
        setup.Window.__init__(self)
        cache.init_cache()
        self.done = False                       #etat du programme
        self.clock = pg.time.Clock()            #horloge du programme
        self.fps = 30                           #frequence d'update
        self.current_time = 0.0                 #valeur du chronometre
        #TODO : Sortir d'un JSON les etats possibles du jeu
        self.states =   {
                            'home screen' : HomeScreen()
                        }
        self.state = self.states['home screen']
        #endTODO

    def update(self):
        """Met a jour le programme"""
        self.current_time = pg.time.get_ticks() #maj du chronometre
        if self.state.quit:                     #prog doit se terminer?
            self.done = True                    #le prog est termine
        elif self.state.done:                   #etat doit changer?
            self.flip_state()                   #changement d'etat
        self.state.update(self.surface)         #maj de l'etat

    def event_control(self):
        """Boucle des evenements"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def main(self):
        """Boucle principale du programme"""
        while not self.done:
            self.event_control()        #controle evenements ihm
            self.update()               #maj du prog
            pg.display.update()         #maj de la fenetre
            self.clock.tick(self.fps)   #si self.fps non depasse, attend


    def flip_state(self):
        """Change l'etat du programme"""
        pass
        #TODO : Changement d'etat
