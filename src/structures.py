from typing import NamedTuple
from dataclasses import dataclass, astuple

import pygame

class IterableObject(type):
    def __iter__(cls):
        return iter(cls.__name__)

Point = NamedTuple("Point", [('x', float), ('y', float)])

Vec2 = pygame.Vector2