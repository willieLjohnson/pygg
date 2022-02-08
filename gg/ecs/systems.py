import pygame
import math

from dataclasses import dataclass
from typing import List 


from . import entities
from . import components
from . import constants
from .. import structures

Entity = entities.Entity
Component = components.Component
ComponentType = components.Type
IDtoTypeComponentListDict = components.IDtoTypeComponentListDict
TypeComponentListDict = components.TypeComponentListDict

Type = constants.SYSTEM_TYPE

@dataclass
class System:
    component_types: List[ComponentType]
    _entities: List[Entity]
    _id_to_type_components_dict: IDtoTypeComponentListDict

    
    def __init__(self, component_types, entites = None):
        self.component_types = component_types
        self._id_to_type_components_dict = IDtoTypeComponentListDict()
        self._entities = list()

        if entites is not None:
            for entity in entites:
                self.add(entity)
    
    def add(self, entity: Entity) -> None:
        for component_type in self.component_types:
            component = entity.get_component(component_type)
    
            if component is None: 
                return

            self._entities.append(entity)
            type_component_list_dict = TypeComponentListDict() 
            type_component_list_dict[component_type] = component
            self._id_to_type_components_dict[entity.id] = type_component_list_dict
        
    def remove(self, entity: Entity) -> None:
        if entity in self._entities:
            self._entities.remove(entity)

                
    def update(self, delta) -> None:
        pass
            
 
                
@dataclass
class PhysicsSystem(System):
    def __init__(self, entities=None):
        super().__init__([ComponentType.BODY, ComponentType.ACCELERATOR], entities)
        
    def update(self, delta) -> None:
        for entity in self._entities:
            self._update_position(entity, delta)
            self._update_velocity(entity, delta)
            
    def _update_position(self, entity, delta) -> None:
        components = self._id_to_type_components_dict[entity.id]
        body = components.get(ComponentType.BODY)
        if body is None: return
        
        entity._rot_center(-body.form.body.angle)
        entity.rect.center = body.position
        body.update(delta)

    
    def _update_velocity(self, entity, delta) -> None:
        components = self._id_to_type_components_dict.get(entity.id)


        body = components.get(ComponentType.BODY)
        accelerator = components.get(ComponentType.ACCELERATOR)
        
        if body is None or accelerator is None: return
        
        body.velocity = accelerator.acceleration
        
        accelerator.update(delta)
        body.update(delta)
    
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