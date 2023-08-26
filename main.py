import sys
import math
import random
import pygame
from pygame.locals import *


'''
    ---- FIREWORKS SIMULATION ----

     # AUTHOR: MCKENZIE, REGALADO J.
     # DATE  : 12/28/2022
'''

class Firework :
	def __init__(self, SCREEN_SIZE) :
		self.pos = pygame.Vector2(random.randint(100, SCREEN_SIZE[0]-100), SCREEN_SIZE[1])
		self.vel = pygame.Vector2(random.uniform(-2.0, 2.0), random.uniform(-10.0, -12.0))
		self.GRAVITY = 0.2
		self.exploded = False

	def update(self) :
		self.vel.y += self.GRAVITY
		self.pos += self.vel
		if self.vel.y >= 2.0 :
			self.exploded = True

	def draw(self, surface) :
		pygame.draw.circle(surface, (255, 255, 175), self.pos, 5.0)


class Particle :
	def __init__(self, initial_pos) :
		self.pos = pygame.Vector2(initial_pos[0], initial_pos[1])
		self.angle = self.generateRandomAngle2D()
		self.vel = pygame.Vector2(self.angle.x, self.angle.y)
		self.vel *= random.uniform(1.0, 5.0)
		self.acc = 0.0
		self.GRAVITY = 0.05
		self.done = False
		self.r = random.randint(1, 255)
		self.g = random.randint(1, 255)
		self.b = random.randint(1, 255)
		self.alpha = 255
    
    # Make a new 2D unit vector from a random angle.
	def generateRandomAngle2D(self) :
		angle = random.random() * (2*math.pi)
		length = 1
		return (pygame.Vector2(length * math.cos(angle), length * math.sin(angle)))

	def update(self) :
		self.acc += self.GRAVITY
		self.vel.y += self.acc
		self.pos += self.vel
		self.acc *= 0.0

	def draw(self, surface) :
		self.alpha -= 5
		if self.alpha <= 0 :
			self.alpha = 0
			self.done = True
		pygame.draw.circle(surface, (self.r, self.g, self.b, self.alpha), self.pos, 2.0)

def main() :
	# Initialize pygame
	pygame.init()

	# Target Frame Rate
	FPS = 60
	fpsClock = pygame.time.Clock()

	# set the Windows Width and Height
	WIDTH, HEIGHT = 640, 480
	mainwindow = pygame.display.set_mode((WIDTH, HEIGHT))
	# mainwindow = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
	mainwindow.fill((0, 0, 0))

    # The surface where we draw.
	surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

	# List of Fireworks
	fireworks = []

	# number of particles for the explosion.
	n_particles = 32

	# List of particles
	particles = []
    
    # target time when the new firework is created.
	target_t = 0.0

	# Game loop
	status = 1
	while status :
		surface.fill((0, 0, 0, 30))

		# add FPS/1000.0 or 0.016 every frame.
		target_t += 0.016

        # Create new firework every one[1] second.
		if target_t >= 1.0 :
			fireworks.append(Firework((WIDTH, HEIGHT)))
			target_t = 0.0


		''' Note: To boost the performance of this application it is important to 
		remove each object in the list when it's done. '''

        # Check if there are fireworks in the list.
		if (len(fireworks) > 0) :
			# If so, update and draw each firework.
			for f in fireworks :
				f.update()
				f.draw(surface)
				# if the firework exploded,
				if f.exploded == True :
					# remove it from the list
					fireworks.remove(f)
					# Then, generate n particles for the explosion.
					for n in range(n_particles) :
						particles.append(Particle((f.pos.x, f.pos.y)))

		# Check if there are particles in the list.
		if len(particles) >= 0 :
			# If so, update and draw each particle.
			for p in particles :
				p.update()
				p.draw(surface)
				# If the particle is done
				if p.done == True :
					# remove it from the list.
					particles.remove(p)

		# Handle inputs
		for event in pygame.event.get() :
			if event.type == QUIT :
				status = 0
				pygame.quit()
				sys.exit()

		mainwindow.blit(surface, (0, 0))
		pygame.display.flip()
		fpsClock.tick(FPS)

if __name__ == "__main__" :
	main()