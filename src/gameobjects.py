from abc import abstractclassmethod
import pygame
import uuid
from enum import Enum
from dataclasses import dataclass

from . import world
from . import style


World = world.World
Vec2 = world.Vec2
Color = style.Color
STYLE = style.GGSTYLE


PLAYER_NAME = "Player"
ENEMY_NAME = "Enemy"
WALL_NAME = "Wall"

PLAYER_COLOR = STYLE.WHITE
ENEMY_COLOR = STYLE.RED
WALL_COLOR = STYLE.BROWN
DEATH_COLOR = STYLE.BLACK

class Direction:
    UP: float = -1.0
    DOWN: float = 1.0
    LEFT: float = -1.0
    RIGHT: float = 1.0

class ComponentType(Enum):
    ID = "ID"
    DEFAULT = "DEFAULT"
    STATS = "STATS"
    BODY = "BODY"
    
@dataclass
class Component:
    type = ComponentType.DEFAULT
    
@dataclass
class ID(Component):
    type = ComponentType.ID
    uuid: uuid.UUID
    
@dataclass
class Stats(Component):
    type = ComponentType.STATS
    
    health: int
    strength: int
    defense: int
    agility: int
    
    def change_health(self, amount):
        self.health += amount
    
    def change_strength(self, amount):
        self.strength += amount
    
    def change_defense(self, amount):
        self.defense += amount
    
    def change_agility(self, amount):
        self.agility += amount
    
@dataclass
class Body(Component):
    type = ComponentType.BODY
    
    position: Vec2
    size: Vec2
    color: Color
    speed: float
    velocity: Vec2
    mass: float
    density: float = 1.0
    h_collision: bool = False
    v_collision: bool = False
    
    is_alive: bool = True
    is_frictionless: bool = False
    
    def __init__(self, position = None, size = None, color = None, speed = None, velocity = None):
        super().__init__()
        self.position = position if position else Vec2(0, 0)
        self.size = size if size else Vec2(0, 0)
        self.color = color if color else STYLE.STONE
        self.velocity = velocity if velocity else Vec2(0, 0)
        self.speed = speed if speed else 3
        self.calculate_mass()
        
    def update(self):
        self.position += self.velocity 
        
    def reset_collisions(self):
        self.h_collision = False
        self.v_collision = False
        
    def calculate_mass(self):
        self.mass = (self.size.x * self.size.y) * self.density * World.FRICTION
        
    def get_momentum(self):
        return self.mass * self.velocity
    
    def die(self):
        self.is_alive = False
        
        
