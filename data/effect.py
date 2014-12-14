#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from . import constants as ct
from .tools import Panel, text_to_surface

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
        self.pause = False
        self.backup_img = None
        self.backup_rect = None
        self.priority = 0

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

    def stop(self):
        pass

    def resume(self):
        pass

    def backup(self):
        return self.backup_img, self.backup_rect

class TextEffect1(_Effect):

    """
    Hue variation effect and arrow index mark.
    """
    def __init__(self, delay, step, style, txt):
        super().__init__(delay)
        self.txt = txt
        self.sign = 1
        self.time_stacker = 0
        self.targeted = False
        self.arrow_txt = ''
        self.style = style
        self.style_hover = style.get('hover', 'default')

    def apply(
        self,
        elapsed,
        surface,
        rect,
    ):
        if self.first_apply:
            self.backup_img = surface.copy()
            self.backup_rect = rect.copy()
            self.color = self.temp_c = self.style_hover['color']
            self.start = False
            self.sign = 1
            self.time_stacker = 0
            self.first_apply = False
        else:
            self.arrow_txt = '+' if self.arrow_txt == '*' else '*'
            if self.time_stacker > 300:
                self.sign = -1*self.sign
                self.time_stacker = 0
            step = 1
            self.temp_c = [x - self.sign*step for x in self.temp_c]
            self.color = [max(0, min(x - self.sign*step, 255))
                                    for x in self.temp_c]
            self.time_stacker += elapsed
        i = text_to_surface(
                self.txt + self.arrow_txt,
                self.style['font'],
                self.style['size'],
                self.color,
                self.style['AA'],
                self.style['bold'])
        return (i, rect)

    def stop(self):
        self.pause = True

    def resume(self):
        self.pause = False

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
            self.panel = Panel(surface.get_size(), (0, 0, 0, self.alpha))
            surface.blit(self.panel.image, (0,0))
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
            self.panel = Panel(surface.get_size(), (0, 0, 0, 20))
            self.first_apply = False
        if self.current_delay <= 0:
            self.panel.image.fill((0, 0, 0, 0))
            self.done = True
        else:
            self.panel.image.fill((0, 0, 0, 20))
            surface.blit(self.panel.image, (0,0))
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
        priority=0,
        reversed_motion=False,

    ):
        super().__init__(delay)
        self.reversed_motion = reversed_motion
        self.distance = distance
        self.priority = priority

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
                    self.dest_rect = rect
                else:
                    self.init_rect = rect
                    self.dest_rect = rect.move(*self.distance)
                self.first_apply = False
            ratio_y = self.step(elapsed, -self.init_rect.y + self.dest_rect.y,
                                self.current_delay)
            ratio_x = self.step(elapsed, -self.init_rect.x + self.dest_rect.x,
                                self.current_delay)
            ratio = (ratio_x, ratio_y)
            rect.move_ip(*ratio)
            self.current_delay -= elapsed
        elif self.current_delay <= 0:
            rect = self.init_rect if self.reversed_motion else self.dest_rect
            self.done = True
        return (surface, rect)


EFFECTS_DICT = {
    'blink': Blink,
    'fadein1': FadeIn1,
    'fadein2': FadeIn2,
    'fadeout': FadeOut,
    'wait': Wait,
    'move': Move,
    'txt_effect1': TextEffect1
}
