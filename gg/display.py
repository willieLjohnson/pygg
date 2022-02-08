import pygame
from dataclasses import dataclass

from abc import ABC, abstractmethod

from . import structures
Vec2 = structures.Vec2

from . import style

@dataclass
class Screen:
    WIDTH = 800
    HEIGHT = 600
    
    display = pygame.display.set_mode([WIDTH, HEIGHT])
    canvas = pygame.Surface((WIDTH, HEIGHT))
    
    width: int = WIDTH
    height: int = HEIGHT
    
    camera = None
    
    def __init__(self, width = None, height = None, camera = None):
        self.width = width if width else self.WIDTH
        self.height = height if height else self.HEIGHT
        self.display = pygame.display.set_mode([width, height])
        self.canvas = pygame.Surface((width, height))
        self.camera = camera
        
    def draw(self, entity):
        self.canvas.blit(entity.image, (entity.rect.x - self.camera.offset.x, entity.rect.y - self.camera.offset.y))

    
    def update(self):
        self.display.blit(self.canvas, (0, 0))
        if self.camera:
            self.camera.scroll()


    
    def clear(self, color = style.GGSTYLE.BLACK):
        self.canvas.fill(color)

class Camera:
    def __init__(self, player, width, height):
        self.player = player
        self.width = width
        self.height = height
        self.offset = Vec2(0, 0)
        self.offset_float = Vec2(0, 0)
        self.CONST = Vec2(-width / 2 + player.rect.w / 2, -height / 2 + player.rect.h / 2)

    def setmethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()

class CamScroll(ABC):
    def __init__(self, camera,player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass

class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)

class Border(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = max(self.player.left_border, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, self.player.right_border - self.camera.DISPLAY_W)

class Auto(CamScroll):
    def __init__(self,camera,player):
        CamScroll.__init__(self,camera,player)

    def scroll(self):
        self.camera.offset.x += 1
