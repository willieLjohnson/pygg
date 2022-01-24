import pygame
from typing import NamedTuple
from dataclasses import dataclass


Vec2 = pygame.Vector2
        
@dataclass 
class World:
    FRICTION = 0.5
    TOLERANCE = 0.8
    
    