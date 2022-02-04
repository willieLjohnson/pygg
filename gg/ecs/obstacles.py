import pymunk

from ..style import GGSTYLE
from ..gen import gen_range

from . import objects


from .physics import Rectangle

from . import defaults
  
class Wall(objects.Entity):
    def __init__(self, game, position, size):
        super().__init__(game, defaults.WALL_NAME, Rectangle(game.space, position, size, defaults.WALL_COLOR), 0)
    
    
def zero_damping(body, gravity, damping, dt):
    pymunk.Body.update_velocity(body, gravity, 1, dt)

class Bullet(objects.Entity):
    def __init__(self, game, position, size, direction, speed):
        super().__init__(game, "Bullet", Rectangle(game.space, position, size, GGSTYLE.RED, 1, 0), speed)
        self._accelerate(direction)
        self.set_decaying(1100, game.clock, True)
        body = self.get_body()
        body.form.body.velocity_func = zero_damping
        body.form.body.angular_velocity = 50 * gen_range(-2, 2)
    