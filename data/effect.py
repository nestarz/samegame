#!/bin/python3

import pygame as pg
from . import constants as ct
from .tools import Panel

class _Effect():
    """
    Base de chaque effet applicable à une surface.
    """
    def __init__(self, delay):
        self.init_delay = delay
        self.current_delay = self.init_delay
        self.display = True
        self.done = False

    def apply(self, surface, rect):
        """
        Met à jour l'effet et l'applique à la surface.
        """
        pass

class Shake(_Effect):
    """
    Fait vibrer la surface.
    """
    def __init__(self, delay):
        super().__init__(delay)
        self.sign1 = 1
        self.sign2 = -1

    def apply(self, surface, rect):
        self.sign1 = - self.sign1
        self.sign2 = - self.sign2
        rect = rect.move(self.sign1*1,self.sign2*1)

class Wait(_Effect):
    """
    Attend un certain temps avant d'afficher la surface.
    """
    def __init__(self, delay):
        super().__init__(delay)

    def apply(self):
        if self.current_delay == 0:
            self.display = True
            self.done = True
        elif self.current_delay > 0:
            self.display = False
            self.current_delay -= 1
        return self.display

class Blink(_Effect):
    """
    Scintillement de la surface avec un intervalle définit.
    """
    def __init__(self, delay):
        super().__init__(delay)

    def apply(self, surface, rect):
        if self.current_delay == 0:
            self.display = not self.display
            self.current_delay = self.init_delay
        elif self.current_delay > 0:
            self.current_delay -= 1
        return surface, rect

class FadeIn1(_Effect):
    """
    Fait varier de manière décroissante la transparence de la surface
    en fonction de la durée restante de l'effet. Lorsque l'effet est
    terminé la transparence initiale de la surface est totalement
    rétablise.
    Uniquement pour les surface SANS transparence.
    set_alpha = False seulement en cas d'utilisation d'AA.
    """
    def __init__(self, delay, set_alpha=False):
        super().__init__(delay)
        self.set_alpha = set_alpha

    def apply(self, surface, rect):
        if self.current_delay == 0:
            self.alpha = 255
            self.done = True
        elif self.current_delay > 0:
            ratio = 1-(self.current_delay / self.init_delay)
            self.alpha = ratio*255
            if self.set_alpha:
                # /!\ marche seulement si AA=0
                surface.set_alpha(int(self.alpha))
            else:
                # /!\ marche seulement si AA=1
                self.apply_alpha(surface, self.alpha)
            self.current_delay -= 1
        return surface, rect

    def apply_alpha(self, surface, alpha):
        """
        Modifie le niveau de transparence pixel par pixel à une valeur
        alpha (Le pixel n'est pas modifié s'il est totalement
        transparent afin de garder la transparence globale de l'image)
        """
        for x in range(surface.get_width()):
            for y in range(surface.get_height()):
                color = surface.get_at((x, y))
                if color.a != 0:
                    color.a = min(int(alpha+1),255)
                surface.set_at((x, y), color)

class FadeIn2(_Effect):
    """
    Fait varier de manière décroissante la transparence de la surface
    en fonction de la durée restante de l'effet. Lorsque l'effet est
    terminé la transparence initiale de la surface est totalement
    rétablise.
    Uniquement pour les surface SANS transparence.
    """
    def __init__(self, delay):
        super().__init__(delay)

    def apply(self, surface, rect):
        ratio = (self.current_delay / self.init_delay)
        self.alpha = int(ratio*255)
        if self.current_delay == self.init_delay:
            self.surface_init = surface.copy()
        if self.current_delay == 0:
            surface = self.surface_init.copy()
            self.done = True
        else:
            surface = self.surface_init.copy()
            panel = pg.Surface(surface.get_size(), pg.SRCALPHA)
            self.panel = Panel(panel, surface, (0,0,0,self.alpha), False)
            self.panel.fill((0,0,0,self.alpha))
            self.panel.draw()
        self.current_delay -= 1
        return surface, rect

class FadeOut(_Effect):
    """
    Fait varier de manière croissante la transparence de la surface
    en fonction de la durée restante de l'effet. Lorsque l'effet est
    terminé la transparence de la surface est totale.
    Uniquement pour les surface SANS transparence.
    """
    def __init__(self, delay):
        super().__init__(delay)

    def apply(self, surface, rect):
        """
        Applique une surface transparente (alpha:20) sur la surface
        A MODIFIER pour tenir compte de self.alpha
        """
        ratio = (self.current_delay / self.init_delay)
        self.alpha = int(ratio*255)
        if self.current_delay == self.init_delay:
            panel = pg.Surface(surface.get_size(), pg.SRCALPHA)
            self.panel = Panel(panel, surface, (0,0,0,20), False)
        elif self.current_delay == 0:
            self.panel.fill((0,0,0,0))
            self.done = True
        else:
            self.panel.fill((0,0,0,20))
            self.panel.draw()
        self.current_delay -= 1
        return surface, rect

class Move(_Effect):
    """
    Déplace la surface dans une direction et durant un temps définit.
    Le déplacement se base uniquement sur la durée de l'effet.
    A modifier pour permettre de décider du point d'arrivé/départ,
    de la vitesse et ne plus dépendre des fps.
    """
    def __init__(self, delay, direction, mtype='move', speed=0):
        super().__init__(delay)
        self.direction = direction
        self.speed = speed
        self.mtype = mtype

    def apply(self, surface, rect):
        if self.mtype == 'move':
            if self.current_delay == 0:
                rect = self.init_rect
                self.done = True
            elif self.current_delay > 0:
                if self.current_delay == self.init_delay:
                    self.init_rect = rect
                    rect = rect.move(0,self.init_delay)
                ratio = 1-(self.current_delay / self.init_delay)
                rect = rect.move(*self.direction)
                self.current_delay -= 1
        if self.mtype == 'move2':
            if self.current_delay == 0:
                rect = self.init_rect
                self.done = True
            elif self.current_delay > 0:
                if self.current_delay == self.init_delay:
                    self.init_rect = rect
                    rect = rect.move(-surface.get_width(),0)
                rect = rect.move(
                    self.direction[0]*self.speed,
                    self.direction[1]*self.speed)
                self.current_delay -= 1
        if self.mtype == 'move3':
            if self.current_delay == 0:
                rect = self.init_rect
                self.done = True
            elif self.current_delay > 0:
                if self.current_delay == self.init_delay:
                    self.init_rect = rect
                rect = rect.move(
                    self.direction[0]*self.speed,
                    self.direction[1]*self.speed)
                self.current_delay -= 1
        return surface, rect

EFFECTS_DICT = {
            'blink': Blink,
            'fadein1': FadeIn1,
            'fadein2': FadeIn2,
            'fadeout': FadeOut,
            'wait': Wait,
            'move': Move
          }
