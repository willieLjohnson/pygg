import pygame
from typing import NamedTuple
from dataclasses import dataclass

Vec2 = NamedTuple("Point", [('x', float), ('y', float)])

Point = NamedTuple("Point", [('x', float), ('y', float)])

        
@dataclass 
class World:
    FRICTION = 0.5
    TOLERANCE = 0.8
    

    