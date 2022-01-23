from dataclasses import dataclass
import pygame


@dataclass
class Game:
    name = ""
    gameobjects = pygame.sprite.Group()
    
    def __init__(self, name):
        self.name = name
        pygame.init()
        pygame.display.set_caption(name)