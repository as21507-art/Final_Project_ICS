import math, os
import globals

class Bullet:

	def __init__(self, player, tank_x, tank_y, tank_radius, velocity, angle, sound_player):
		angle = math.radians(angle)
		# For player 1, X values are incremented (+1 or bullet moves to right) and for player 2, X values are decremented (-1 or bullet moves to left)
		self.direction = math.pow(-1, player + 1)
		self.x = int(tank_x + self.direction * math.cos(angle) * (tank_radius + globals.default_tank_nozzle))    	# Initial x coordinate of the bullet
		self.y = int(tank_y - math.sin(angle) * (tank_radius + globals.default_tank_nozzle))						# Initial y coordinate of the bullet
		self.vx = velocity * math.cos(angle)                       		# Initial horizontal velocity of the bullet
		self.vy = - velocity * math.sin(angle)                       	# Initial vertical velocity of the bullet
		self.r = globals.default_bullet_size // 2                       # Radius of the bullet
		self.landed = False                                          	# Flag to check if the bullet has landed
		self.range = globals.default_bullet_range						# Max range beyond which bullet does not deal damage to opponent
		self.damage = globals.default_bullet_damage						# Maximum damage that can be caused with direct hit
		self.shooting_noise = sound_player.loadFile(os.getcwd() + r"\\sounds\shooting.mp3")			# Sound for shooting effect
		self.shooting_noise.play()
		self.explosion_noise = sound_player.loadFile(os.getcwd() + r"\\sounds\exploding.mp3")
		self.explode_count = 0	 											# Flag to animate the explosion effect
		self.explosion_frames = 20											# Max number of frames in explosion sprite
		self.explosive = loadImage(os.getcwd() + r"\\images\Explosion.png") # Sprite for explosion (20 frames)
		self.square_size = 50												# Size of images for explosion
		# Add bullet image

	# Applies gravity only to the vertical velocity
	def gravity(self):
		self.vy = self.vy + globals.gravity_effect

	# Handles the case when the bullet attempts to go below the ground
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
		if frameCount % 8 == 0:										# Slows down the animation of bullet
			self.follow_trajectory()

	# Calculates horizontal distance between bullet and another tank
	def distance(self, another_x):
		return max(self.x - another_x, another_x - self.x)

	# Calculates damaging factor using inverse square law
	def get_damage(self, enemy_x):
		damaging_factor = 1 - (self.distance(enemy_x) / self.range) ** 2       # value is negative if the bullet is out of range
		return max(0, self.damage * damaging_factor) 	 				       # returns the value if positive, otherwise returns 0

	# Displays the bullet at its current coordinates
	def display(self):
		stroke(255)
		fill(0)
		ellipse(int(self.x), int(self.y), 2 * self.r, 2 * self.r)

	# Animates the explosion when the bullet lands
	def explosion(self):
		if self.explode_count == 0:						# Playing the sound when the explosion begins
			self.explosion_noise.rewind()
			self.explosion_noise.play()
		# Cropping the images (sprite)
		upper_x = (self.explode_count % 5) * 50
		upper_y = (self.explode_count // 5) * 50
		image(self.explosive, self.x - self.square_size // 2, self.y - self.square_size //2, self.square_size, self.square_size, upper_x, upper_y, upper_x + self.square_size, upper_y + self.square_size)
		self.explode_count = self.explode_count + 1		# Proceeds to next frame
