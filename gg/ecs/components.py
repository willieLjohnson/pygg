import uuid
import pygame

from dataclasses import dataclass

from ..style import Color
from ..structures import Vec2

from . import physics
Model = physics.Model
vec2 = physics.vec2


@dataclass
class Component:
    entity_id = None
    def update(self, delta) -> None: pass
    
    @property
    def class_name(self):
        return self.__class__.__name__
    
    def update(self):
        pass
    
@dataclass    
class Stats(Component):    
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
    
    @property
    def is_alive(self):
        return self.health >= 0

@dataclass
class Accelerator(Component):
    acceleration: float
    max_acceleration: float 
    direction: Vec2 = None
    
    def __init__(self, acceleration = 0, max_acceleration = 0, direction = None):
        self.acceleration = acceleration
        self.max_acceleration = max_acceleration
        self.direction = direction if direction else Vec2(0,0)
    
    def update(self, delta):
        self.decelerate(delta)

    def decelerate(self, delta):
        self.acceleration = 0
        self.direction = Vec2(0,0)
        
    def accelerate(self, direction: Vec2):
        self.direction += direction
        if self.acceleration > self.max_acceleration: return 
        self.acceleration = 0.1 * self.max_acceleration

    @property
    def velocity(self) -> Vec2:
        return Vec2(self.acceleration * self.direction.x, self.acceleration * self.direction.y)
@dataclass
class Body(Component):
    model: Model

    def get_position(self) -> Vec2:
        return vec2(self.model.body.position)
    
    def get_size(self) -> Vec2:
        return vec2(self.model.size)
    
    def get_angle(self) -> Vec2:
        return -self.model.body.angle
    
    def set_angle(self, value) -> Vec2:
        self.model.body.angle = value
    
    def get_color(self) -> Color:
        return self.model.color
    
    def get_velocity(self) -> Vec2:
        return self.model.body.velocity
    
    @property
    def velocity(self) -> Vec2:
        return self.get_velocity()
    
    @property
    def color(self) -> Color:
        return self.get_color()
    
    @property
    def angle(self) -> Vec2:
        return self.get_angle()
    
    @property
    def position(self) -> Vec2:
        return self.get_position()
    
    @property
    def size(self) -> Vec2:
        return self.get_size()

    @property
    def bottom(self) -> float:
        return self.position.y + self.model.size.y

    @property
    def top(self) -> float:
        return self.position.y
    
    @property
    def left(self) -> float:
        return self.position.x

    @property
    def right(self) -> float:
        return self.position.x + self.model.size.x

@dataclass
class Decaying(Component):    
    entity = None
    start: float
    clock: pygame.time.Clock
    is_dead: bool = False
    is_decaying: bool = False
    current: float = None
    
    def __init__(self, entity, start, clock, is_decaying=False, current=None): 
        self.entity = entity
        self.start = start
        self.clock = clock
        self.is_decaying = is_decaying
        self.current = current if current else self.start

    def update(self):
        if self.is_dead: return
        
        if self.current is None:
            self.current = self.start
            
        self.current -= self.clock.get_time()
        if self.current <= 0:
            self.is_dead = True
            
        color = self.entity.get_body().color
        a = (color[3] * (self.current / self.start)) % 255
        self.entity.change_color((color[0], color[1],color[2], a))


@dataclass
class Weapon(Component):
    damage: float
    fire_rate: float
    bullet_speed: float
    damping: float
    clock: pygame.time.Clock

    can_fire: bool = False
    cooldown: float = 0
    
    def update(self):
        self.cooldown -= self.clock.get_time()
        if self.cooldown <= 0:
            self.can_fire = True
            
        
    def fire(self):
        if self.can_fire:
            self.cooldown = self.fire_rate
            self.can_fire = False
