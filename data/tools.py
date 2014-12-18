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
