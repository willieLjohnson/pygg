import pymunk

from ..style import GGSTYLE
from ..gen import gen_range
from ..structures import Vec2

from . import entities
_Body = entities.Body
_Accelerator = entities.Accelerator
_Decaying = entities.Decaying

from . import physics
Rectangle = physics.Rectangle

from . import defaults

@entities.generate_component_classmethods(_Body)
class Wall(entities.Entity):
    def __init__(self, game, position, size):
        super().__init__(defaults.WALL_NAME)
        self._set_body(game.space, position, size, defaults.WALL_COLOR, Vec2(0,0))
        self._update_sprite_with_body()
    

def zero_damping(body, gravity, damping, dt):
    pymunk.Body.update_velocity(body, gravity, 1, dt)

@entities.generate_component_classmethods(_Body, _Accelerator, _Decaying)
class Bullet(entities.Entity):
    def __init__(self, game, position, size, initial_velocity, force):
        super().__init__("Bullet")
        self._set_body(game.space, position, size, defaults.PLAYER_COLOR, initial_velocity)
        self._set_decaying(1100, game.clock, True)
        # self._set_accelerator(speed, speed, direction)
        body = self.get_body()
        body.model.apply_impulse(physics.point(force))
        body.model.body.velocity_func = zero_damping
        body.model.body.angular_velocity = 10 * gen_range(-2, 2)
        body.model.shape.filter = pymunk.ShapeFilter(1)
        self._update_sprite_with_body()
    