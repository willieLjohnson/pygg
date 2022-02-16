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
                continue 
            
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
            self._update_components(entity, delta)

    def _sync_to_body(self, entity, body):
        entity.rot_center(body.angle)
        entity.rect.center = body.position
    
    def _update_components(self, entity, delta) -> None:
        components = self._entity_to_components.get(entity.id)
        body = components.get(_Body.__name__)
        accelerator = components.get(_Accelerator.__name__)
        

        if accelerator is not None:
            acceleration = accelerator.acceleration
            direction = accelerator.direction
            if direction is not None and acceleration > 0: 
                body.model.apply_impulse((direction.x * acceleration, direction.y * acceleration))
        
            accelerator.update(delta)
        
        if body is not None:
            self._sync_to_body(entity, body)


    
    def _handle_friction(self, entity):
        body = entity.get_body()

        if body.is_frictionless:
            entity.velocity = entity.velocity
        elif not entity.is_accelerating:
            entity.velocity *= 0.8
        else: 
            entity.velocity = structures.Vec2(0,0)
   
    def _handle_entity_collision(self, entity):
        for other in self._entities:
            if other.id == entity.id:
                continue
            
            entities.collide(entity, other)