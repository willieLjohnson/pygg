import pygame

from src.pygg.src.game import Game

from . import gameobjects
from . import world

GameObject = gameobjects.GameObject
playerName = gameobjects.PLAYER_NAME
playerColor = gameobjects.PLAYER_COLOR
ComponentType = gameobjects.ComponentType
Body = gameobjects.Body


Vec2 = world.Vec2

class Player(GameObject):
    def __init__(self, game, x, y):
        super().__init__(game, playerName, Vec2(x, y), Vec2(15, 15), playerColor, 3)
    
    def update(self):
        super().update()
        self._handle_enemy_collision()
        
    def _handle_enemy_collision(self):
        enemies_hit = pygame.sprite.spritecollide(self, self.game.enemies, False)

        for enemy in enemies_hit:
            enemy.receiveDamage(10)
    