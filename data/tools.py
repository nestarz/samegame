import pygame as pg

class Font(pg.font.Font):

    def __init__(self, name, size):
        self.name = name
        self.size = size
        super().__init__(
            cache._cache.fonts.get(
                name,
                pg.font.get_default_font()),
            size)

def render_text(
    text,
    name,
    size,
    color,
    AA=0,
    bold=False,
    italic=False,
):
    font = Font(name, size)
    font.set_bold(bold)
    font.set_italic(italic)
    return font.render(text, AA, color)
