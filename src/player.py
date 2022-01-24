import pygame

from . import gameobjects
from . import world

Entity = gameobjects.Entity
playerName = gameobjects.PLAYER_NAME
playerColor = gameobjects.PLAYER_COLOR
ComponentType = gameobjects.ComponentType
Body = gameobjects.Body


Vec2 = world.Vec2

class Player(Entity):
    def __init__(self, game, x, y):
        super().__init__(playerName)
        self.game = game
        self.set_component(ComponentType.BODY, Body(Vec2(x, y), Vec2(15,15), playerColor, 3, Vec2(0,0)))
        self._updatesprite()
    
    def update(self):
        super().update()
        self._handle_enemy_collision()
        
    def _handle_enemy_collision(self):
        enemies_hit = pygame.sprite.spritecollide(self, self.game.enemies, False)

        for enemy in enemies_hit:
            print(enemy)
            enemy.receiveDamage(10)
    