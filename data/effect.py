#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from . import constants as ct
from .tools import Panel


class _Effect:

    """
    Base de chaque effet applicable a une surface.
    """

    def __init__(self, delay):
        self.init_delay = delay
        self.current_delay = self.init_delay
        self.display = True
        self.done = False
        self.first_apply = True

    def apply(
        self,
        elapsed,
        surface,
        rect,
        ):
        """
        Met a jour l'effet et l'applique a la surface.
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

    def apply(
        self,
        elapsed,
        surface,
        rect,
        ):
        self.sign1 = -self.sign1
        self.sign2 = -self.sign2
        rect = rect.move(self.sign1 * elapsed, self.sign2 * elapsed)


class Wait(_Effect):

    """
    Attend un certain temps avant d'afficher la surface.
    """

    def __init__(self, delay):
        super().__init__(delay)

    def apply(self, elapsed):
        if self.current_delay <= 0:
            self.display = True
            self.done = True
        elif self.current_delay > 0:
            self.display = False
            self.current_delay -= elapsed
        return self.display


class Blink(_Effect):

    """
    Scintillement de la surface avec un intervalle definit.
    """

    def __init__(self, delay):
        super().__init__(delay)

    def apply(
        self,
        elapsed,
        surface,
        rect,
        ):
        if self.current_delay <= 0:
            self.display = not self.display
            self.current_delay = self.init_delay
        elif self.current_delay > 0:
            self.current_delay -= elapsed
        return (surface, rect)


class FadeIn1(_Effect):

    """
    Fait varier de maniere decroissante la transparence de la surface
    en fonction de la duree restante de l'effet. Lorsque l'effet est
    termine la transparence initiale de la surface est totalement
    retablise.
    Uniquement pour les surface SANS transparence.
    set_alpha = False seulement en cas d'utilisation d'AA.
    """

    def __init__(self, delay, set_alpha=False):
        super().__init__(delay)
        self.set_alpha = set_alpha

    def apply(
        self,
        elapsed,
        surface,
        rect,
        ):
        if self.current_delay <= 0:
            self.alpha = 255
            self.done = True
        elif self.current_delay > 0:
            ratio = 1 - self.current_delay / self.init_delay
            self.alpha = ratio * 255
            if self.set_alpha:

                # /!\ marche seulement si AA=0

                surface.set_alpha(int(self.alpha))
            else:

                # /!\ marche seulement si AA=1

                self.apply_alpha(surface, self.alpha)
            self.current_delay -= elapsed
        return (surface, rect)

    def apply_alpha(self, surface, alpha):
        """
        Modifie le niveau de transparence pixel par pixel a une valeur
        alpha (Le pixel n'est pas modifie s'il est totalement
        transparent afin de garder la transparence globale de l'image)
        """

        for x in range(surface.get_width()):
            for y in range(surface.get_height()):
                color = surface.get_at((x, y))
                if color.a != 0:
                    color.a = min(int(alpha + 1), 255)
                surface.set_at((x, y), color)


class FadeIn2(_Effect):

    """
    Fait varier de maniere decroissante la transparence de la surface
    en fonction de la duree restante de l'effet. Lorsque l'effet est
    termine la transparence initiale de la surface est totalement
    retablise.
    Uniquement pour les surface SANS transparence.
    """

    def __init__(self, delay):
        super().__init__(delay)

    def apply(
        self,
        elapsed,
        surface,
        rect,
        ):
        ratio = max(0, self.current_delay) / self.init_delay
        self.alpha = int(ratio * 255)
        if self.first_apply:
            self.surface_init = surface.copy()
            self.first_apply = False
        if self.current_delay <= 0:
            surface = self.surface_init.copy()
            self.done = True
        else:
            surface = self.surface_init.copy()
            panel = pg.Surface(surface.get_size(), pg.SRCALPHA)
            self.panel = Panel(panel, surface, (0, 0, 0, self.alpha),
                               False)
            self.panel.fill((0, 0, 0, self.alpha))
            self.panel.draw()
        self.current_delay -= elapsed
        return (surface, rect)


class FadeOut(_Effect):

    """
    Fait varier de maniere croissante la transparence de la surface
    en fonction de la duree restante de l'effet. Lorsque l'effet est
    termine la transparence de la surface est totale.
    Uniquement pour les surface SANS transparence.
    """

    def __init__(self, delay):
        super().__init__(delay)

    def apply(
        self,
        elapsed,
        surface,
        rect,
        ):
        """
        Applique une surface transparente (alpha:20) sur la surface
        A MODIFIER pour tenir compte de self.alpha
        """

        ratio = self.current_delay / self.init_delay
        self.alpha = int(ratio * 255)
        if self.first_apply:
            panel = pg.Surface(surface.get_size(), pg.SRCALPHA)
            self.panel = Panel(panel, surface, (0, 0, 0, 20), False)
            self.first_apply = False
        if self.current_delay <= 0:
            self.panel.fill((0, 0, 0, 0))
            self.done = True
        else:
            self.panel.fill((0, 0, 0, 20))
            self.panel.draw()
        self.current_delay -= elapsed
        return (surface, rect)


class Move(_Effect):

    """
    Deplace la surface dans une direction et durant un temps definit.
    Le deplacement se base uniquement sur la duree de l'effet.
    A modifier pour permettre de decider du point d'arrive/depart,
    de la vitesse et ne plus dependre des fps.
    """

    def __init__(
        self,
        delay,
        distance,
        reversed_motion=False,
        ):
        super().__init__(delay)
        self.reversed_motion = reversed_motion
        self.distance = distance

    def step(
        self,
        elapsed,
        remaining_range,
        remaining_delay,
        ):
        return remaining_range / remaining_delay * elapsed

    def apply(
        self,
        elapsed,
        surface,
        rect,
        ):
        if self.current_delay > 0:
            if self.first_apply:
                if self.reversed_motion:
                    self.init_rect = rect.move(*self.distance)
                else:
                    self.init_rect = rect
                    rect = rect.move(*self.distance)
                self.first_apply = False
            ratio_y = self.step(elapsed, self.init_rect.y - rect.y,
                                self.current_delay)
            ratio_x = self.step(elapsed, self.init_rect.x - rect.x,
                                self.current_delay)
            ratio = (ratio_x, ratio_y)
            rect = rect.move(*ratio)
            self.current_delay -= elapsed
        elif self.current_delay <= 0:
            rect = self.init_rect
            self.done = True
        return (surface, rect)


EFFECTS_DICT = {
    'blink': Blink,
    'fadein1': FadeIn1,
    'fadein2': FadeIn2,
    'fadeout': FadeOut,
    'wait': Wait,
    'move': Move,
    }


