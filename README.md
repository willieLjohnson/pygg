# pygg


## how to use:

1. clone the repo into your project

2. import it:

'''
from . import pygg as GG
'''

3. use GG to access all the needed files:

> Sample game

'''python
import pygame
from random import random
from . import pygg as GG

 
class BouncyGame(GG.Game):

    def __init__(self):
        super().__init__('bouncy')
        self.speed_multiplier = 1

        for _ in range(50):
            self._create_bouncy()
    
        
    def run(self):
        self.clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self.clock.tick(60)
            for bouncy in self.gameobjects:
                bouncy_body =  bouncy.get_component(GG.ComponentType.BODY)
                bouncy_body.velocity *= self.speed_multiplier
                if bouncy.rect.right > GG.SCREEN_WIDTH or bouncy.rect.left < 0:
                    bouncy_body.velocity.x *= -1
                if bouncy.rect.bottom > GG.SCREEN_HEIGHT or bouncy.rect.top < 0:
                    bouncy_body.velocity.y *= -1
                    
            self.gameobjects.update()
   
            self._handle_input()
            GG.screen.fill(GG.STYLE.BLACK)
            self.gameobjects.draw(GG.screen)
            pygame.display.update()

        pygame.quit()
    
    def _create_bouncy(self):
        random_color = GG.gen_color()
        random_position = GG.gen_vec2(GG.SCREEN_WIDTH, GG.SCREEN_HEIGHT)
        random_size = GG.gen_range(15, 20)
        random_speed = GG.gen_range(3, 15)
        random_velocity = GG.gen_vec2(random_speed, random_speed)
        
        bouncy = GG.GameObject(self, "bouncy", random_position, GG.Vec2(random_size, random_size), random_color, random_speed, random_velocity)
        bouncy.get_component(GG.ComponentType.BODY).is_frictionless = True
        self.gameobjects.add(bouncy)
        
             
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        keys = pygame.key.get_pressed()  #checking pressed keys

        if keys[pygame.K_a]:
            self.speed_multiplier -= 0.001
        if keys[pygame.K_d]:
            self.speed_multiplier += 0.001
'''


super simple wrapper for pygame that i'm use to prototype games

