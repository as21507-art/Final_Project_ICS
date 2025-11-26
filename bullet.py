import math
import globals

class Bullet:

	def __init__(self, player, tank_x, tank_y, tank_radius, velocity, angle, mode = "default"):
		angle = math.radians(angle)
		self.direction = math.pow(-1, player + 1)					# Since they are facing opposite directions, x values will be either incremented or decremented
		self.x = int(tank_x + self.direction * math.cos(angle) * (tank_radius + globals.default_tank_nozzle))    	# Initial x coordinate of the bullet
		self.y = int(tank_y - math.sin(angle) * (tank_radius + globals.default_tank_nozzle))						# Initial y coordinate of the bulelt
		self.vx = velocity * math.cos(angle)                       		# Initial horizontal velocity of the bullet
		self.vy = - velocity * math.sin(angle)                       	# Initial vertical velocity of the bullet
		self.r = globals.default_bullet_size // 2                       # Raidus of the bullet
		self.landed = False                                          	# Flag to check if the bullet has landed
		self.range = globals.default_bullet_range
		self.damage = globals.default_bullet_damage
		# Add bullet image

	def gravity(self):
		self.vy = self.vy + globals.gravity_effect							# Applies gravity only to the vertical velocity

	# Handles the case when the bullet attemps to go below the ground
	def adjust_landing(self):
		self.x = self.x + self.direction * self.vx * (globals.ground_level - self.y) / self.vy    	# Linearly approximates the horizontal position
		self.y = globals.ground_level - self.r 														# Rests the vertical position to ground level

	# Defines the trajectory of the bullet
	def follow_trajectory(self):
		if self.y + self.vy >= globals.ground_level - self.r:           # If bullet crossed the ground then reset it to the ground
			self.adjust_landing()
			self.landed = True
		else:                                                           # Otherwise, update horizontal and vertical positions
			self.x = self.x + self.direction * self.vx										
			self.y = self.y + self.vy
			self.gravity() 												# Changes vertical velocity under gravity

	# Moves the bullet if it has not yet landed
	def move(self):
		if not self.landed:
			if frameCount % 8 == 0:										# Slows down the animation of bullet
				self.follow_trajectory()
		return self.x, self.y

	# Calculates horizontal distance between bullet and another tank
	def distance(self, another_x):
		return max(self.x - another_x, another_x - self.x)

	# Calculates damage linearly based on range
	def get_damage(self, enemy_x):
		damaging_factor = 1 - self.distance(enemy_x) / self.range       # value is negative if the bullet is out of range
		return max(0, self.damage * damaging_factor)  					# returns the value if positive, otherwise returns 0

	# Displays the bullet at its current coordinates
	def display(self):
		# Display image
		stroke(0)
		fill(0)
		ellipse(int(self.x), int(self.y), 2 * self.r, 2 * self.r)
		self.move()
