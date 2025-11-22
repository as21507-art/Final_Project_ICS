import os, math
import globals as gb

class Tank:

	def __init__(self, player, x, angle):
		self.player = player
		self.x = x
		self.y = gb.ground_level - gb.default_tank_radius
		self.angle = angle 					# Current angle of the nozzle
		self.angle_increase = False			# Flag for whether the nozzle is moving upwards or downwards
		self.vleft = 0 						# Velocity due to left key press
		self.vright = 0 					# Velocity due to right key press
		self.moving_phase = True			# Flag for the phase where the tank can move left and right
		self.angle_phase = False  			# Flag for the phase where the tank's nozzle changes its angle
		self.velocity_phase = False
		self.mouse_start_x = 0
		self.mouse_start_y = 0
		self.distance = 0
		self.velocity = 0
		# Creating list of picture of the tank at different angles
		self.pics = []						
		for i in range(9):
			name = "Tank " + str(i * 10) + ".png"
			self.pics.append(loadImage(os.getcwd() + r"\\Tank images" + "\\" + name))

	# Sets velocity when key is pressed
	def key_press(self, input_key, input_key_code):
		if self.moving_phase:
			if self.player == 1:						# if player 1, then only unlock the ASW keys
				if input_key == 'd':
					self.vleft = 5
				if input_key == 'a':
					self.vright = -5
				if input_key == 's':
					self.moving_phase = False
					self.angle_phase = True     		# Angle phase comes directly after the player fixes his position
					self.vleft = 0
					self.vright = 0
			if self.player == 2:						# if player 2, then only unlock the arrow keys
				if input_key_code == RIGHT:
					self.vleft = 5
				if input_key_code == LEFT:
					self.vright = -5
				if input_key_code == DOWN:
					self.moving_phase = False
					self.angle_phase = True     		# Angle phase comes directly after the player fixes his position
					self.vleft = 0
					self.vright = 0
		
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

	# Animates the angle of the tank's nozzle
	def animate_angle(self):
		if frameCount % 12 == 0: 					# Slows down the animation
			if self.angle_increase:
				self.angle += 10
				if self.angle == 80:
					self.angle_increase = False		# Decreasing phase starts at 80 degrees
			else:
				self.angle -= 10
				if self.angle == 0:
					self.angle_increase = True		# Increasing phase starts at 0 degrees

	# Stops angle animation and records the point where the mouse is clicked
	def mouse_click(self, centreX, centreY):
		if self.angle_phase:											# This only works in angle phase, not in moving phase
			self.angle_phase = False									# Stops angle animation
			self.velocity_phase = True									# Enables velocity selection
			self.mouse_start_x, self.mouse_start_y = centreX, centreY

	# displays a circle and the cross on the screen
	def fiducial_marker(self):
		noFill()
		ellipse(self.mouse_start_x, self.mouse_start_y, gb.fiducial_scope, gb.fiducial_scope)
		line(self.mouse_start_x + int(gb.fiducial_scope * 1.5), self.mouse_start_y, self.mouse_start_x + int(gb.fiducial_scope * 1.5) + gb.fiducial_line, self.mouse_start_y)
		line(self.mouse_start_x - int(gb.fiducial_scope * 1.5) - gb.fiducial_line, self.mouse_start_y, self.mouse_start_x - int(gb.fiducial_scope * 1.5), self.mouse_start_y)
		line(self.mouse_start_x, self.mouse_start_y + int(gb.fiducial_scope * 1.5), self.mouse_start_x, self.mouse_start_y + int(gb.fiducial_scope * 1.5) + gb.fiducial_line)
		line(self.mouse_start_x, self.mouse_start_y - int(gb.fiducial_scope * 1.5) - gb.fiducial_line, self.mouse_start_x, self.mouse_start_y - int(gb.fiducial_scope * 1.5))

	# Selects the velocity of the bullet:
	def velocity_selector(self):
		self.display
		self.distance = pow((mouseX - self.mouse_start_x)**2 + (mouseY - self.mouse_start_y)**2, 0.5)
		factor = min(1, self.distance/gb.drag_limit)
		if factor > 0.2:
			self.velocity = int(gb.default_bullet_max_velocity * factor)
		else:
			self.velocity = 0

	# Displays the tank
	def display(self):
		upper_x, upper_y = self.get_upper_left()
		image(self.pics[self.angle // 10], upper_x, upper_y, gb.default_tank_width, gb.default_tank_height, 150*(2 - self.player), 0, 150*(self.player - 1), 178)

	# Manipulates the tank based on the current phase of the game
	def tank_action(self):
		if self.moving_phase:
			self.move()
		elif self.angle_phase:
			self.animate_angle()
		elif self.velocity_phase:
			self.fiducial_marker()
			self.velocity_selector()
