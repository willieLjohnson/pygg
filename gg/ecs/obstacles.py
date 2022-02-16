import pymunk

from ..style import GGSTYLE
from ..gen import gen_range
from ..structures import Vec2

from . import entities
_Body = entities.Body
_Accelerator = entities.Accelerator

from .physics import Rectangle

from . import defaults

@entities.generate_component_classmethods(_Body)
class Wall(entities.Entity):
    def __init__(self, game, position, size):
        super().__init__(defaults.WALL_NAME)
        self._set_body(game.space, position, size, defaults.WALL_COLOR, Vec2(0,0))
        self._update_sprite_with_body()
    

def zero_damping(body, gravity, damping, dt):
    pymunk.Body.update_velocity(body, gravity, 1, dt)

@entities.generate_component_classmethods(_Body, _Accelerator)
class Bullet(entities.Entity):
    def __init__(self, game, position, size, direction, speed):
        super().__init__(game, "Bullet", Rectangle(game.space, position, size, GGSTYLE.RED, 1, 0), speed)
        self._accelerate(direction)
        self._set_decaying(1100, game.clock, True)
        body = self.get_body()
        body.model.body.velocity_func = zero_damping
        body.model.body.angular_velocity = 50 * gen_range(-2, 2)
    