import pygame
import uuid
from dataclasses import dataclass
import pymunk

from .. import world
from .. import style
from .. import structures

World = world.World

Vec2 = structures.Vec2
Point = structures.Point

Color = style.Color
STYLE = style.STYLE

@dataclass
class Vertices:
    __metaclass__ = structures.GetAttr
    
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
    __metaclass__ = structures.IterableObject
    
    def __init__(self, body, a, b, radius: float, elasticity: float, friction: float):
        super().__init__(body, a, b, radius)
        self.elasticity = elasticity
        self.friction = friction
    
@dataclass    
class Box:
    vertices: Vertices
    segments: list[Segment]
    thickness: float
    
    def __init__(self, space: pymunk.Space, left_top: Point = (10, 10), right_bottom: Point = (690, 230), thickness: float = 2, elasticity: float = 0.5, friction: float = 0.5):
        super().__init__()
        left, top = left_top
        right, bottom = right_bottom
        self.vertices = Vertices(left, top, right, bottom)
        self.thickness = thickness
        self.segments = list[Segment]()
        for i in range(4):
            segment = Segment(space.static_body, self.vertices.get(i), self.vertices.get((i+1)%4), thickness, elasticity, friction)
            self.segments.append(segment)
            space.add(segment)
      
@dataclass
class Model:
    body: pymunk.Body
    shape: pymunk.Shape
    color: pygame.Color
    size: Vec2
    
    def apply_impulse(self, force):
        self.body.apply_impulse_at_world_point(force, self.body.position)
      
    
@dataclass
class Rectangle(Model):
    def __init__(self, space: pymunk.Space, position: Vec2 = None, size: Vec2 = None, color: Color = STYLE.WHITE, elasticity: float = 0, friction: float = 1):
        self.body = pymunk.Body()
        self.body.position = point(position) if position else (0, 0)
        self.color = color
        
        self.shape = pymunk.Poly.create_box(self.body, point(size) if size else (50,50))
        self.shape.density = 1
        self.shape.friction = friction
        self.shape.elasticity = elasticity
        self.shape.color = color
        
        self.size = size
        
        space.add(self.body, self.shape)
        self.space = space
        
class Circle(Model):
    def __init__(self, space: pymunk.Space, position: Vec2 = None, radius: float = 1, color: Color = STYLE.WHITE, elasticity: float = 0, friction: float = 1):
        self.body = pymunk.Body()
        self.body.position = point(position) if position else (0, 0)
        self.color = color
        
        
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = 1
        self.shape.friction = friction
        self.shape.elasticity = elasticity
        self.shape.color = color
        
        self.size = Vec2(radius * 2, radius * 2)
        
        space.add(self.body, self.shape)
        self.space = space
        
def vec2(point: Point) -> Vec2:
    return Vec2(point[0], point[1]) 

def point(vec2: Vec2) -> Point:
    return Point(vec2[0], vec2[1])
