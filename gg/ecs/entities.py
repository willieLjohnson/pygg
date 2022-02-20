
from this import d
import pygame
import uuid
import math

from typing import TypeVar, Type


from . import components


Component = components.Component

Body = components.Body
Accelerator = components.Accelerator
Stats = components.Stats
Weapon = components.Weapon
Decaying = components.Decaying




from . import physics
Model = physics.Model
Rectangle = physics.Rectangle

from .. import structures
Vec2 = structures.Vec2
Point = structures.Point

from .. import style
Color = style.Color

from .. import world
World = world.World



class Entity(pygame.sprite.Sprite):
    id: uuid.UUID
    name: str 

    _components: dict[str, Type[Component]]
    _image: pygame.Surface
    

    def __init__(self, name: str, *components):
        super().__init__()
        self.name = name
        self.id = uuid.uuid4()
        self._components = {}
        self._create_image((0,0), (0,0,0))
        
        for component in components:
            if not issubclass(Component, type(component)): 
                continue
            self.add_component(component)

    def _create_image(self, size: tuple[int, int], color: tuple[0, 0, 0]) -> None:
        self.image = pygame.Surface(size).convert_alpha()
        self.image.fill(color)
        self.rect = pygame.Rect = self.image.get_rect()
        self._image = self.image
        
    def _update_image(self, size: tuple[int, int], color: tuple[0, 0, 0]):
        self._image = pygame.Surface(size).convert_alpha()
        self._image.fill(color)

            
    def rot_center(self, angle):
        rot_image = pygame.transform.rotozoom(self._image, math.degrees(angle), 1)
        rot_rect = rot_image.get_rect(center=self.rect.center)
        self.image = rot_image
        self.rect = rot_rect
        
        
    def _update_components(self):
        for component in self._get_components():
            component.update()  

          
    def add_component(self, component: Component) -> None:
        component.entity_id = self.id
        self._components[component.class_name] = component
        
    def get_component(self, component_class: Type[Component]) -> Component:
        # print(f"\n\n{self}")
        # print(f"\n\nget componeont: {component_class} with {component_class.__name__}")
        # print(f"result: {self._components.get(component_class.__name__)}\n\n")
        return self._components.get(component_class.__name__)
     
    def has_component(self, component_class: str) -> bool:
        return component_class.__name__ in self._components
              
    def get_components(self) -> dict[str, Type[Component]]:
        return self._components
    

    @property
    def center(self) -> Vec2:
        return Vec2(self.rect.center[0], self.rect.center[1])
    
    @property
    def components_set(self) -> set[Component]:
        return [self.get_component(key) for key in self._components.keys()]

    def __iter__(cls):
        return iter(cls.__name__)
    

def generate_component_classmethods(*component_classes: Component):
    def generate(entity_class: Entity):
        decorated_class = entity_class
        for i, component_class in enumerate(component_classes):
            match component_class.__name__:
                case Body.__name__:
                    decorated_class = body(decorated_class)
                case Stats.__name__:
                    decorated_class = stats(decorated_class)
                case Decaying.__name__:
                    decorated_class = decaying(decorated_class)
                case Weapon.__name__:
                    decorated_class = weapon(decorated_class)
                case Accelerator.__name__:
                    decorated_class = accelerator(decorated_class)
                case _:
                    continue
        
        return decorated_class
                
    def body(entity_class):
        def _set_body(self: Entity, space, position, size, color, velocity = None, elasticity = 0, friction = 1):
            model = Rectangle(space, position, size, color, elasticity, friction)
            if velocity: 
                model.body.velocity = physics.point(velocity)
            self.add_component(Body(model))
            
        def _update_sprite_with_body(self):
            body = self.get_body()
            self._create_image((body.size.x, body.size.y), body.color)
            self.rect.center = body.position

        def _set_position(self, position):
            body = self.get_body()
            body.model.body.position = position.x, position.y
            self.rect.center = position
            
        def _handle_entity_collision(self):
            entities = self.game.entities
            for entity in entities:
                if entity == self:
                    continue
                
                collide(self, entity)
        
        def get_body(self: Entity):
            return self.get_component(Body)
        
        def get_momentum(self: Entity):
            body = self._get_body()
            return body.mass * self.velocity

        def change_color(self, new_color):
            body = self.get_body()
            body.model.color = new_color
            self._update_image(body.size, new_color)
        
            
        setattr(entity_class, "_set_body", _set_body)
        setattr(entity_class, "_update_sprite_with_body", _update_sprite_with_body)
        setattr(entity_class, "_set_position", _set_position)
        setattr(entity_class, "_handle_entity_collision", _handle_entity_collision)
        setattr(entity_class, "get_body", get_body)
        setattr(entity_class, "get_momentum", get_momentum)
        setattr(entity_class, "change_color", change_color)

        return entity_class
    
    def stats(entity_class):
        def _set_stats(self: Entity, health, strength, defense, agility):
            self.add_component(Stats(health, strength, defense, agility))
            
        def get_stats(self: Entity):
            return self.get_component(Stats)
        
        def _hurt(self, amount):
            stats = self.get_stats()
            stats.health -= amount
            if not stats.is_alive: self._die()
                
        def _die(self):
            pass
        
        setattr(entity_class, "_set_stats", _set_stats)
        setattr(entity_class, "get_stats", get_stats)
        setattr(entity_class, "_hurt", _hurt)
        setattr(entity_class, "_die", _die)

        return entity_class
            
    
    def decaying(entity_class):
        def _set_decaying(self: Entity, start, clock, is_decaying=False, current=None):
            self.add_component(Decaying(self, start, clock, is_decaying, current))
            
        def get_decaying(self: Entity):
            return self.get_component(Decaying)

        setattr(entity_class, "_set_decaying", _set_decaying)
        setattr(entity_class, "get_decaying", get_decaying)
        
        return entity_class
        
    def weapon(entity_class):
        def _set_weapon(self: Entity, damage, fire_rate, bullet_speed, damping, clock):
            self.add_component(Weapon(damage, fire_rate, bullet_speed, damping, clock))
        
        def get_weapon(self: Entity):
            return self.get_component(Weapon)
        
        setattr(entity_class, "_set_weapon", _set_weapon)
        setattr(entity_class, "get_weapon", get_weapon)

        return entity_class
    
    def accelerator(entity_class):
        def _set_accelerator(self: Entity, acceleration, max_acceleration, direction = None):
            self.add_component(Accelerator(acceleration, max_acceleration, direction))
        
        def get_accelerator(self: Entity):
            return self.get_component(Accelerator)
                    
        def _accelerate(self, direction: Vec2):
            accelerator = self.get_accelerator()
            accelerator.accelerate(direction)
        
        setattr(entity_class, "_set_accelerator", _set_accelerator)
        setattr(entity_class, "get_accelerator", get_accelerator)
        setattr(entity_class, "_accelerate", _accelerate)

        return entity_class   
    
    return generate
    
# class Entity(Entity):
#     def __init__(self, game, name: str, model: Model, speed: float, velocity: Vec2 = None):
#         super().__init__(name)
#         self.game = game
#      ``   self.name = name
#         self.speed = speed
#         self.velocity = velocity if velocity is not None else Vec2(0,0)
#         body = Body(model, model.color)
#         self._set_body(body)
#         self._update_sprite_with_body()
        

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
  
  

        
