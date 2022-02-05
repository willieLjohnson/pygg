import pygame

from dataclasses import dataclass
from typing import List

from . import objects




@dataclass
class System:
    name: str
    objects: List[objects.Object]
    
    def update(self) -> None:
        if objects is None: return
        
        for object in self.objects:
            object.update(self)
    
Weapons = System
Bodies = System
Decay = System
Stats = System

