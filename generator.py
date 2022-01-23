import random 

import random
import uuid

from . import style
from . import world

SEED = str(uuid.uuid1())
random.seed(SEED)

def set_seed(custom_seed):
    SEED = custom_seed
    random.seed(SEED)
    
def gen_float():
    return random.random()

def gen_range(min, max):
    return random.randrange(min, max)

def gen_color():
    return style.Color().randomized()

def gen_vec2(max_x = 1, max_y = 1, min_x = 0, min_y = 0):
    return world.Vec2(gen_range(min_x, max_x), gen_range(min_y, max_y))