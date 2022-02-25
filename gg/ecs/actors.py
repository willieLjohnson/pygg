from re import A
import pygame


from .. import structures
Vec2 = structures.Vec2
Point = structures.Point

from .. import style
Color = style.Color  

from .. import world
World = world.World

from . import defaults
from . import entities

_Body = entities.Body
_Accelerator = entities.Accelerator
_Weapon = entities.Weapon
_Stats = entities.Stats

from . import physics
_Model = physics.Model
_Rectangle = physics.Rectangle

@entities.generate_component_classmethods(_Body, _Accelerator, _Stats)
class Actor(entities.Entity):
    def move(self, direction):
        self._accelerate(direction)
        
    def skip(self, amount: Vec2):
        self._set_position(self.get__Body().position + amount)

    def teleport(self, point: Vec2):
        self._set_position(point)
        
## Actor
class NPC(Actor):
    def __init__(self, game, name, position, size, color, speed, health, strength, defense, agility):
        super().__init__(name)
        self.game = game
        self._set_stats(health, strength, defense, agility)
        self._set_body(game.space, position, size, color, Vec2(0,0))
        self._set_accelerator(0, speed)
        self._update_sprite_with_body()
        
    def update(self):
        super().update()

    def _die(self):
        self.change_color(defaults.DEATH_COLOR)
        
    def receiveDamage(self, amount):
        self._hurt(amount)
        # TODO: Timer that has shows damage animation effect

@entities.generate_component_classmethods(_Weapon)
class Enemy(NPC):
    def __init__(self, game, position, size):
        self._max_acceleration = 100000
        self.max_acceleration = self._max_acceleration
        super().__init__(game, defaults.ENEMY_NAME, position, size, defaults.ENEMY_COLOR, self._max_acceleration, 100, 1, 1, 1)
        self._set_weapon(1, 75, 30000, 1, game.clock)
        self.targets = pygame.sprite.Group()
        self.targets.add(game.player)
        
        
    def update(self):
        super().update()
        entities = self.game.entities.values()

        # targets_hit = pygame.sprite.spritecollide(self, self.targets, False)
        for target in self.targets:
            if target == self: continue
            if target.name == defaults.PLAYER_NAME:
                pbody = target.get_body()
                ebody = self.get_body()
                difference = (pbody.position - ebody.position)
                normal = difference / difference.length()
                print(difference, normal)
                self.move(normal)
        
        for entity in entities:
            if entity == self: continue
            pbody = entity.get_body()
            ebody = self.get_body()
            difference = (pbody.position - ebody.position)
            normal = difference / difference.length()

            if entity.name == defaults.ENEMY_NAME:
                if difference.length() < 200:
                    if difference.length() >= 75:
                        self.max_acceleration += self._max_acceleration * 0.02
                    else:
                        self.max_acceleration += self._max_acceleration * 0.001
                    self.move(normal * 0.5)
                    self.get_accelerator().max_acceleration = self.max_acceleration
                else:
                    self.max_acceleration = self._max_acceleration
            else:
                if difference.length() < 75:
                    self.move(-normal * 2)


            
