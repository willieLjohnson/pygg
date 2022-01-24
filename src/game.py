from dataclasses import dataclass
import pygame

from . import style
from . import screen


@dataclass
class Game:
    name = ""
    gameobjects = pygame.sprite.Group()
    style = style.GGSTYLE()
    
    def __init__(self, name):
        self.name = name
        pygame.init()
        pygame.display.set_caption(name)
        
    def run(self):
        self.clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self.clock.tick(60)
            self._handle_quit()
            screen.main.fill(style.GGSTYLE.BLACK)
            hello = self.style.FONT.render("hi", False, style.GGSTYLE.GREEN)
            self.gameobjects.draw(screen.main)
            screen.main.blit(hello, (screen.SCREEN_WIDTH / 2 - hello.get_rect().w / 2, screen.SCREEN_HEIGHT / 2 - hello.get_rect().h / 2))
            pygame.display.update()

        pygame.quit()
        
                    
    def _handle_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
        