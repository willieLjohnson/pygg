import pygame
import uuid
from enum import Enum
from dataclasses import dataclass
from typing import TypedDict, NamedTuple
import pymunk


from . import world
from . import style


World = world.World
Vec2 = world.Vec2
Point = world.Point
Color = style.Color
STYLE = style.GGSTYLE


PLAYER_NAME = "Player"
ENEMY_NAME = "Enemy"
WALL_NAME = "Wall"

PLAYER_COLOR = STYLE.WHITE
ENEMY_COLOR = STYLE.RED
WALL_COLOR = STYLE.BROWN
DEATH_COLOR = STYLE.BLACK

class IterableObject(type):
    def __iter__(cls):
        return iter(cls.__name__)

class GetAttr(type):
    def __getitem__(cls, x):
        return getattr(cls, x)        

class ComponentType(Enum):
    ID = "ID"
    DEFAULT = "DEFAULT"
    STATS = "STATS"
    BODY = "BODY"
    
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
class Form:
    body: pymunk.Body
    shape: pymunk.Shape
    color: pygame.Color
    size: Vec2
    
    def apply_impulse(self, force):
        self.body.apply_force_at_local_point(force)
    

@dataclass
class Vertices:
    __metaclass__ = GetAttr
    
    left: float
    top: float
    right: float
    bottom: float
    
    def get(self, index) -> Point:
        match index:
            case 0:
                return Point(self.left, self.top)
            case 1:
                return Point(self.right, self.top)
            case 2:
                return Point(self.right, self.bottom)
            case 3:
                return Point(self.left, self.bottom)
            case _:
                return None

@dataclass(unsafe_hash=True)
class Segment(pymunk.Segment):
    __metaclass__ = IterableObject
    def __init__(self, body, a, b, radius: float, elasticity: float, friction: float):
        super().__init__(body, a, b, radius)
        self.elasticity = elasticity
        self.friction = friction
    
@dataclass    
class Box:
    vertices: Vertices
    segments: list[Segment]
    thickness: float
    
    def __init__(self, space: pymunk.Space, left_top: Point = (10, 10), right_bottom: Point = (690, 230), thickness: float = 2):
        super().__init__()
        left, top = left_top
        right, bottom = right_bottom
        self.vertices = Vertices(left, top, right, bottom)
        self.thickness = thickness
        self.segments = list[Segment]()
        for i in range(4):
            segment = Segment(space.static_body, self.vertices.get(i), self.vertices.get((i+1)%4), thickness, 1, 1)
            self.segments.append(segment)
            space.add(segment)
            
    
@dataclass
class Rectangle(Form):
    def __init__(self, space: pymunk.Space, position: Point = (10, 10), size: Point = (50, 50), color: Color = STYLE.WHITE):
        self.body = pymunk.Body()
        self.body.position = position
        self.color = color
        
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.density = 0.1
        self.shape.friction = 1
        self.shape.color = color
        
        self.size = size

        space.add(self.body, self.shape)
        self.space = space
        
@dataclass
class Body(Component):
    type = ComponentType.BODY
    
    form: Form
    position: Vec2
    size: Vec2
    color: Color
    speed: float 
    velocity: Vec2
    
    def __init__(self, form: Form, velocity: Vec2 = None):
        super().__init__()
        self.form = form
        self.position = point_to_vec2(form.body.position)
        self.size = form.size
        self.color = form.color
        self.velocity = Vec2(0, 0) if velocity is None else velocity
        
    def update(self):
        self.form.apply_impulse((self.velocity[0], -self.velocity[1]))
        self.position = point_to_vec2(self.form.body.position)
        
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
    
    
        
# Entities
class Entity(pygame.sprite.Sprite):
    name: str 
    components: ComponentDict

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.components = ComponentDict()
        self.set_component(ComponentType.ID, ID(uuid.uuid4()))  

    def _update_components(self):
        for component in self.get_components():
            component.update()
            
            
    def set_component(self, component_type: ComponentType, component: Component):
        self.components[component_type] = component
        
    def get_component(self, component_type: ComponentType) -> Component:
        if component_type in self.components:
            return self.components[component_type]
        
    def get_components(self) -> list[Component]:
        return [self.get_component(key) for key in self.components.keys()]
            
        

## Game Objects

