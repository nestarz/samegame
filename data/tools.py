import pygame as pg
from . import constants as c
from .cache import cache

class Font(pg.font.Font):

    def __init__(self, name, size):

        # Gets the font from the cache
        font = cache.get_font(name)
        # If font hasn't been found, get pygame default font
        #font = pg.font.get_default_font()

        # Create pygame font object with our loaded font
        super().__init__(font, size)

def render_text(
    text,
    size=10,
    color=c.WHITE_RGB,
    name=c.FONT1,
    AA=0,
    bold=False,
    italic=False,
    **kwargs
):
    font = Font(name, size)
    font.set_bold(bold)
    font.set_italic(italic)
    return font.render(text, AA, color, kwargs.get('bg_color', None))

class EffectDict(dict):
    """ Dictionary which contains effect """
    def resumeall(self):
        """ Resume all effects in the dict """
        for l in self.values():
            l.resumeall()

    def stopall(self):
        """ Stop all effects in the dict """
        for l in self.values():
            l.stopall()

    def ongoing(self):
        """ Is one effect or more is ongoing ? """
        for l in self.values():
            if l.ongoing():
                return True
        return False

    def backup(self, img, rect):
        """ Return initial surface and rect stored in effects """
        for l in self.values():
            for e in l:
                if not e.first_apply:
                    return e.backup()
        return (img, rect)

    def is_empty(self):
        """ Check if there is effect in the dict """
        for l in self.values():
            if l:
                return False
        return True

class EffectList(list):
    """ List which contains effect """
    def resumeall(self):
        for e in self:
            e.resume()

    def stopall(self):
        for e in self:
            e.stop()

    def ongoing(self):
        for e in self:
            if not e.pause:
                return True
        return False

    def backup(self, img, rect):
        for e in self:
            if not e.first_apply:
                return e.backup()
        return (img, rect)
