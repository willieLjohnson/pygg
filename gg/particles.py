import random
import uuid
import pygame

from dataclasses import dataclass

from . import display

class Particle:
    def __init__(self, pos, dir = (1,1)):
        self.id = uuid.uuid4()
        self.x, self.y = pos[0], pos[1]
        self.vx, self.vy = random.randint(-2, 2) * dir[0], random.randint(-2, 2) * dir[1]
        self.rad = 10

    def draw(self, screen: display.Screen):
        screen.draw_particle(self)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if random.randint(0, 100) < 20:
            self.rad -= 1
            self.vx *= 0.5
            self.vy *=  0.5

@dataclass
class ParticleEffect:
    id: uuid.UUID
    
class Dust(ParticleEffect):
    def __init__(self, pos, dir = (1,1)):
        self.id = uuid.uuid4()
        self.pos = pos
        self.particles = {}
        self._dead_particles = {}
        self.completed = False
        
        for i in range(2):
            particle = Particle(self.pos, (dir[0] * i, dir[1] * i))
            self.particles[particle.id] = particle

    def update(self):
        if self.completed: return
        
        for particle in self.particles.values():
            if particle.rad <= 0: 
                self._dead_particles[particle.id] = particle
            else:
                particle.update()
        
        if len(self._dead_particles) == len(self.particles):
            self.completed = True
        


    def draw(self, win):
        if self.completed: return
        
        for particle in self.particles.values():
            particle.draw(win)
        