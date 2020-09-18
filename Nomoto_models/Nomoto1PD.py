
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

command_heading = 90
velocity = 15

from scipy.integrate import solve_ivp

class Ship():

	def __init__(self):
		self.x = 100
		self.y = 750
		self.orientation = 0
		self.orientation_rate = 0
		self.psid = command_heading*np.pi/180
		self.T = 2.7257
		self.K = -1.6721
		self.vel = velocity
		self.wn2 = (2*np.pi/25)**2

		self.kp = (self.wn2)*self.T/self.K
		self.kd = (2*(self.T*self.K*self.kp)**0.5-1)/self.K

	def set(self, x, y,orientation):
		self.x = x
		self.y = y
		self.orientation = orientation

	def move(self,dt):

		self.x = self.x + self.vel*np.cos(self.orientation)*dt
		self.y = self.y - self.vel*np.sin(self.orientation)*dt
		
		self.orientation %= 2*np.pi
		self.x %= world_size
		self.y %= display_height

	def nomotoeqn(self,t,x): 
		psi = x[0]
		rp = x[1]
		delta = np.clip(x[2], a_min = -35*np.pi/180, a_max = 35*np.pi/180) 
		delta_dot = np.clip(self.kp*(self.psid-psi)-self.kd*rp-delta,a_min = -5*np.pi/180, a_max = 5*np.pi/180)
		xd = [rp, (self.K*delta-rp)/self.T,delta_dot]
		return xd

	def Nomoto(self,t,dt):

		sol = solve_ivp(self.nomotoeqn,[0,t],[0,0,0])
		self.orientation_rate = sol.y[1,-1]
		self.orientation = sol.y[0,-1]
		self.delta = sol.y[2,-1]
		print(f" r: {self.orientation_rate} \n phi:{self.orientation*180/np.pi} \n rudder:{self.delta*180/np.pi}\n")

	def draw(self):
		ship_img = pygame.image.load("ship.png")
		img = pygame.transform.rotate(ship_img, self.orientation*180/np.pi)
		screen.fill(background_colour)
		screen.blit(img, (self.x, self.y))
		pygame.draw.line(screen,(255,255,255),(self.x-display_width*np.cos(self.psid), self.y+display_width*np.sin(self.psid)),(self.x+display_width*np.cos(self.psid), self.y-display_width*np.sin(self.psid)), 3)



class Simulator(object):

	def main(self , screen , Ship):
		clock = pygame.time.Clock()
		Ship.draw()
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
			Ship.Nomoto((curr_time-start_time)/1000,(curr_time-prev_time)/1000)
			Ship.move((curr_time-prev_time)/1000)
			Ship.draw()
			pygame.display.flip()
			clock.tick(60)
			prev_time = curr_time

if __name__ == '__main__':
	pygame.init()
	pygame.display.set_caption("Nomoto_Ship_PD")
	screen = pygame.display.set_mode((display_width,display_height))
	Ship = Ship()
	Simulator().main(screen , Ship)