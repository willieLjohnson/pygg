from turtle import position, width
import pygame
from dataclasses import dataclass

from abc import ABC, abstractmethod

from . import structures
Vec2 = structures.Vec2

from . import style
from . import ecs

@dataclass
class Grid:
    width: int
    height: int
    col: int
    rows: int
    position: tuple[int, int]
    surface: pygame.Surface
    rect: pygame.Rect = None
    _squares: list = None
    
    def update(self):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
    
    def generate_squares(self):
        square_size = self.square_size
        coords = [0, 0]
        self.rect = self.surface.get_rect()

        self._squares = list()
        self.surface.fill((15, 15, 15, 120))
        for x in range(0, self.col):
            for y in range(0, self.rows):
                if (x + y) % 2 == 0:
                    square = {}
                    surface = pygame.Surface(square_size).convert_alpha()
                    surface.fill((10, 10, 10, 120))

                    rect = surface.get_rect()
                    rect.x = x * square_size[0] * 0.9
                    rect.y = y * square_size[1] * 0.9
                    square["surface"] = surface
                    square["rect"] = rect
                    square["coords"] = (x, y)
                    self._squares.append(square)

                    self.surface.blit(surface, (rect.x, rect.y))
        
    
    @property
    def square_size(self):
        return (self.width // self.col, self.height // self.rows)

@dataclass
class Screen:
    WIDTH = 800
    HEIGHT = 600
    
    display = pygame.display.set_mode([WIDTH, HEIGHT])
    canvas = pygame.Surface((WIDTH, HEIGHT))
    
    width: int = WIDTH
    height: int = HEIGHT
    
    camera = None
    
    grid = None
    grid_surface = None

    
    def __init__(self, width = None, height = None, camera = None):
        self.width = width if width else self.WIDTH
        self.height = height if height else self.HEIGHT
        self.display = pygame.display.set_mode([width, height])
        self.canvas = pygame.Surface((width, height))
        self.camera = camera
        self.grids = []
        self.background_size = width, height
        self.create_grid_background(width, height)
        
    def create_grid_background(self, width, height):
        col = 2
        row = 2
        grid_size = width, height
        self.background_size = (width * col, height * row)
        for x in range(0, col):
            for y in range(0, row):
                grid = Grid(grid_size[0], grid_size[1], 3, 3, (0, 0), pygame.Surface((grid_size[0], grid_size[1])))
                grid.generate_squares()
                grid.position = x * self.width, y * self.height
                self.grids.append(grid)
            
            
        
        
    def draw(self, entity):
        if self.camera is not None:
            self.canvas.blit(entity.image, (entity.rect.x - self.camera.offset.x, entity.rect.y - self.camera.offset.y))
        else:
            self.canvas.blit(entity.image, (entity.rect.x, entity.rect.y))
        
    def draw_particle(self, particle):
        if self.camera is not None:
            particle_color_factor = ((particle.rad / 5) * 100)
            pygame.draw.circle(self.canvas, (particle_color_factor % 150, particle_color_factor % 110, particle_color_factor % 110, particle_color_factor % 255), (particle.x - self.camera.offset.x, particle.y - self.camera.offset.y), particle.rad)
        else:
            if particle.rad > 0:
                pygame.draw.circle(self.canvas, ecs.PLAYER_COLOR, (particle.x, particle.y), particle.rad)
            

        
    
    def draw_entities(self, entities):
        entities.draw(self.canvas)
        
    def drawGrid(self):
        for i, grid in enumerate(self.grids):
            grid.update()
            player = self.camera.player
            velocity = player.get_body().model.body.velocity
            difference = Vec2(grid.position[0] - self.camera.player.rect.x, grid.position[1] - self.camera.player.rect.y)
            distance = difference.length()

        
            self.canvas.blit(grid.surface, (grid.rect.x - self.camera.offset.x, grid.rect.y - self.camera.offset.y))
        
            
            limitX = grid.width
            limitY = grid.height

            
            newPosition = [grid.position[0], grid.position[1]]

            if velocity[0] > 0 and newPosition[0] < (self.camera.offset.x - limitX):
                newPosition[0] += self.background_size[0]
            
            if velocity[1] > 0 and newPosition[1] < (self.camera.offset.y - limitY):
                newPosition[1] += self.background_size[1]
            
            
            if velocity[0] < 0 and newPosition[0] > (self.camera.offset.x + limitX):
                newPosition[0] -= self.background_size[0]
            
            if velocity[1] < 0 and newPosition[1] > (self.camera.offset.y + limitY):
                newPosition[1] -=  self.background_size[1]

            grid.position = newPosition

    def update(self):
        if self.camera:
            self.camera.scroll()
        self.display.blit(self.canvas, (0, 0))


    
    def clear(self, color = style.GGSTYLE.STONE):
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
