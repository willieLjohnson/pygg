from typing import NamedTuple
from dataclasses import dataclass, astuple

import pygame
import math

class IterableObject(type):
    def __iter__(cls):
        return iter(cls.__name__)

Point = NamedTuple("Point", [('x', float), ('y', float)])

Vec2 = pygame.Vector2

def angleof(x: float, y: float) -> float:
    return math.atan2(x, y)