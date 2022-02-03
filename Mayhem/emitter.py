# coding=utf-8
''' Author - Torkel Syversen, University of Tromsø '''
import pygame
import random
import util

class Emitter:
    ''' A class to create, update and render particles. '''
    def __init__(self):
        self.emitter_list = []
        self.color = (255, 255, 255)

    def add(self, amount, x, y, width, height):
        ''' Adds particles to a random position, where x and y is centered.
        '''
        for i in range(0, amount):
            pos_x = random.randrange(int(x-width/2), int(x+width/2))
            pos_y = random.randrange(int(y-height/2), int(y+height/2))
            self.emitter_list.append(Particle(pos_x, pos_y))

    def add_rect(self, amount, x, y, width, height):
        ''' Adds particles to a random position between the specified parameters. '''
        for i in range(0, amount):
            pos_x = random.randrange(int(x), int(x+width))
            pos_y = random.randrange(int(y), int(y+height))
            p = Particle(pos_x, pos_y, .5, 1, 3, 8)
            p.color = self.color
            self.emitter_list.append(p)

    def add_stars(self, amount, x, y):
        for i in range(0, amount):
            self.emitter_list.append(Star(random.randrange(0, x), random.randrange(0, y)))

    def update(self, delta):
        for particle in self.emitter_list:
            if particle.life > 0.0:
                # Lerps size to 0 based on scale_speed
                particle.particle.x = particle.x
                particle.particle.y = particle.y
                particle.size = util.lerp(particle.size, 0, particle.scale_speed*delta)
                particle.set_size(particle.size)
                particle.life -= delta
            else:
                self.emitter_list.remove(particle)
                continue

    def update_stars(self, delta):
        for particle in self.emitter_list:
            particle.particle.x = particle.x
            particle.particle.y = particle.y



    def render(self, screen, cam):
        for particle in self.emitter_list:
            particle.particle.x += cam.x
            particle.particle.y += cam.y
            pygame.draw.rect(screen, particle.color, particle.particle)
            particle.particle.x -= cam.x
            particle.particle.y -= cam.y

class Particle:
    def __init__(self, x, y, sl=.2, el=.5, sc=12, ec=96):
        self.life = random.uniform(sl, el)
        # Scale speed is multiplied by delta,
        self.scale_speed = random.randrange(sc, ec)
        self.x = x
        self.y = y
        self.color = (255, 255, 255)
        self.size = 15.0
        self.particle = pygame.Rect(x, y, self.size, self.size)

    def set_size(self, size):
        self.particle.width = size
        self.particle.height = size
    def set_color(c):
        self.color = c

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (250, 200, 0)
        self.size = random.randrange(0, 2)
        self.particle = pygame.Rect(x, y, self.size, self.size)
