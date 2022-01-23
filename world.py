import pygame
from dataclasses import dataclass

Vec2 = pygame.Vector2

@dataclass 
class World:
    FRICTION = 0.5