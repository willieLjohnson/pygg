# pygg

A modular pygame wrapper that adds ECS, procedural generation, cameras, and physics

## Features

- Super simple.
- Modularity using ECS and OOP.
- Core modules:
    - **Game** - the main class that handles the game loop.
    - **Generator** - procedural generation.
    - **Style** - color palette system that allows you to easily change color of the whole game during runtime.
    - **World** - game world configuration.
    - **Screen** - cameras, canvas, screen, and window size.
    - **Gameobjects** - ecs.

## how to use:

 Clone the repo into your project:

```bash

cd your_project/src && git clone https://github.com/willieLjohnson/pygg.git

```

### Hello World example 

> importing the whole module

```python

import pygg as GG

GG.Game("Hello World").run()

```

> importing submodules

```python

from pygg import game

game.Game("Hello World").run()


```

### Using pygg in your project

> Sample game

```
bouncy:
    src:
        __init__.py
        pygg/
        bouncygame.py
    rungame.py
```

```python

# rungame.py

import src.bouncygame as Bouncy
Bouncy.Game().run()

```

```python

# src/__init__.py

from . import bouncygame

```


```python

# src/bouncygame.py

import pygame
from random import random
from . import pygg as GG

 
class Game(GG.Game):

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

```

