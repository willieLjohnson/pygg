import pygame
import src as GG

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
            self.gameobjects.update()

            if self.debug:
                self.space.debug_draw(self._draw_options)
            self.gameobjects.draw(GG.main)
            pygame.display.update()


        pygame.quit()
    
    def _create_bouncy(self):
        random_color = GG.gen_color()
        random_position = GG.gen_point(GG.SCREEN_WIDTH, GG.SCREEN_HEIGHT)
        random_size = GG.gen_range(1, 40)
        random_speed = GG.gen_range(-100000, 100000)
        random_velocity = GG.gen_vec2(random_speed, random_speed)
        shape = GG.Rectangle(self.space, random_position, GG.Vec2(random_size, random_size), random_color)
        bouncy = GG.GameObject(self, "bouncy", shape, random_speed, random_velocity)
        self.gameobjects.add(bouncy)
        
             
    def _handle_input(self):
        keys = pygame.key.get_pressed()  #checking pressed keys

        if keys[pygame.K_d]:
            self.debug = not self.debug

BouncyGame().run()
