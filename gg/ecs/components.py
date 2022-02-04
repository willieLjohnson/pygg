import uuid
import pymunk
import pygame

from enum import Enum
from dataclasses import dataclass
from typing import TypedDict

from ...gg.style import Color
from ...gg.structures import Vec2

from . import physics
Form = physics.Form
point_to_vec2 = physics.point_to_vec2

class ComponentType(Enum):
    ID = "ID"
    DEFAULT = "DEFAULT"
    STATS = "STATS"
    BODY = "BODY"
    DECAYING = "DECAYING"


@dataclass
class Component:
    type = ComponentType.DEFAULT
    
    def update(self):
        pass
    
class ComponentDict(TypedDict):
    type: ComponentType
    component: Component
    
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
    
    form: Form
    position: Vec2
    rotation: float
    size: Vec2
    color: Color
    speed: float 
    velocity: Vec2
    
    def __init__(self, form: Form, velocity: Vec2 = None):
        super().__init__()
        self.form = form
        self.position = point_to_vec2(form.body.position)
        self.rotation = form.body.angle
        self.size = form.size
        self.color = form.color
        self.velocity = Vec2(0, 0) if velocity is None else velocity

        
    def update(self):
        self.form.apply_impulse((self.velocity[0], self.velocity[1]))
        self.position = point_to_vec2(self.form.body.position)
        self.velocity = Vec2(0, 0)
        
    @property
    def bottom(self) -> float:
        return self.position.y + self.size.sy

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
    type = ComponentType.DECAYING
    
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

    def update(self):
        if self.current is None:
            self.current = self.start
            
        self.current -= self.clock.get_time()
        if self.current <= 0:
            self.entity.die()
            
        color = self.entity.get_body().color
        decaying_alpha = (color[0] * (self.current / self.start)) % 255
        self.entity.change_color((decaying_alpha, color[1], color[2], color[3]))
        