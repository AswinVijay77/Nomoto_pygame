
import pygame
import numpy as np

"""Define color"""
red = (200, 0, 0)
blue = (135, 206, 235)
green = (0, 155, 0)
yellow = (155, 155, 0)
white = (255, 255, 255)
black = (0, 0, 0)
background_colour = blue

display_width = 1500
display_height = 900
world_size = display_width

rudder = 30		# Set rudder anglr in degrees
velocity = 20	# Set velocity in m/s

class robot():

	def __init__(self):
		self.x = 100
		self.y = 800
		self.orientation = 0
		self.delta0 = rudder*(np.pi/180)
		self.T = 4.8
		self.K = 0.08
		self.vel = velocity

	def set(self, x, y,orientation):
		self.x = x
		self.y = y
		self.orientation = orientation

	def move(self,dt):

		self.x = self.x + self.vel*np.cos(self.orientation)*dt
		self.y = self.y - self.vel*np.sin(self.orientation)*dt
		print(self.orientation*180/np.pi)
		
		self.orientation %= 2*np.pi
		self.x %= world_size
		self.y %= display_height

	def Nomoto(self,t):
		self.orientation = self.K*self.delta0*(t- self.T + self.T*np.exp(-t/self.T))

	def draw(self):
		car_img = pygame.image.load("ship.png")
		img = pygame.transform.rotate(car_img, self.orientation*180/np.pi)
		screen.fill(background_colour)
		screen.blit(img, (self.x, self.y))
		self.px = self.x
		self.py = self.y

class Simulator(object):

	def main(self , screen , robot):
		clock = pygame.time.Clock()
		robot.draw()
		delta_orient = 0.0
		delta_forward = 0.0
		loop = True
		start_time = pygame.time.get_ticks()
		prev_time = 0
		curr_time = 0
		while loop:
			curr_time = pygame.time.get_ticks()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			robot.Nomoto((curr_time-start_time)/1000)
			robot.move((curr_time-prev_time)/1000)
			robot.draw()
			pygame.display.flip()
			clock.tick(60)
			prev_time = curr_time

if __name__ == '__main__':
	pygame.init()
	pygame.display.set_caption("Nomoto_Ship")
	screen = pygame.display.set_mode((display_width,display_height))
	robot = robot()
	Simulator().main(screen , robot)