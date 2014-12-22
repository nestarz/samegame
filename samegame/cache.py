import os
import pygame as pg


class ImageError(Exception):
    pass


class FontError(Exception):
    pass


class Cache:

    def __init__(self):
        self.__graphics = {}
        self.__fonts = {}

    def load_images(
        self, directory, colorkey=(
            255, 0, 255), accept=(
                '.png', 'jpg', 'bmp', '.gif')):
        for pic in os.listdir(directory):
            name, ext = os.path.splitext(pic)
            if ext.lower() in accept:
                img = pg.image.load(os.path.join(directory, pic))
                if img.get_alpha():
                    img = img.convert_alpha()
                else:
                    img = img.convert()
                    img.set_colorkey(colorkey)
                self.__graphics[name] = img

    def load_fonts(self, directory, accept=('.ttf')):
        for font in os.listdir(directory):
            name, ext = os.path.splitext(font)
            if ext.lower() in accept:
                self.__fonts[name] = os.path.join(directory, font)

    def load(self):
        self.load_images(os.path.join("resources", "images"))
        self.load_fonts(os.path.join("resources", "fonts"))

    def get_image(self, name):
        try:
            return self.__graphics[name]
        except KeyError:
            raise ImageError("Image not found: {}".format(name))

    def get_font(self, name):
        try:
            return self.__fonts[name]
        except KeyError:
            raise FontError("Font not found: {}".format(name))

# Cache creation
cache = Cache()
