import globals

class Health:

	def __init__(self, player):
		self.player = player															# Current player, 1 or 2
		self.w = globals.health_bar_width												# Width of health bar
		self.h = globals.health_bar_height												# Height of health bar
		self.x = globals.horizontal_health_bar_position[player - 1] - self.w // 2 		# Converting centre x to upperleft x
		self.y = globals.vertical_health_bar_position - self.h // 2 					# Converting centre y to upperleft y
		self.health = 100																# Stores remaining health of the player (0 to 100)
		self.colour = [103, 235, 52]													# Stores the colour of health bar
		self.animate = 0																# Variable that regulates the animation of changing health

	# Draws the rectangle
	def make_health_bar(self):
		fill(self.colour[0], self.colour[1], self.colour[2])  							# Setting the colour of the health bar
		noStroke()
		rect(self.x, self.y, int(self.w * self.health / 100), self.h)  					# Fills remaining health
		noFill()
		stroke(0)
		strokeWeight(2)
		rect(self.x, self.y, self.w, self.h)											# Outline of the health bar

	# Draws the rectangle and updates the colour
	def display(self):
		self.make_health_bar()
		self.animate_colour()

	# Linearly transitions between two colours
	def interpolate(self, colour_1, colour_2,lower):
		for i in range(3):
			self.colour[i] = int(colour_2[i] - ((self.health - lower)/25)*(colour_2[i] - colour_1[i]))

	# Chooses the boundaries colour
	def change_colour(self):
		if self.health >= 75:
			temp_2 = [51, 254, 51]
			temp_1 = [153, 204, 0]
			lower = 75
		elif self.health >=50:
			temp_2 = [153, 204, 0]
			temp_1 = [180, 204, 0]
			lower = 50
		elif self.health >=25:
			temp_2 = [180, 204, 0]
			temp_1 = [179, 179, 0]
			lower = 25
		elif int(self.health) > 0:
			temp_2 = [179, 179, 0]
			temp_1 = [180, 41, 0]
			lower = 0
		else:
			self.health = 0
			return None							# No interpolation of colour when health is 0
		self.interpolate(temp_2, temp_1, lower)
			
	# Decrements health quickly in the begining and slowly towards the end
	def animate_colour(self):
		if int(self.animate) != 0:
			self.animate = self.animate - (1 + self.animate / 20)			# Non-linear, decreasing speed
			self.health = self.health - (1 + self.animate / 20)				# Decrements health too
		else:
			self.animate = 0     		# Resets the animate to 0
		self.change_colour()			# Changes the colour of health bar if required

	# Initialised the value of animate so that it triggers animate colour
	def change_health(self, damage):
		self.animate = damage
	

# class Power:

# 	def __init__(self, player):
# 		self.x = globals.horizontal_power_bar_position[player - 1]
# 		self.y = globals.vertical_power_bar_position
# 		self.w = globals.power_bar_width
# 		self.h = globals.power_bar_height
# 		self.health = 100
# 		self.colour = [103, 235, 52]
# 		self.power = 0

# 	def display(self):
# 		noFill()
# 		rect(self.x, self.y, self.w, self.h)							# Outline of the health bar
# 		fill(self.colour[0], self.colour[1], self.colour[2])			# Setting the colour of the health bar
# 		rect(self.x, self.y, int(self.w * self.power / 100), self.h)	# Remaining health as colour

# 	# Converts velocity into scale of 0 to 100, where 0 is the min velocity and 100 is the max velocity 
# 	def change_power(self, velocity):
# 		self.power = int(100 * (velcoity - globals.default_bullet_min_velocity)/ (globals.default_bullet_max_velocity - globals.default_bullet_min_velocity)
