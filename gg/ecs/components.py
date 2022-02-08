import uuid
import pymunk
import pygame

from dataclasses import dataclass
from typing import TypedDict, List

from ..style import Color
from ..structures import Vec2

from . import constants

from . import physics
Form = physics.Form
point_to_vec2 = physics.point_to_vec2


Type = constants.COMPONENT_TYPE

@dataclass
class Component:
    type = Type.DEFAULT
    entity_id: uuid.UUID
  
    def update(self, delta) -> None: pass
    

class TypeComponentDict(TypedDict):
    type: Type
    component: Component

ComponentList = List[Component]
class TypeComponentListDict(TypedDict):
    type: Type
    components: ComponentList
    
class IdComponentListDict(TypedDict):
    id: uuid.UUID
    components: ComponentList
    
class IDtoTypeComponentListDict(TypedDict):
    id: uuid.UUID
    type_to_components: TypeComponentListDict

    


@dataclass
class Stats(Component):
    type = Type.STATS
    
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
    acceleration: Vec2
    max_acceleration: float 
    
    def update(self, delta):
        self.decelerate(delta)

    def decelerate(self, delta):
        self.acceleration *= 0.1 * delta
        
    def accelerate(self, direction: Vec2, delta):
        if self.acceleration.length() > self.max_acceleration: return 
        self.acceleration.x += direction.x * self.max_acceleration * delta
        self.acceleration.y += direction.y * self.max_acceleration * delta
        
@dataclass
class Body(Component):
    type = Type.BODY
    
    form: Form
    position: Vec2
    rotation: float
    size: Vec2
    color: Color
    velocity: Vec2
    
    def __init__(self, entity_id, form: Form, velocity: Vec2 = None):
        super().__init__(entity_id)
        self.form = form
        self.position = point_to_vec2(form.body.position)
        self.rotation = form.body.angle
        self.size = form.size
        self.color = form.color
        self.velocity = Vec2(0, 0) if velocity is None else velocity

        
    def update(self, delta):
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
    type = Type.DECAYING
    
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
    _clock: pygame.time.Clock
    _can_fire: bool = False
    _cooldown: float = 0


    def update(self):
        self._cooldown -= self._clock.get_time()
        if self._cooldown <= 0:
            self._can_fire = True
        
    def fire(self):
        if self._can_fire:
            self._cooldown = self.fire_rate
            self._can_fire = False
