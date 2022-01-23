from dataclasses import dataclass

from . import generator as RNG

@dataclass
class Color:
    r: int = 255
    g: int = 255
    b: int = 255
    
    def rgb(self):
        return (self.r, self.g, self.b)
    
    def randomized(self):
        self.r = RNG.gen_float() * 255
        self.g = RNG.gen_float() * 255
        self.b = RNG.gen_float() * 255
        
        return (self.r, self.g, self.b)
    
@dataclass
class STYLE():
    BLACK: Color = (0, 0, 0)
    WHITE: Color = (225, 255, 255)
    BLUE: Color = (50, 50, 255)
    BROWN: Color = (139, 69, 19)
    STONE: Color = (55, 70, 70)
    RED: Color = (255, 50, 50)
    RED_FADED: Color = (125, 50, 50)
