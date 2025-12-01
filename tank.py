import os, math
import globals

class Tank:

	def __init__(self, player, x, angle):
		self.player = player				# Current player, 1 or 2
		self.x = x							# Horizontal position of the tank
		self.y = globals.ground_level - globals.default_tank_radius			# Vertical position always fixed as constant
		# Flag for the phase where the tank can move left and right
		self.moving_phase = True
		self.vleft = 0  					# Velocity due to left key press
		self.vright = 0  					# Velocity due to right key press
		# Flag for the phase where the tank's nozzle changes its angle
		self.angle_phase = False
		self.angle = angle 					# Current angle of the nozzle
		self.angle_increase = True			# Flag for whether the nozzle is moving upwards or downwards
		# Flag for the phase where the user can drag their mouse to select velocity
		self.velocity_phase = False
		self.mouse_start_x = 0				# X coordinate of click and hold
		self.mouse_start_y = 0				# Y coordinate of click and hols
		self.distance = 0					# Distance between drag and initial click
		self.velocity = 0					# Calculated velocity of the bullet
		# Flag for the phase where the tank stops all activity and shoots bullet
		self.bullet_phase = False
		# List storing images of tank of different angles
		self.pics = []						
		for i in range(9):
			name = "Tank " + str(i * 10) + ".png"
			self.pics.append(loadImage(os.getcwd() + r"\\Tank images" + "\\" + name))

	# Sets velocity when key is pressed
	def key_press(self, input_key, input_key_code):
		if self.moving_phase:
			if self.player == 1:						# if player 1, then only unlock the ASW keys
				if input_key == 'a':
					self.vleft = 5						# Tank moves left with 'a' key
				if input_key == 'd':
					self.vright = 5						# Tank moves right with 'd' key
				if input_key == 's':
					self.moving_phase = False
					self.angle_phase = True     		# Angle phase comes directly after the player fixes the position
					self.vleft = 0
					self.vright = 0
			if self.player == 2:						# if player 2, then only unlock the arrow keys
				if input_key_code == LEFT:
					self.vleft = 5						# Tank moves left with left arrow key
				if input_key_code == RIGHT:
					self.vright = 5						# Tank moves right with right arrow key
				if input_key_code == DOWN and self.player == 2:
					self.moving_phase = False
					self.angle_phase = True     		# Angle phase comes directly after the player fixes the position
					self.vleft = 0
					self.vright = 0
		elif self.angle_phase:
			if self.player == 1 and input_key == 's':						# Player 1 can toggle between angle phase and moving phase
				self.moving_phase = True
				self.angle_phase = False
			if self.player == 2 and input_key_code == DOWN:					# Player 2 can toggle between angle phase and moving phase
				self.moving_phase = True
				self.angle_phase = False

		
	# Rests the velocity to zero when the corresponding key is released
	def key_release(self, input_key, input_key_code):
		if self.player == 1:
			if input_key == 'a':
				self.vleft = 0
			if input_key == 'd':
				self.vright = 0
		if self.player == 2:
			if input_key_code == LEFT:
				self.vleft = 0
			if input_key_code == RIGHT:
				self.vright = 0

	# Updates the horizontal position
	def move(self):
		self.x = self.x - self.vleft + self.vright
		if self.player == 1:
			if self.x < globals.p1_limit[0]:			# Checks left limit for player 1 and restricts
				self.x = globals.p1_limit[0]
			if self.x > globals.p1_limit[1]:			# Checks right limit for player 1 and restricts
				self.x = globals.p1_limit[1]
		if self.player == 2:
			if self.x < globals.p2_limit[0]:			# Checks left limit for player 2 and restricts
				self.x = globals.p2_limit[0]
			if self.x > globals.p2_limit[1]:			# Checks right limit for player 2 and restricts
				self.x = globals.p2_limit[1]

	# Generates the upper_left corner of the image
	def get_upper_left(self):
		return self.x - globals.default_tank_width // 2, self.y - globals.default_tank_height // 2

	# Animates the angle of the tank's nozzle
	def animate_angle(self):
		if frameCount % 12 == 0: 					# Slows down the animation
			if self.angle_increase:
				self.angle += 10					# Increments the angle for nozzle in increasing phase
				if self.angle == 80:
					self.angle_increase = False		# Decreasing phase for nozzle starts at 80 degrees
			else:
				self.angle -= 10					# Decrements the angle for nozzle in decreasing phase
				if self.angle == 0:
					self.angle_increase = True		# Increasing phase for nozzle starts at 0 degrees

	# Stops tank motions and proceeds to velocity selector
	def mouse_press(self, centreX, centreY):
		if self.angle_phase or self.moving_phase:
			self.angle_phase = False										# Stops angle animation
			self.moving_phase = False										# Stops motion of the tank
			self.velocity_phase = True										# Enables velocity selection
			self.mouse_start_x, self.mouse_start_y = centreX, centreY 		# Records position of click and hold

	# Records the velocity and proceeds to shooting bullets if the velocity is selected, otherwise goes again to the moving phase
	def mouse_release(self):
		if self.velocity_phase:												# Prevents from shooting when it's not velocity phase
			self.velocity_selector()										# Calculates the velocity using distance of drag
			if self.velocity == 0:
				self.moving_phase = True									# Minimal drag means no velocity selected, start again
			else:
				self.bullet_phase = True									# Proceed to shooting bullet
			self.velocity_phase = False										# All tank related phases come to end, no more interactivity after shooting

	# Displays a circle and the cross on the screen as the starting point of drag
	def fiducial_marker(self):
		noFill()
		stroke(0)
		strokeWeight(2)
		ellipse(self.mouse_start_x, self.mouse_start_y, globals.fiducial_scope, globals.fiducial_scope)
		line(self.mouse_start_x + int(globals.fiducial_scope * 1.5), self.mouse_start_y, self.mouse_start_x + int(globals.fiducial_scope * 1.5) + globals.fiducial_line, self.mouse_start_y)
		line(self.mouse_start_x - int(globals.fiducial_scope * 1.5) - globals.fiducial_line, self.mouse_start_y, self.mouse_start_x - int(globals.fiducial_scope * 1.5), self.mouse_start_y)
		line(self.mouse_start_x, self.mouse_start_y + int(globals.fiducial_scope * 1.5), self.mouse_start_x, self.mouse_start_y + int(globals.fiducial_scope * 1.5) + globals.fiducial_line)
		line(self.mouse_start_x, self.mouse_start_y - int(globals.fiducial_scope * 1.5) - globals.fiducial_line, self.mouse_start_x, self.mouse_start_y - int(globals.fiducial_scope * 1.5))

	# Selects the velocity of the bullet:
	def velocity_selector(self):
		self.distance = pow((mouseX - self.mouse_start_x)**2 + (mouseY - self.mouse_start_y)**2, 0.5) 		# Distance of drag using distance formula
		factor = min(1, self.distance/globals.drag_limit)													# Converts into a scale from 0 to 1 to be applied to max velocity
		if factor > globals.bullet_velocity_min_factor:														# Checks for threshold minimum speed of bullet
			self.velocity = int(globals.default_bullet_max_velocity * factor)								# Calculates velocity if threshold met
		else:
			self.velocity = 0																				# No velocity if threshold is not met

	# Displays the tank
	def display(self):
		upper_x, upper_y = self.get_upper_left()
		image(self.pics[self.angle // 10], upper_x, upper_y, globals.default_tank_width, globals.default_tank_height, 150*(2 - self.player), 0, 150*(self.player - 1), 178)

	# Manipulates the tank based on the current phase of the game
	def tank_action(self):
		if self.moving_phase:
			self.move()
		elif self.angle_phase:
			self.animate_angle()
		elif self.velocity_phase:
			self.fiducial_marker()
		return self.bullet_phase			# returns True only if the player shoots bullet with certain velocity
