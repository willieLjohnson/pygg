from dataclasses import dataclass

import pygame
import uuid
import math

from . import components
Body = components.Body
ComponentType = components.ComponentType
Component = components.Component
ComponentDict = components.ComponentDict
ID = components.ID
Stats = components.Stats
Decaying = components.Decaying

from . import physics
Form = physics.Form
Rectangle = physics.Rectangle

from .. import structures
Vec2 = structures.Vec2
Point = structures.Point

from .. import style
Color = style.Color

from .. import world
World = world.World


class Object(pygame.sprite.Sprite):
    name: str 
    components: ComponentDict
    _image: None

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.components = ComponentDict()
        self._set_component(ComponentType.ID, ID(uuid.uuid4()))  
        
    def __iter__(cls):
        return iter(cls.__name__)

    def update(self):
        super().update()
        self._update_components()
        
    def _update_components(self):
        for component in self._get_components():
            component.update()  

    def _set_component(self, component_type: ComponentType, component: Component):
        self.components[component_type] = component
        
    def _get_component(self, component_type: ComponentType) -> Component:
        if component_type in self.components:
            return self.components[component_type]
    def _get_components(self) -> list[Component]:
        return [self._get_component(key) for key in self.components.keys()]
       

class Entity(Object):
    acceleration: Vec2
    velocity: Vec2
    speed: float = 3.0
    is_alive: bool = False
     
    def __init__(self, game, name: str, form: Form, speed: float, velocity: Vec2 = None):
        super().__init__(name)
        self.game = game
        self.name = name
        self.speed = speed
        self.velocity = velocity if velocity is not None else Vec2(0,0)
        body = Body(form, form.color)
        self.set_body(body)
        self._update_sprite()
        self.is_alive = True
        
    def _update_sprite(self):
        body = self.get_body()
        self._image = pygame.Surface([body.size.x, body.size.y])
        self.image = self._image
        self.image.fill(body.color)
        self.rect = pygame.Rect = self.image.get_rect()
        self.rect.center = body.position

    def update(self):
        super().update()
        self._update_position()
        self._update_velocity()
        

    def _update_position(self):
        body = self.get_body()
        self._rot_center(-body.form.body.angle)
        self.rect.center = body.position
        
    
    def _update_velocity(self):
        body = self.get_body()
        body.velocity = self.velocity
        self.velocity = Vec2(0, 0)
        
    
    def _accelerate(self, direction: Vec2):
        self.velocity.x += direction.x * self.speed
        self.velocity.y += direction.y * self.speed
        
    
    def _handle_friction(self):
        body = self.get_body()

        if body.is_frictionless:
            self.velocity = self.velocity
        elif not self.is_accelerating:
            self.velocity *= 0.8
        else: 
            self.velocity = Vec2(0,0)
    
     
    def _rot_center(self, angle):
        rot_image = pygame.transform.rotozoom(self._image, math.degrees(angle), 1)
        rot_rect = rot_image.get_rect(center=self.rect.center)
        self.image = rot_image
        self.rect = rot_rect
           
    def _handle_entity_collision(self):
        entities = self.game.entities
        for entity in entities:
            if entity == self:
                continue
            
            collide(self, entity)
            

    def die(self):
        self.is_alive = False
     
    
    def set_body(self, body):
        self._set_component(ComponentType.BODY, body)
    
    def get_body(self) -> Body:
        return self._get_component(ComponentType.BODY)

    def set_stats(self, health: float, strength: float, defense: float, agility: float) -> None:
        self._set_component(ComponentType.STATS, Stats(health, strength, defense, agility))

    def get_stats(self) -> Stats:
        return self._get_component(ComponentType.STATS)
        
    def set_decaying(self, start, clock, is_decaying = False, current = None):
        self._set_component(ComponentType.DECAYING, Decaying(self, start, clock, is_decaying, current))
    
    def get_decaying(self) -> Decaying:
        return self._get_component(ComponentType.DECAYING)
    
    def get_momentum(self):
        body = self.get_body()
        return body.mass * self.velocity
 
    def change_color(self, new_color):
        body = self.get_body()
        body.color = new_color
        self.image.fill(new_color)
        self._image.fill(new_color)
           
def collide(entity: Entity, other: Entity):
    entity_body = entity.get_body()
    other_body = other.get_body()

    if entity.rect.colliderect(other):
        collision_tolerance_w = (min(entity_body.size.x, other_body.size.x) / max(entity_body.size.x, other_body.size.x))
        collision_tolerance_h = (min(entity_body.size.y, other_body.size.y) / max(entity_body.size.y, other_body.size.y))
        
        entity_momentum = entity.get_momentum()
        other_momentum = entity.get_momentum()
        
        # moving up
        up_difference = other_body.bottom - entity_body.top
        up_tolerance = collision_tolerance_h * abs(other_body.top - entity_body.bottom)
        if abs(up_difference + entity.velocity.y) < up_tolerance and entity.velocity.y < 0:
            entity_body.position.y += up_difference 
            entity_body.v_collision = True
                        
            other.velocity.y = entity_momentum.y / other_body.mass
            entity.velocity.y = other_momentum.y / entity_body.mass
            
        # moving down
        down_difference = other_body.top - entity_body.bottom

        down_tolerance = collision_tolerance_h * abs(other_body.bottom - entity_body.top)
        if abs(down_difference + entity.velocity.y) < down_tolerance and entity.velocity.y > 0:
            entity_body.position.y += down_difference
            entity_body.v_collision = True
                
            other.velocity.y = entity_momentum.y / other_body.mass
            entity.velocity.y = other_momentum.y / entity_body.mass

        # moving left
        left_difference = other_body.right - entity_body.left
        left_tolerance = collision_tolerance_w * abs(other_body.left - entity_body.right)
        
        if abs(left_difference + entity.velocity.x) < left_tolerance and entity.velocity.x < 0:
            entity_body.position.x += left_difference 
            entity_body.h_collision = True

            other.velocity.x = entity_momentum.x / other_body.mass
            entity.velocity.x = other_momentum.x / entity_body.mass

        # moving right
        right_difference = other_body.left - entity_body.right
        right_tolerance = collision_tolerance_w * abs(other_body.right - entity_body.left) 
        if abs(right_difference + entity.velocity.x) < right_tolerance and entity.velocity.x > 0:
            entity_body.position.x += right_difference 
            entity_body.h_collision = True
                    
            other.velocity.x = entity_momentum.x / other_body.mass
            entity.velocity.x = other_momentum.x / entity_body.mass 