import pygame
import pymunk

from dataclasses import dataclass

from . import ecs

Actor = ecs.Actor
playerName = ecs.PLAYER_NAME
playerColor = ecs.PLAYER_COLOR
Weapon = ecs.Weapon
Rectangle = ecs.Rectangle

from . import structures
Vec2 = structures.Vec2
Point = structures.Point


@ecs.generate_component_classmethods(Weapon)
class Player(Actor):
    focusing: bool = False
    focus_angle: float = 0

    def __init__(self, game, x, y):
        super().__init__(playerName)    
        self.game = game
        self._set_body(game.space, Vec2(x,y), Vec2(15,15), playerColor, Vec2(0,0))
        self._set_weapon(1, 75, 10000, 1, game.clock)
        self._set_accelerator(0, 40000)
        self._update_sprite_with_body()
        self.get_body().model.shape.filter = pymunk.ShapeFilter(1)

    
    def update(self):
        super().update()
        # weapon = self.get_weapon()    
        # weapon.update()
        # self._handle_enemy_collision()
        body = self.get_body()
        angle = structures.angleof(body.model.body.velocity[0], -body.model.body.velocity[1]) 
        if self.focusing:
            if body.model.shape.friction == 10000:
                body.model.shape.friction = 1 
            body.model.body.angle = self.focus_angle
        else:
            if body.model.shape.friction == 1:
                body.model.shape.friction = 10000 
            body.set_angle(angle)
            self.focus_angle = angle
        self.get_weapon().update()
            
        
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
        self.get_weapon().fire()
        
    @property     
    def can_shoot(self) -> bool:
        return self.get_weapon().can_fire
