import pygame
import math
import uuid

from dataclasses import dataclass
from typing import List, Type


from . import entities
from . import physics
from .. import structures

_Entity = entities.Entity
_Component = entities.Component
_Body = entities.Body
_Accelerator = entities.Accelerator

@dataclass
class System:
    component_classes: List[Type[_Component]]
    _entity_to_components: dict[uuid.UUID, List[_Component]]

    
    def __init__(self, component_classes, entites = None):
        self.component_classes = component_classes
        self._entity_to_components = {}
        self._entities = list()

        if entites is not None:
            for entity in entites:
                self.add(entity)
    
    def add(self, entity: _Entity) -> None:
        components_to_add = dict()
        for component_class in self.component_classes:
            component = entity.get_component(component_class)
    
            if component is None: 
                return 
            
            components_to_add[component_class.__name__] = component
            
        self._entities.append(entity)
        self._entity_to_components[entity.id] = components_to_add
        
    def remove(self, entity: _Entity) -> None:
        if entity in self._entities:
            self._entities.remove(entity)

                
    def update(self, delta) -> None:
        pass
            
 
                
@dataclass
class PhysicsSystem(System):
    def __init__(self, entities=None):
        super().__init__([_Body, _Accelerator], entities)
        
    def update(self, delta) -> None:
        for entity in self._entities:
            self._update_entitiy(entity, delta)

            
    def _update_position(self, entity, delta) -> None:
        components = self._entity_to_components[entity.id]
        body = components.get(_Body)
        if body is None: return



    
    def _update_entitiy(self, entity, delta) -> None:
        components = self._entity_to_components.get(entity.id)


        body = components.get(_Body.__name__)
        accelerator = components.get(_Accelerator.__name__)
        # print(f"\n\nupdate velocity: {entity.name}")
        # print(f"\n\ncomponents: {components}")
        # print(f"body is none: {body is None}")
        # print(f"accelerator is None: {accelerator is None}\n\n")
        if body is None or accelerator is None: return
        
        acceleration = accelerator.acceleration
        direction = accelerator.direction
        
        if direction is not None and acceleration > 0: 
            body.form.apply_impulse((direction.x * acceleration, direction.y * acceleration))
            direction = None
        body.position = physics.point_to_vec2(body.form.body.position)
            
        entity._rot_center(-body.form.body.angle)
        entity.rect.center = body.position

        accelerator.update(delta)
        entity.update()

    
    def _handle_friction(self, entity):
        body = entity.get_body()

        if body.is_frictionless:
            entity.velocity = entity.velocity
        elif not entity.is_accelerating:
            entity.velocity *= 0.8
        else: 
            entity.velocity = structures.Vec2(0,0)
    
     
    def _rot_center(self, entity, angle):
        rot_image = pygame.transform.rotozoom(entity._image, math.degrees(angle), 1)
        rot_rect = rot_image.get_rect(center=entity.rect.center)
        entity.image = rot_image
        entity.rect = rot_rect
           
    def _handle_entity_collision(self, entity):
        for other in self._entities:
            if other.id == entity.id:
                continue
            
            entities.collide(entity, other)