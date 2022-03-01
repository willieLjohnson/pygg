from dataclasses import dataclass
from typing import NamedTuple

from . import gen

import pygame

pygame.init()



@dataclass
class Color:
    r: int = 255
    g: int = 255
    b: int = 255
    a: int = 255
    
    @property
    def rgb(self):
        return (self.r, self.g, self.b, self.a)
    
    def is_same_rgb(color, other):
        return color[0] == other[0] and color[1] == other[1] and color[2] == other[2]
    
    def randomized(self, alpha = None):
        self.r = gen.gen_float() * 255
        self.g = gen.gen_float() * 255
        self.b = gen.gen_float() * 255
        self.a = gen.gen_float() * 255 if alpha is None else alpha
        
        return (self.r, self.g, self.b, self.a)
    
@dataclass
class STYLE():
    _FONT: pygame.font.Font
    BLACK = (0, 0, 0, 255)
    WHITE = (225, 255, 255, 255)
    BLUE = (50, 50, 255, 255)
    BROWN = (139, 69, 19, 255)
    RED = (255, 0, 0, 255)
    YELLOW = (0, 255, 255, 255)
    FONT_SIZE: int = 36
    
    def __init__(self):
        self._FONT = self._generate_font()
    
    def _generate_font(self):
        return pygame.font.Font(pygame.font.get_default_font(), self.FONT_SIZE)
    
    @property
    def FONT(self): 
        return self._FONT
  
# PYGG Palette https://coolors.co/464d77-36827f-f9db6d-f4eded-ff5d73  
class GGSTYLE(STYLE):
    RED = (255, 93, 115, 255)
    WHITE = (244, 237, 237, 255)
    YELLOW = (249, 219, 109, 255)
    GREEN = (54, 130, 127, 255)
    NEON_BLUE = (54, 250, 200, 255)
    NAVY = (70, 77, 119, 255)
    STONE = (55, 70, 70, 255)
    FONT_SIZE: int = 1000
