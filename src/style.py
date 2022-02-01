from dataclasses import dataclass
from re import A

from . import generator as RNG

import pygame

pygame.init()


@dataclass
class Color:
    r: int = 255
    g: int = 255
    b: int = 255
    a: int = 255
    
    def rgb(self):
        return (self.r, self.g, self.b, self.a)
    
    def randomized(self):
        self.r = RNG.gen_float() * 255
        self.g = RNG.gen_float() * 255
        self.b = RNG.gen_float() * 255
        self.a = RNG.gen_float() * 255
        
        return (self.r, self.g, self.b, self.a)
    
@dataclass
class STYLE():
    _FONT: pygame.font.Font
    BLACK: Color = (0, 0, 0, 255)
    WHITE: Color = (225, 255, 255, 255)
    BLUE: Color = (50, 50, 255, 255)
    BROWN: Color = (139, 69, 19, 255)
    RED: Color = (255, 0, 0, 255)
    YELLOW: Color = (0, 255, 255, 255)
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
    RED: Color = (255, 93, 115, 255)
    WHITE: Color = (244, 237, 237, 255)
    YELLOW: Color = (249, 219, 109, 255)
    GREEN: Color = (54, 130, 127, 255)
    NAVY: Color = (70, 77, 119, 255)
    STONE: Color = (55, 70, 70, 255, 255)
    FONT_SIZE: int = 1000
