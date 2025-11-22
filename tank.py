import os
import globals as gb

class Tank:

	def __init__(self, player, x, angle):
		self.player = player
		self.x = x
		self.y = gb.ground_level - gb.default_tank_radius
		self.angle = angle
		self.vleft = 0
		self.vright = 0
		self.pics = []
		self.moving_phase = True			# Flag for the phase where the tank can move left and right
		self.angle_phase = False  			# Flag for the phase where the tank's nozzle changes its angle
		for i in range(9):
			name = "Tank " + str(i * 10) + ".png"
			self.pics.append(loadImage(os.getcwd() + r"\\Tank images" + "\\" + name))

	# Sets velocity when key is pressed
	def key_press(self, input_key, input_key_code):
		if self.moving_phase != 0:						# if the player is allowed to move then only unlock controls
			if self.player == 1:						# if player 1, then only unlock the ASW keys
				if input_key == 'd':
					self.vleft = 5
				if input_key == 'a':
					self.vright = -5
				if input_key == 's':
					self.moving_phase = False
			if self.player == 2:						# if player 2, then only unlock the arrow keys
				if input_key_code == RIGHT:
					self.vleft = 5
				if input_key_code == LEFT:
					self.vright = -5
				if input_key_code == DOWN:
					self.moving_phase = False
		else:											# if not allowed to move then reset the velocity
			self.vleft = 0
			self.vright = 0
			self.angle_phase = True						# Angle phase comes directly after the player fixes his position

	# Rests the velcoity to zero when the key is released
	def key_release(self, input_key, input_key_code):
		if self.player == 1:
			if input_key == 'd':
				self.vleft = 0
			if input_key == 'a':
				self.vright = 0
		if self.player == 2:
			if input_key_code == RIGHT:
				self.vleft = 0
			if input_key_code == LEFT:
				self.vright = 0

	# Updates the horizontal position
	def move(self):
		self.x = self.x + self.vleft + self.vright
		if self.player == 1:
			if self.x < gb.p1_limit[0]:			# Checks left limit for player 1 and restricts
				self.x = gb.p1_limit[0]
			if self.x > gb.p1_limit[1]:			# Checks right limit for player 1 and restricts
				self.x = gb.p1_limit[1]
		if self.player == 2:
			if self.x < gb.p2_limit[0]:			# Checks left limit for player 2 and restricts
				self.x = gb.p2_limit[0]
			if self.x > gb.p2_limit[1]:			# Checks right limit for player 2 and restricts
				self.x = gb.p2_limit[1]

	# Generates the upper_left corner of the image
	def get_upper_left(self):
		return self.x - gb.default_tank_width // 2, self.y - gb.default_tank_height // 2

	# Displays the tank
	def display(self):
		upper_x, upper_y = self.get_upper_left()
		image(self.pics[self.angle // 10], upper_x, upper_y, gb.default_tank_width, gb.default_tank_height, 150*(2 - self.player), 0, 150*(self.player - 1), 178)
