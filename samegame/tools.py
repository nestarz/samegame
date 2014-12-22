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
    size=None,
    color=None,
    name=None,
    AA=None,
    bold=None,
    italic=None,
    **kwargs
):
    style = kwargs.get('style', {})
    if not size:
        size = style.get('size', 10)
    if not color:
        color = style.get('color1', c.WHITE_RGB)
    if not name:
        name = style.get('name', c.FONT1)
    if not AA:
        AA = style.get('AA', 1)
    if not bold:
        bold = style.get('bold', False)
    if not italic:
        italic = style.get('italic', False)
    bg_color = kwargs.get('bg_color', style.get('bg_color', None))
    font = Font(name, size)
    font.set_bold(bold)
    font.set_italic(italic)
    image = font.render(text, AA, color, bg_color)
    image = image.convert_alpha()
    return image
