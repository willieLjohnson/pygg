import pygame
import pymunk

from . import gameobjects
from . import structures

GameObject = gameobjects.GameObject
playerName = gameobjects.PLAYER_NAME
playerColor = gameobjects.PLAYER_COLOR
ComponentType = gameobjects.ComponentType
Rectangle = gameobjects.Rectangle


Vec2 = structures.Vec2
Point = structures.Point

class Player(GameObject):
    shoot_cooldown = 0

    def __init__(self, game, x, y):
        super().__init__(game, playerName, Rectangle(game.space, Point(x,y), Point(15,15), playerColor, 2), 500)
        # self.get_component(ComponentType.BODY).form.body.velocity_func = self.limit_velocity

    
    def update(self):
        super().update()
        self._handle_enemy_collision()
        body = self.get_component(ComponentType.BODY)
        angle = structures.angleof(body.form.body.velocity[0], -body.form.body.velocity[1]) 
        body.form.body.angle = angle

        
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
