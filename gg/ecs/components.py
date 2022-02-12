import uuid
import pymunk
import pygame

from dataclasses import dataclass

from ..style import Color
from ..structures import Vec2

from . import physics
Form = physics.Form
point_to_vec2 = physics.point_to_vec2



class Component:
    entity_id: uuid.UUID
    def update(self, delta) -> None: pass
    
    @property
    def class_name(self):
        return self.__class__.__name__
    
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
        if direction:
            self.direction = direction
    
    def update(self, delta):
        self.decelerate(delta)

    def decelerate(self, delta):
        self.acceleration = 0
        self.direction = None
        
    def accelerate(self, direction: Vec2):
        self.direction = direction
        if self.acceleration > self.max_acceleration: return 
        self.acceleration = 0.1 * self.max_acceleration
        
@dataclass
class Body(Component):
    form: Form
    position: Vec2
    rotation: float
    size: Vec2
    color: Color
    velocity: Vec2 = None
    
    
    def __init__(self, entity_id, form, position, rotation, size, color, velocity = None): 
        self.entity_id = entity_id
        self.form = form
        self.position = position
        self.rotation = rotation
        self.size = size
        self.color = color
        self.velocity = velocity if velocity else Vec2(0,0)

    @property
    def bottom(self) -> float:
        return self.position.y + self.size.y

    @property
    def top(self) -> float:
        return self.position.y
    
    @property
    def left(self) -> float:
        return self.position.x

    @property
    def right(self) -> float:
        return self.position.x + self.size.x
    
    def limit_velocity(body, gravity, damping, dt):
        max_velocity = 1000
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        l = body.velocity.length
        if l > max_velocity:
            scale = max_velocity / l
            body.velocity = body.velocity * scale

@dataclass
class Decaying(Component):    
    entity = None
    start: float
    clock: pygame.time.Clock
    is_decaying: bool = False
    current: float = None
    
    def __init__(self, entity, start, clock, is_decaying=False, current=None): 
        self.entity = entity
        self.start = start
        self.clock = clock
        self.is_decaying = is_decaying
        self.current = current if current else self.start

    def update(self, delta):
        if self.current is None:
            self.current = self.start
            
        self.current -= self.clock.get_time()
        if self.current <= 0:
            self.entity.die()
            
        color = self.entity.get_body().color
        decaying_alpha = (color[0] * (self.current / self.start)) % 255
        self.entity.change_color((decaying_alpha, color[1], color[2], color[3]))


@dataclass
class Weapon(Component):
    damage: float
    fire_rate: float
    bullet_speed: float
    damping: float
    clock: pygame.time.Clock

    can_fire: bool = False
    cooldown: float = 0
    
    def __init__(self, entity_id, damage, fire_rate, bullet_speed, damping, clock):
        self.entity_id = entity_id
        self.damage = damage
        self.fire_rate = fire_rate
        self.bullet_speed = bullet_speed
        self.damping = damping
        self.clock = clock


    def update(self):
        self.cooldown -= self.clock.get_time()
        if self.cooldown <= 0:
            self.can_fire = True
            
        
    def fire(self):
        if self.can_fire:
            self.cooldown = self.fire_rate
            self.can_fire = False
