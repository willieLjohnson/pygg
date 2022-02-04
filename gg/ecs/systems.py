import pygame

from dataclasses import dataclass

from . import objects

@dataclass
class System:
    name: str
    objects = pygame.sprite.Group()
    
    def update(self) -> None:
        for object in self.objects:
            object.update(self)
    
Weapons = System
Entities = System