# Entities
class Entity(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.components = {ComponentType.ID: uuid.uuid1()}
        
    def set_component(self, component_type, component):
        self.components[component_type] = component
        
    def get_component(self, component_type):
        if component_type in self.components:
            return self.components[component_type]
    
    def is_alive(self):
        return self.get_component(ComponentType.BODY).is_alive
    
    def update(self):
        self.get_component(ComponentType.BODY).update()
        self._move()
        self._handle_gameobject_collision()
        self._reset_collisions()
        self._reset_velocity()
     
    def accelerate(self, x, y):
        body = self.get_component(ComponentType.BODY)
        body.velocity.x += x * body.speed
        body.velocity.y += y * body.speed
 
    def change_color(self, new_color):
        body = self.get_component(ComponentType.BODY)
        body.color = new_color
        self.image.fill(new_color)
    
    def _reset_velocity(self):
        body = self.get_component(ComponentType.BODY)        
        body.velocity = body.velocity if body.is_frictionless else Vec2(0,0)
        
    def _move(self):
        body = self.get_component(ComponentType.BODY)
        self.rect.y = body.position.y
        self.rect.x = body.position.x

    def _updatesprite(self):
        body = self.get_component(ComponentType.BODY)
        self.image = pygame.Surface([body.size.x, body.size.y])
        self.image.fill(body.color)
        self.rect = pygame.Rect = self.image.get_rect()
        self.rect.x = body.position.x
        self.rect.y = body.position.y
       
    def _handle_gameobject_collision(self):
        gameobjects = self.game.gameobjects
        for gameobject in gameobjects:
            if gameobject == self:
                continue
            
            collide(self, gameobject)

    def _reset_collisions(self):
        self.get_component(ComponentType.BODY).reset_collisions()
        

## Game Objects

class GameObject(Entity):
    def __init__(self, game, name, position, size, color, speed, velocity=None):
        super().__init__(name)
        self.game = game
        self.name = name
        self.set_component(ComponentType.BODY, Body(position, size, color, speed, velocity))
        self._updatesprite()
    
class Wall(GameObject):
    def __init__(self, game, position, size):
        super().__init__(game, WALL_NAME, position, size, WALL_COLOR, 0)
    
## Actors

class Actor(GameObject):
    def __init__(self, game, name, position, size, color, speed, health, strength, defense, agility):
        super().__init__(game, name, position, size, color, speed)
        self.set_component(ComponentType.STATS, Stats(health, strength, defense, agility))
        
    def update(self):
        super().update()
        
    def _hurt(self, amount):
        stats = self.get_component(ComponentType.STATS)
        stats.health -= amount
        if (stats.health < 0):
            self._die()
            
    def _die(self):
        self.change_color(DEATH_COLOR)
        self.get_component(ComponentType.BODY).die()
        
    def receiveDamage(self, amount):
        self._hurt(amount)
        # TODO: Timer that has shows damage animation effect
       

class Enemy(Actor):
    def __init__(self, game, position, size):
        super().__init__(game, ENEMY_NAME, position, size, ENEMY_COLOR, 3, 100, 1, 1, 1)
        
    def update(self):
        super().update()
        targets = pygame.sprite.Group()
        targets.add(self.game.player)
        targets_hit = pygame.sprite.spritecollide(self, targets, False)
        
        for target in targets_hit:
            if target.name == PLAYER_NAME:
                # TODO: Player damage
                pass

def collide(gameobject, other):
    if gameobject.rect.colliderect(other.rect):
        gameobject_body = gameobject.get_component(ComponentType.BODY)
        other_body = other.get_component(ComponentType.BODY)
        
        collision_tolerance_h = min(gameobject_body.size.y, other_body.size.y) * World.TOLERANCE
        collision_tolerance_w = min(gameobject_body.size.x, other_body.size.x) * World.TOLERANCE

        gameobject_momentum = gameobject_body.get_momentum()
        other_momentum = other_body.get_momentum()
        
        # moving up
        up_difference = other.rect.bottom - gameobject.rect.top
        if abs(up_difference) < collision_tolerance_h and gameobject_body.velocity.y < 0:
            gameobject_body.position.y += up_difference
            gameobject_body.v_collision = True
                        
            other_body.velocity.y = gameobject_momentum.y / other_body.mass
            gameobject_body.velocity.y = other_momentum.y / gameobject_body.mass

        
            
        # moving down
        down_difference = other.rect.top - gameobject.rect.bottom
        if abs(down_difference) < collision_tolerance_h and gameobject_body.velocity.y > 0:
            gameobject_body.position.y += down_difference
            gameobject_body.v_collision = True
                
            other_body.velocity.y = gameobject_momentum.y / other_body.mass
            gameobject_body.velocity.y = other_momentum.y / gameobject_body.mass

        # moving left
        left_difference = other.rect.right - gameobject.rect.left
        if abs(left_difference) < collision_tolerance_w and gameobject_body.velocity.x < 0:
            gameobject_body.position.x += left_difference
            gameobject_body.h_collision = True

            other_body.velocity.x = gameobject_momentum.x / other_body.mass
            gameobject_body.velocity.x = other_momentum.x / gameobject_body.mass

        # moving right
        right_difference = other.rect.left - gameobject.rect.right
        if abs(right_difference) < collision_tolerance_w and gameobject_body.velocity.x > 0:
            gameobject_body.position.y += right_difference
            gameobject_body.h_collision = True
                    
            other_body.velocity.x = gameobject_momentum.x / other_body.mass
            gameobject_body.velocity.x = other_momentum.x / gameobject_body.mass
