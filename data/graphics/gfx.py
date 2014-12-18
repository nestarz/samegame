#!/bin/python3
# -*- coding: utf-8 -*-

import pygame as pg
from ..cache import cache
from .. import constants as c
from ..tools import render_text

class SuperSurface:

    def __init__(self, surface):
        self.image = surface
        self.rect = self.image.get_rect()
        self.effect_dict = {}
        self.visible = 1
        self.dirty = 1

    def resize(self, w, h):
        self.image = pg.transform.scale(self.image, (int(w), int(h)))
        self.rect = self.image.get_rect()

    def setup_effect(self, name, *args):
        self.effect_dict[name] = self.effect_dict.get(name, [])
        Effect = EffectObject.get_child(name)
        self.effect_dict[name].append(Effect(*args))

    def pause_effect(self, name):
        for e in self.effect_dict[name]:
            e.stop()

    def resume_effect(self, name):
        for e in self.effect_dict[name]:
            e.resume()

    def update(self, elapsed):
        for n, elist in self.effect_dict.items():
            for e in elist:
                self.image, self.rect = e.apply(elapsed, self.image, self.rect)
                self.visible = 1 if e.visible else 0
                if e.done:
                    elist.remove(e)
                if e.priority == 1 and not e.pause:
                    break


class Image(SuperSurface):
    """ Is not a sprite ! Usefull for once upon time blit and background """

    def __init__(self, image):

        # If string is passed in arg, will try to get
        # it in cache, otherwise an error will rise
        if isinstance(image, str):
            # Get/Load the image in cache
            image = cache.get_image(image)

        # Check that image is now a pygame Surface
        assert isinstance(image, pg.Surface)

        # Call the parent class (SuperSurface) constructor
        # with our image passed in arg as a pygame Surface
        super().__init__(image)

    def update(self, elapsed):

        # Image isn't a Sprite, so we must update rect manually
        self.rect = self.image.get_rect()

        # If effects will apply we should draw our image
        # Then, we check if there is no empty list effect
        # in our dictionnary of effect (effect_dict)
        self.dirty = 0
        for l in self.effect_dict.values():
            if l: self.dirty = 1; break

        # Call the parent class (SuperSurface) constructor
        # with time elapsed since previous game update
        SuperSurface.update(self, elapsed)

    def draw(self, dest, force=False):

        # If Image wants to be drawn and be visible,
        # or if force option is up then we will draw it
        if (self.visible and self.dirty) or force:
            dest.blit(self.image, self.rect)

            # Return rect where image have been drawn
            return self.rect


#########################

# Effects

class AccessEffectError(Exception): pass

class EffectObject:

    """
    Base of each effect
    """

    def __init__(self, delay):
        assert delay > 0
        self.init_delay = delay #time duration of effect
        self.current_delay = self.init_delay #remaining time before effect ending
        self.visible = True #False=img will not be displayed
        self.done = False #effect is done
        self.first_apply = True
        self.pause = False #True=effect will not apply
        self.backup_img = None #img initial
        self.backup_rect = None #rect initial
        self.priority = 0 #1=other effects will wait until end of this one

    def apply(
        self,
        elapsed,
        surface,
        rect,
    ):
        """
        Update effect and applies it to the surface and rect.
        """
        pass

    def stop(self):
        """ Stop of the current effect """
        pass

    def resume(self):
        """ Resume of the current effect """
        pass

    def backup(self):
        """ Return initial surface and rect """
        return self.backup_img, self.backup_rect

    @classmethod
    def get_child(cls, name):
        try:
            return {
                'blink': Blink,
                'fade_alpha': FadeAlpha,
                'fadein': FadeIn,
                'fadeout': FadeOut,
                'wait': Wait,
                'move': Move,
                'text_effect': TextEffect,
                'inflate': Inflate
            }[name]
        except KeyError:
            raise AccessEffectError(name)

class TextEffect(EffectObject):

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

    def apply(
        self,
        elapsed,
        surface,
        rect,
    ):
        super().apply(elapsed, surface, rect)
        if self.first_apply:
            self.backup_img = surface.copy()
            self.backup_rect = rect.copy()
            self.color = self.temp_c = self.style.get('color2', c.ORANGE_RGB)
            self.start = False
            self.sign = 1
            self.time_stacker = 0
            self.first_apply = False
        elif self.pause:
            return self.backup_img, self.backup_rect
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
        i = render_text(
                self.txt + self.arrow_txt,
                self.style['size'],
                self.color,
                self.style['font'],
                self.style.get('AA', 0),
                self.style.get('bold',False))
        return (i, rect)

    def stop(self):
        self.pause = True

    def resume(self):
        self.pause = False

class Shake(EffectObject):

    """
    Vibrates the surface
    """

    def __init__(self, delay):
        super().__init__(delay)
        self.sign1 = 1
        self.sign2 = -1

    def apply(self, elapsed, surface, rect):
        super().apply(elapsed, surface, rect)
        self.sign1 = -self.sign1
        self.sign2 = -self.sign2
        rect = rect.move(self.sign1 * elapsed, self.sign2 * elapsed)


