import pymunk

from ..style import GGSTYLE
from ..gen import gen_range

from . import entities


from .physics import Rectangle

from . import constants
ComponentType = constants.COMPONENT_TYPE
from . import defaults

@entities.created_with([ComponentType.BODY])
class Wall(entities.Entity):
    def __init__(self, game, position, size):
        super().__init__(defaults.WALL_NAME)
        form = Rectangle(game.space, position, size, defaults.WALL_COLOR)
        self._create_body(form)
        self._update_sprite()

    
def zero_damping(body, gravity, damping, dt):
    pymunk.Body.update_velocity(body, gravity, 1, dt)

@entities.created_with([ComponentType.BODY, ComponentType.ACCELERATOR])
class Bullet(entities.Entity):
    def __init__(self, game, position, size, direction, speed):
        super().__init__(game, "Bullet", Rectangle(game.space, position, size, GGSTYLE.RED, 1, 0), speed)
        self._accelerate(direction)
        self._set_decaying(1100, game.clock, True)
        body = self.get_body()
        body.form.body.velocity_func = zero_damping
        body.form.body.angular_velocity = 50 * gen_range(-2, 2)
    