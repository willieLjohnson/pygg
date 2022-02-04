from dataclasses import dataclass
import pygame
import pymunk
import pymunk.pygame_util


from . import style
from . import display

@dataclass
class Game:
    name = ""
    entities = pygame.sprite.Group()
    style = style.GGSTYLE()
    space: pymunk.Space
    _draw_options: pymunk.pygame_util.DrawOptions
    screen: display.Screen
    
    def __init__(self, name, width = 800, height = 600):
        self.name = name
        self.screen = display.Screen(width, height)
        
        pygame.init()
        pygame.display.set_caption(name)
        self.space = pymunk.Space()
        self._draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.clock = pygame.time.Clock()


    def run(self):
        self.running = 1
        while self.running == 1:
            self._handle_quit()
            self.screen.clear(self.style.BLACK)
            hello = self.style.FONT.render("hi", False, style.GGSTYLE.GREEN)
            self.entities.draw(self.screen)
            self.screen.blit(hello, (self.screen.width / 2 - hello.get_rect().w / 2, self.scree.height / 2 - hello.get_rect().h / 2))
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        
                    
    def _handle_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = 0
    
    def _update_space(self):
        self.space.step(1/60)
                
    
    def addobject(self, object):
        self.entities.addobject(object)

    def addtospace(self, body):
        self.space.add(body)