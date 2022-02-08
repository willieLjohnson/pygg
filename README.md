# pygg

A modular pygame wrapper that adds ECS, procedural generation, cameras, and physics.

## Features

- Super simple.
- Modularity using ECS and OOP.
- Core modules:
    - **Game** - the main class that handles the game loop.
    - **Gen** - procedural generation.
    - **Style** - color palette system that allows you to easily change color of the whole game during runtime.
    - **World** - game world configuration.
    - **Screen** - cameras, canvas, screen, and window size.
    - **entities** - ecs.

## How to use it

 Clone the repo into your project:

```bash

cd your_project/src && git clone https://github.com/willieLjohnson/pygg.git

```

### Hello World

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

### Example Project

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

from gg import bouncygame

```


```python

# src/bouncygame.py

import pygame
from gg import pygg as GG

class BouncyGame(GG.Game):
    debug = False
    def __init__(self):
        super().__init__('bouncy')
        self.speed_multiplier = 1
        self.style.background = GG.GGSTYLE.BLACK
        self.debug = False
        for _ in range(200):
            self._create_bouncy()
            
        self.box = GG.Box(self.space, (10, 10), (GG.SCREEN_WIDTH - 10, GG.SCREEN_HEIGHT - 10), 1, 0)
        
        self.rectangle = GG.Rectangle(self.space, size=(300,300), position=(GG.SCREEN_WIDTH / 2, GG.SCREEN_HEIGHT / 2))
        
    def run(self):
        self.clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self._handle_quit()
            self._handle_input()
            
            GG.main.fill(self.style.background) 
            
            self.clock.tick(60)
            self._update_space()
            self.entities.update()

            if self.debug:
                self.space.debug_draw(self._draw_options)
            self.entities.draw(GG.main)
            pygame.display.update()


        pygame.quit()
    
    def _create_bouncy(self):
        random_color = GG.gen_color()
        random_position = GG.gen_point(GG.SCREEN_WIDTH, GG.SCREEN_HEIGHT)
        random_size = GG.gen_range(1, 40)
        random_speed = GG.gen_range(-100000, 100000)
        random_velocity = GG.gen_vec2(random_speed, random_speed)
        shape = GG.Rectangle(self.space, random_position, GG.Vec2(random_size, random_size), random_color)
        bouncy = GG.Entity(self, "bouncy", shape, random_speed, random_velocity)
        self.entities.add(bouncy)
        
             
    def _handle_input(self):
        keys = pygame.key.get_pressed()  #checking pressed keys

        if keys[pygame.K_d]:
            self.debug = not self.debug

```

## Roadmap


### spec - Game, ECS, Collision

- [x] Game and loop
- [x] Components
  - [x] ID
  - [x] Body
  - [x] Stats
- [x] Entities
  - [x] Player
  - [x] entities
    - [x] Walls
    - [x] Actors
- [x] Systems
  - [x] Camera
  - [x] Collision

### v0.0.0 - Physics



### v0.1.0 - Managers

- [ ] Systems
- [ ] Scene
- [ ] Object
- [ ] Actors
- [ ] Sound
- [ ] Save

### v0.2.0 - Procedural generation

- [ ] ECS
- [ ] Map
- [ ] Art
- [ ] Sound

### v0.3.0 - VFX

- [ ] Particle system
- [ ] Lights
- [ ] Post processing
- [ ] Shaders

### v0.x.0 - TBD...

- [ ] Menus with easy navigation
- [ ] Prefabs to allow for easily creating entire scenes/entities
- [ ] Spritesheet and atlas for animations
- [ ] Sharing and saving seeds
- [ ] Map building through external tools/files
- [ ] Parallax scrolling
- [ ] Build for Web, Mobile, PC, and Mac
- [ ] Commandline tools
- [ ] Item pickups and inventory system
- [ ] Customizable weapons
- [ ] Achievments
