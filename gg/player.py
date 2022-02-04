import pygame
import pymunk

from dataclasses import dataclass

from . import ecs

Actor = ecs.Actor
playerName = ecs.PLAYER_NAME
playerColor = ecs.PLAYER_COLOR
ComponentType = ecs.ComponentType
Rectangle = ecs.Rectangle

from . import structures
Vec2 = structures.Vec2
Point = structures.Point

@dataclass
class Weapon:
    damage: float
    fire_rate: float
    bullet_speed: float
    damping: float
    _clock: pygame.time.Clock
    _can_fire: bool = False
    _cooldown: float = 0


    def update(self):
        self._cooldown -= self._clock.get_time()
        if self._cooldown <= 0:
            self._can_fire = True
        
    def fire(self):
        if self._can_fire:
            self._cooldown = self.fire_rate
            self._can_fire = False

    
class Player(Actor):
    weapon: Weapon
    focusing: bool = False
    focus_angle: float = 0

    def __init__(self, game, x, y):
        super().__init__(game, playerName, Rectangle(game.space, Point(x,y), Point(15,15), playerColor,0, 20), 2500)
        self.weapon = Weapon(1, 75, 20000, 1, game.clock, True, 0)
        
    
    def update(self):
        super().update()    
        self.weapon.update()
        self._handle_enemy_collision()
        body = self.get_body()
        angle = structures.angleof(body.form.body.velocity[0], -body.form.body.velocity[1]) 
        if self.focusing:
            if body.form.shape.friction == 10000:
                body.form.shape.friction = 1 
            body.form.body.angle = self.focus_angle
        else:
            if body.form.shape.friction == 1:
                body.form.shape.friction = 10000 
            body.form.body.angle = angle
            self.focus_angle = angle

            

        
    def _handle_enemy_collision(self):
        enemies_hit = pygame.sprite.spritecollide(self, self.game.enemies, False)

        for enemy in enemies_hit:
            enemy.receiveDamage(10)
    
    def limit_velocity(body, gravity, damping, dt):
        max_velocity = 30
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        l = body.velocity.length
        if l > max_velocity:
            scale = max_velocity / l
            body.velocity = body.velocity * scale
       
    def shoot(self):
        self.weapon.fire()
        
    @property     
    def can_shoot(self) -> bool:
        return self.weapon._can_fire
