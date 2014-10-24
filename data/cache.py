import os
import pygame as pg

def load_all_images(directory, colorkey=(255,0,255), accept=('.png', 'jpg', 'bmp', '.gif')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics

def load_all_fonts(directory, accept=('.ttf')):
    fonts = {}
    for font in os.listdir(directory):
        name,ext = os.path.splitext(font)
        if ext.lower() in accept:
            fonts[name] = os.path.join(directory, font)
    return fonts

class Cache():
    def __init__(self):
        self.images = load_all_images(os.path.join("resources","images"))
        self.fonts = load_all_fonts(os.path.join("resources","fonts"))

_cache = None
def init_cache():
    global _cache
    _cache = Cache()
