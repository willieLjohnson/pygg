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
        rectangle = Rectangle(game.space, Vec2(x,y), Vec2(15,15), game.style.RED)
        self._set_body(rectangle, Vec2(x,y), 0, Vec2(15,15), playerColor, Vec2(0,0))
        self._set_weapon(1, 50, 2000, 1, game.clock)
        self._set_accelerator(0, 20000)
        print(f"\n\nPlayer\nComponents: {self.get_components()}")
        print(f"Body: {self.get_body()}\n\n")
        self._update_sprite()

    
    def update(self):
        super().update()
        # weapon = self.get_weapon()    
        # weapon.update()
        # self._handle_enemy_collision()
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
        self.get_weapon().fire()
        
    @property     
    def can_shoot(self) -> bool:
        return self.get_weapon().can_fire
