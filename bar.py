import globals

class Bar:

	def __init__(self, player, x, y, w, h):
		self.player = player											# Current player, 1 or 2
		self.w = w														# Width of bar
		self.h = h														# Height of bar
		self.x = x														# Centre X
		self.y = y				 										# Centre Y
		self.upper_x, self.upper_y = self.get_upper_left()				# Converting center of bar to upper_left corners
		self.colour = [103, 235, 52]									# Stores the colour of bar

	def get_upper_left(self):
		return self.x - self.w //2, self.y - self.h //2

	# Draws the rectangle
	def make_bar(self, parameter):
		noStroke()
		fill(255)
		rect(self.upper_x, self.upper_y, self.w, self.h)
		fill(self.colour[0], self.colour[1], self.colour[2])  							# Setting the colour of the bar
		rect(self.upper_x, self.upper_y, int(self.w * parameter/ 100), self.h)  		# Fills only a portion of the rectangle
		noFill()
		stroke(0)
		strokeWeight(1)
		rect(self.upper_x, self.upper_y, self.w, self.h)								# Outline of the bar

	# Draws the rectangle and updates the colour
	def display(self, parameter):
		self.make_bar(parameter)

	# Linearly transitions between two colours
	def interpolate(self, colour_1, colour_2,lower, parameter):
		for i in range(3):
			self.colour[i] = int(colour_2[i] - ((parameter - lower)/25)*(colour_2[i] - colour_1[i]))

	# Chooses the boundaries colour
	def change_colour(self, parameter):
		if parameter >= 75:
			temp_2 = [51, 254, 51]
			temp_1 = [153, 204, 0]
			lower = 75
		elif parameter >=50:
			temp_2 = [153, 204, 0]
			temp_1 = [180, 204, 0]
			lower = 50
		elif parameter >=25:
			temp_2 = [180, 204, 0]
			temp_1 = [179, 179, 0]
			lower = 25
		elif parameter >= 0:
			temp_2 = [179, 179, 0]
			temp_1 = [180, 41, 0]
			lower = 0
		else:
			return 0							# No interpolation for out of range values
		self.interpolate(temp_2, temp_1, lower, parameter)


class Health(Bar):

	def __init__(self, player):
		Bar.__init__(self, player, globals.horizontal_health_bar_position[player - 1], globals.vertical_health_bar_position, globals.bar_width, globals.bar_height)
		self.health = 100																# Stores remaining health of the player (0 to 100)
		self.animate = 0  																# Variable that regulates the animation of changing health

	# Decrements health quickly in the beginning and slowly towards the end
	def animate_colour(self):
		if int(self.animate) != 0:
			self.animate = self.animate - (1 + self.animate / 20)			# Non-linear, decreasing speed
			self.health = self.health - (1 + self.animate / 20)				# Decrements health too
		else:
			self.animate = 0     											# Resets the animate to 0
		self.change_colour(self.health)										# Changes the colour of health bar if required

	# Initialised the value of animate so that it triggers animate colour
	def change_health(self, damage):
		self.animate = damage

	# Changing the health bar dynamically while being displayed
	def display(self):
		Bar.display(self, self.health)
		self.animate_colour()


class Power(Bar):

	def __init__(self, player):
		Bar.__init__(self, player, globals.horizontal_power_bar_position[player - 1], globals.vertical_power_bar_position, globals.bar_width, globals.bar_height)
		self.current_power = 0													# Current velocity of the player as compared to the max possible velocity

	# Changes the value of based on the argument passed
	def change_level(self, velocity):
		self.current_power = int(100 * velocity / globals.default_bullet_max_velocity)
		self.change_colour(100 - self.current_power)

	# Dislays the power bar with a label
	def display(self):
		fill(0)
		textAlign(CENTER, CENTER)
		text("Power", self.x, self.y - 30)
		Bar.display(self, self.current_power)