class Wait(EffectObject):

    """
    Waiting for a time before displaying the surface
    """

    def __init__(self, delay):
        super().__init__(delay)

    def apply(self, elapsed, surface, rect):
        super().apply(elapsed, surface, rect)
        if self.current_delay <= 0:
            self.visible = True
            self.done = True
        elif self.current_delay > 0:
            self.visible = False
            self.current_delay -= elapsed
        return surface, rect


class Blink(EffectObject):

    """
    Sparkling surface with an interval defines
    """

    def __init__(self, delay):
        super().__init__(delay)

    def apply(self, elapsed, surface, rect):
        super().apply(elapsed, surface, rect)
        if self.current_delay <= 0:
            self.visible = not self.visible
            self.current_delay = self.init_delay
        elif self.current_delay > 0:
            self.current_delay -= elapsed
        return (surface, rect)

class Inflate(EffectObject):

    """
    Zoom / Zoom out the surface with an interval defines
    """

    def __init__(self, delay, step_x, step_y):
        super().__init__(delay)
        self.step_x, self.step_y = step_x, step_y

    def apply(self, elapsed, surface, rect):
        super().apply(elapsed, surface, rect)
        if self.current_delay <= 0:
            self.step_x, self.step_y = -self.step_x, -self.step_y
            rect.inflate_ip(self.step_x, self.step_y)
            self.current_delay = self.init_delay
        elif self.current_delay > 0:
            self.current_delay -= elapsed
        return (surface, rect)

class FadeAlpha(EffectObject):

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

    def apply(self, elapsed, surface, rect):
        super().apply(elapsed, surface, rect)
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


class Fade(EffectObject):

    """
    Fait varier de maniere decroissante la transparence de la surface
    en fonction de la duree restante de l'effet. Lorsque l'effet est
    termine la transparence initiale de la surface est totalement
    retablise.
    Uniquement pour les surface SANS transparence.
    """

    def __init__(self, delay):
        super().__init__(delay)
        self.alpha = None

    def apply(self, elapsed, surface, rect):
        if self.first_apply:
            size = surface.get_size()
            self.layer = pg.Surface(size, pg.HWSURFACE | pg.SRCALPHA)
            self.layer = self.layer.convert()
            self.layer.fill((0, 0, 0, self.alpha))
            self.init_surface = surface.copy()
            surface.blit(self.layer, rect)
            self.first_apply = False
        if self.current_delay <= 0:
            self.done = True
        else:
            self.layer.set_alpha(self.alpha)
            surface = self.init_surface.copy()
            surface.blit(self.layer, rect)
        self.current_delay -= elapsed
        return (surface, rect)

class FadeIn(Fade):
    def apply(self, *args):
        ratio = max(0, self.current_delay) / self.init_delay
        self.alpha = int(ratio * 255)
        return super().apply(*args)

class FadeOut(Fade):
    def apply(self, *args):
        ratio = max(0, self.current_delay) / self.init_delay
        self.alpha = 255-int(ratio * 255)
        return super().apply(*args)

class Move(EffectObject):

    """
    Deplace la surface sur une distance et durant un temps definit.
    Le deplacement se base uniquement sur la duree de l'effet.
    """

    def __init__(self, delay, distance, priority=0):
        super().__init__(delay)
        self.distance = distance
        self.priority = priority
        self.stack = {'x': 0, 'y': 0}

    def step(self, elapsed, remaining_range, remaining_delay, axe):
        ratio = remaining_range / remaining_delay * elapsed

        # Pygame only handle pixel movement larger than 1
        # Problem was to avoid glitch movement effect due
        # to a remaining_range inferior than remaining_delay
        # which causes a ratio < 1 and for pygame a movement
        # of 0 pixel (then no movement would appear at all!)
        # We resolve this problem using a stack variable
        # which updates every time ratio is not an integer.
        # This stacker sum all digits after the decimal point
        # and return itself when he is larger than 1.
        # If stacker have digits after the decimal point
        # he keep them for later.
        if ratio < 1:
            self.stack[axe] += ratio
            if abs(self.stack[axe]) > 1:
                stack = self.stack[axe]
                self.stack[axe] = stack - int(self.stack[axe])
                return int(stack)
            else:
                return 0
        else:
            self.stack[axe] += ratio - int(ratio)
            return int(ratio)

    def apply(self, elapsed, surface, rect):
        super().apply(elapsed, surface, rect)
        if self.current_delay > 0:
            if self.first_apply:
                self.init_rect = rect
                self.dest_rect = rect.move(*self.distance)
                self.first_apply = False
            ratio_x = self.step(elapsed, -self.init_rect.x + self.dest_rect.x,
                                self.current_delay, 'x')
            ratio_y = self.step(elapsed, -self.init_rect.y + self.dest_rect.y,
                                self.current_delay, 'y')
            ratio = (ratio_x, ratio_y)
            rect.move_ip(*ratio)
            self.current_delay -= elapsed
        elif self.current_delay <= 0:
            rect = self.dest_rect
            self.done = True
        return (surface, rect)