class GameObject(Entity):
    acceleration: Vec2
    velocity: Vec2
    is_alive: bool = True
    speed: float = 3.0
    
    
    def __init__(self, game, name: str, form: Form, speed: float, velocity: Vec2 = None):
        super().__init__(name)
        self.game = game
        self.name = name
        self.speed = speed
        self.velocity = velocity if velocity is not None else Vec2(0,0)
        body = Body(form, form.color)
        self.set_component(ComponentType.BODY, body)
        self._updatesprite()
    
    def update(self):
        self._update_components()
        self._update_position()
        self._update_velocity()
        # self._move()
        # self._handle_gameobject_collision()
        # self._handle_friction()
        # self._reset_collisions()

    def _update_position(self):
        self.position = self.get_component(ComponentType.BODY).position
            
    def die(self):
        self.is_alive = False
     
    def accelerate(self, direction: Vec2):
        self.velocity.x += direction.x * self.speed
        self.velocity.y += direction.y * self.speed
    
    def _update_velocity(self):
        self.get_component(ComponentType.BODY).velocity = self.velocity
        

    def _handle_friction(self):
        body = self.get_component(ComponentType.BODY)

        if body.is_frictionless:
            self.velocity = self.velocity
        elif not self.is_accelerating:
            self.velocity *= 0.8
        else: 
            self.velocity = Vec2(0,0)
            
    def get_momentum(self):
        body = self.get_component(ComponentType.BODY)
        return body.mass * self.velocity
 
    def change_color(self, new_color):
        body = self.get_component(ComponentType.BODY)
        body.color = new_color
        self.image.fill(new_color)
            
    def _move(self):
        body = self.get_component(ComponentType.BODY)
        body.position += self.velocity

        self.rect.y = body.position.y
        self.rect.x = body.position.x

    def _updatesprite(self):
        body = self.get_component(ComponentType.BODY)
        self.image = pygame.Surface([body.size.x, body.size.y])
        self.image.fill(body.color)
        self.rect = pygame.Rect = self.image.get_rect()
        self.rect.x = body.position.x
        self.rect.y = body.position.y
       
    def _handle_gameobject_collision(self):
        gameobjects = self.game.gameobjects
        for gameobject in gameobjects:
            if gameobject == self:
                continue
            
            collide(self, gameobject)
        
    
class Wall(GameObject):
    def __init__(self, game, position, size):
        super().__init__(game, WALL_NAME, position, size, WALL_COLOR, 0)
    
## Actors

class Actor(GameObject):
    def __init__(self, game, name, position, size, color, speed, health, strength, defense, agility):
        super().__init__(game, name, position, size, color, speed)
        self.set_component(ComponentType.STATS, Stats(health, strength, defense, agility))
        
    def update(self):
        super().update()
        
    def _hurt(self, amount):
        stats = self.get_component(ComponentType.STATS)
        stats.health -= amount
        if (stats.health < 0):
            self._die()
            
    def _die(self):
        self.die()
        self.change_color(DEATH_COLOR)
        
    def receiveDamage(self, amount):
        self._hurt(amount)
        # TODO: Timer that has shows damage animation effect
       

class Enemy(Actor):
    def __init__(self, game, position, size):
        super().__init__(game, ENEMY_NAME, position, size, ENEMY_COLOR, 3, 100, 1, 1, 1)
        
    def update(self):
        super().update()
        targets = pygame.sprite.Group()
        targets.add(self.game.player)
        targets_hit = pygame.sprite.spritecollide(self, targets, False)
        
        for target in targets_hit:
            if target.name == PLAYER_NAME:
                # TODO: Player damage
                pass
            

def point_to_vec2(point: Point) -> Vec2:
    return Vec2(point.x, -point.y) 

def collide(gameobject: GameObject, other: GameObject):
    gameobject_body = gameobject.get_component(ComponentType.BODY)
    other_body = other.get_component(ComponentType.BODY)

    
    if gameobject.rect.colliderect(other):
        collision_tolerance_w = (min(gameobject_body.size.x, other_body.size.x) / max(gameobject_body.size.x, other_body.size.x))
        collision_tolerance_h = (min(gameobject_body.size.y, other_body.size.y) / max(gameobject_body.size.y, other_body.size.y))
        
        gameobject_momentum = gameobject.get_momentum()
        other_momentum = gameobject.get_momentum()
        
        # moving up
        up_difference = other_body.bottom - gameobject_body.top
        up_tolerance = collision_tolerance_h * abs(other_body.top - gameobject_body.bottom)
        if abs(up_difference + gameobject.velocity.y) < up_tolerance and gameobject.velocity.y < 0:
            gameobject_body.position.y += up_difference 
            gameobject_body.v_collision = True
                        
            other.velocity.y = gameobject_momentum.y / other_body.mass
            gameobject.velocity.y = other_momentum.y / gameobject_body.mass
            
        # moving down
        down_difference = other_body.top - gameobject_body.bottom

        down_tolerance = collision_tolerance_h * abs(other_body.bottom - gameobject_body.top)
        if abs(down_difference + gameobject.velocity.y) < down_tolerance and gameobject.velocity.y > 0:
            gameobject_body.position.y += down_difference
            gameobject_body.v_collision = True
                
            other.velocity.y = gameobject_momentum.y / other_body.mass
            gameobject.velocity.y = other_momentum.y / gameobject_body.mass

        # moving left
        left_difference = other_body.right - gameobject_body.left
        left_tolerance = collision_tolerance_w * abs(other_body.left - gameobject_body.right)
        
        if abs(left_difference + gameobject.velocity.x) < left_tolerance and gameobject.velocity.x < 0:
            gameobject_body.position.x += left_difference 
            gameobject_body.h_collision = True

            other.velocity.x = gameobject_momentum.x / other_body.mass
            gameobject.velocity.x = other_momentum.x / gameobject_body.mass

        # moving right
        right_difference = other_body.left - gameobject_body.right
        right_tolerance = collision_tolerance_w * abs(other_body.right - gameobject_body.left) 
        if abs(right_difference + gameobject.velocity.x) < right_tolerance and gameobject.velocity.x > 0:
            gameobject_body.position.x += right_difference 
            gameobject_body.h_collision = True
                    
            other.velocity.x = gameobject_momentum.x / other_body.mass
            gameobject.velocity.x = other_momentum.x / gameobject_body.mass 