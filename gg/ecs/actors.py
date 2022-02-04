import pygame

from .. import structures
Vec2 = structures.Vec2
Point = structures.Point

from .. import style
Color = style.Color  

from .. import world
World = world.World

from . import defaults
from . import objects

from . import physics
Form = physics.Form
Rectangle = physics.Rectangle

class Actor(objects.Entity):    
    def update(self):
        super().update()
        
    def move(self, direction):
        self._accelerate(direction)
        
    def skip(self, amount: Vec2):
        self.get_body().position += amount
        self._update_position()

    def teleport(self, point: Vec2):
        self.get_body().position = point
        self._update_position() 
        
## Actors
class NPC(Actor):
    def __init__(self, game, name, position, size, color, speed, health, strength, defense, agility):
        super().__init__(game, name, Rectangle(game.space, position, size, color), speed)
        self.set_stats(health, strength, defense, agility)
        
    def update(self):
        super().update()
        
    def _hurt(self, amount):
        stats = self.get_stats()
        stats.health -= amount
        if (stats.health < 0):
            self._die()
            
    def _die(self):
        self.die()
        self.change_color(defaults.DEATH_COLOR)
        
    def receiveDamage(self, amount):
        self._hurt(amount)
        # TODO: Timer that has shows damage animation effect
       

class Enemy(NPC):
    def __init__(self, game, position, size):
        super().__init__(game, defaults.ENEMY_NAME, position, size, defaults.ENEMY_COLOR, 3, 100, 1, 1, 1)
        
    def update(self):
        super().update()
        targets = pygame.sprite.Group()
        targets.add(self.game.player)
        targets_hit = pygame.sprite.spritecollide(self, targets, False)
        
        for target in targets_hit:
            if target.name == defaults.PLAYER_NAME:
                # TODO: Player damage
                pass
            


