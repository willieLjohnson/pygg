
import pygame
import uuid
import math

from dataclasses import dataclass

from . import constants


from . import components
Body = components.Body
Component = components.Component
ComponentList = components.ComponentList
ComponentType = constants.COMPONENT_TYPE
TypeComponentDict = components.TypeComponentDict

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

class Entity(pygame.sprite.Sprite):
    name: str 
    id: uuid.UUID
    _components_dict: TypeComponentDict
    _image = None

    def __init__(self, name: str, components: ComponentList = None):
        super().__init__()
        self.name = name
        self.id = uuid.uuid4()
        self._components_dict = TypeComponentDict()
        if components is not None:
            for component in components:
                self.set_component(component.type, component)

    def _update_components(self):
        for component in self._get_components():
            component.update()  
    
                     
    def _rot_center(self, angle):
        rot_image = pygame.transform.rotozoom(self._image, math.degrees(angle), 1)
        rot_rect = rot_image.get_rect(center=self.rect.center)
        self.image = rot_image
        self.rect = rot_rect

    def set_component(self, component_type: ComponentType, component: Component):
        component.entity_id = self.id
        self._components_dict[component_type] = component
        
    def get_component(self, component_type: ComponentType) -> Component:
        if component_type in self._components_dict:
            return self._components_dict[component_type]
        else:
            return None
     
    def has_component(self, component_type: ComponentType) -> bool:
        return component_type in self._components_dict
              
    @property
    def components(self) -> list[Component]:
        return [self.get_component(key) for key in self._components_dict.keys()]

    def __iter__(cls):
        return iter(cls.__name__)
    
def created_with(components):
    def setup(entity):
        created_entity = entity
        for i, component in enumerate(components):
            print(i, component)
            match component:
                case ComponentType.BODY:
                    created_entity = body(created_entity)
                case ComponentType.STATS:
                    created_entity = stats(created_entity)
                case ComponentType.DECAYING:
                    created_entity = decaying(created_entity)
                case ComponentType.WEAPON:
                    created_entity = weapon(created_entity)
                case ComponentType.ACCELERATOR:
                    created_entity = accelerator(created_entity)
                case _:
                    print("default")
                    continue
        
        return created_entity
                
    def body(entity_with_body):
        def _set_body(self: Entity, body):
            self.set_component(ComponentType.BODY, body)
            
        def _create_body(self: Entity, form, velocity=None):
            body = Body(self.id, form, velocity)
            self.set_component(ComponentType.BODY, body)
            
        def _update_sprite(self):
            body = self.get_body()
            self._image = pygame.Surface([body.size.x, body.size.y])
            self.image = self._image
            self.image.fill(body.color)
            self.rect = pygame.Rect = self.image.get_rect()
            self.rect.center = body.position
        
        def _set_position(self, position):
            body = self.get_body()
            body.form.body.position = position.x, position.y
            body.position = position
            self.rect.center = position
            
        def _handle_entity_collision(self):
            entities = self.game.entities
            for entity in entities:
                if entity == self:
                    continue
                
                collide(self, entity)
        
        def get_body(self: Entity):
            return self.get_component(ComponentType.BODY)
        
        def get_momentum(self: Entity):
            body = self._get_body()
            return body.mass * self.velocity

        def change_color(self, new_color):
            body = self.get_body()
            body.color = new_color
            self.image.fill(new_color)
            self._image.fill(new_color)
        
            
        setattr(entity_with_body, "_set_body", _set_body)
        setattr(entity_with_body, "_create_body", _create_body)
        setattr(entity_with_body, "_update_sprite", _update_sprite)
        setattr(entity_with_body, "_set_position", _set_position)
        setattr(entity_with_body, "_handle_entity_collision", _handle_entity_collision)
        setattr(entity_with_body, "get_body", get_body)
        setattr(entity_with_body, "get_momentum", get_momentum)
        setattr(entity_with_body, "change_color", change_color)

        return entity_with_body
    
    def stats(entity_with_stats):
        def _set_stats(self: Entity, health, strength, defense, agility):
            self.set_component(ComponentType.STATS, Stats(health, strength, defense, agility))
            
        def get_stats(self: Entity):
            return self.get_component(ComponentType.STATS)
        
        def _hurt(self, amount):
            stats = self.get_stats()
            stats.health -= amount
            if not stats.is_alive: self._die()
                
        def _die(self):
            pass
        
        setattr(entity_with_stats, "_set_body", _set_stats)
        setattr(entity_with_stats, "get_stats", get_stats)
        setattr(entity_with_stats, "_hurt", _hurt)
        setattr(entity_with_stats, "_die", _die)

        return entity_with_stats
            
    
    def decaying(entity_with_decaying):
        def _set_decaying(self: Entity, entity, start, clock, is_decaying=False, current=None):
            self.set_component(ComponentType.DECAYING, Decaying(entity, start, clock, is_decaying, current))
            
        def get_decaying(self: Entity):
            return self.get_component(ComponentType.DECAYING)

        setattr(entity_with_decaying, "_set_decaying", _set_decaying)
        setattr(entity_with_decaying, "get_decaying", get_decaying)
        
        return entity_with_decaying
        
    def weapon(entity_with_weapon):
        def _set_weapon(self: Entity, weapon):
            self.set_component(ComponentType.WEAPON, weapon)
        
        def get_weapon(self: Entity):
            return self.get_component(ComponentType.WEAPON)
        
        setattr(entity_with_weapon, "_set_weapon", _set_weapon)
        setattr(entity_with_weapon, "get_weapon", get_weapon)

        return entity_with_weapon
    
    def accelerator(entity_with_accelerator):
        def _set_accelerator(self: Entity, accelerator):
            self.set_component(ComponentType.ACCELERATOR, accelerator)
        
        def get_accelerator(self: Entity):
            return self.get_component(ComponentType.ACCELERATOR)
                    
        def accelerate(self, direction: Vec2, delta):
            accelerator = self.get_accelerator()
            accelerator.accelerate(direction, delta)
        
        setattr(entity_with_accelerator, "_set_accelerator", _set_accelerator)
        setattr(entity_with_accelerator, "get_accelerator", get_accelerator)
        setattr(entity_with_accelerator, "get_accelerator", accelerate)

        return entity_with_accelerator   
    
    return setup
    
# class Entity(Entity):
#     def __init__(self, game, name: str, form: Form, speed: float, velocity: Vec2 = None):
#         super().__init__(name)
#         self.game = game
#      ``   self.name = name
#         self.speed = speed
#         self.velocity = velocity if velocity is not None else Vec2(0,0)
#         body = Body(form, form.color)
#         self._set_body(body)
#         self._update_sprite()
        

#     def update(self):
#         super().update()
#         self._update_position()
#         self._update_velocity()
        


    
#     def _handle_friction(self):
#         body = self.get_body()

#         if body.is_frictionless:
#             self.velocity = self.velocity
#         elif not self.is_accelerating:
#             self.velocity *= 0.8
#         else: 
#             self.velocity = Vec2(0,0)
    

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
  
  

        
