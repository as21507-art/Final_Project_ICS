import os
import globals

class Intro:

	def __init__(self, player):
		self.play = Play(int(globals.full_screenX * 0.5), int(globals.full_screenY * globals.play_position), globals.play_button)																		# Play button
		self.tutorial = Tutorial(globals.full_screenX // 2 - globals.tutorial_button[0] // 2 - globals.button_spacing, int(globals.full_screenY * globals.other_position), globals.tutorial_button)		# Tutorial button
		self.mute = Mute(globals.full_screenX // 2 + globals.button_spacing, int(globals.full_screenY * globals.other_position), globals.mute_button, player)											# Mute button
		self.quit = Quit(globals.full_screenX // 2 + globals.mute_button[0] + globals.button_spacing * 3, int(globals.full_screenY * globals.other_position), globals.quit_button)							# Quit button
		self.logo = loadImage(os.getcwd() + r"\\images\platform.png")

	# Displays the logo of the game
	def display_logo(self):
		rect(int(globals.full_screenX * 0.5 - globals.logo_width //2), int(globals.full_screenY * 0.3 - globals.logo_height //2), globals.logo_width, globals.logo_height)

	# Displays all the logos and button
	def display(self):
		self.display_logo()
		self.play.display()
		self.tutorial.display()
		self.mute.display()
		self.quit.display()
		if self.tutorial.pop_up_open:
			self.tutorial.display_pop()
		if self.quit.pop_up_open:
			self.quit.display_pop()

	# Handles mouse_clicks
	def handle_mouse(self):
		if self.quit.pop_up_open:			# if Quit pop up is open then only enable features within the pop-up
			self.quit.mouse_click()
		elif self.tutorial.pop_up_open:		# if Tutorial pop up is open then only enable features withint the pop-up
			self.tutorial.mouse_click()
		else:								# otherwise enable the features of all buttons
			self.play.mouse_click()
			self.tutorial.mouse_click()
			self.mute.mouse_click()
			self.quit.mouse_click()


class Button:

	def __init__(self, x, y, dim):
		self.x = x 					# x coordinate of the center
		self.y = y  				# y coordinate of the center
		self.w = dim[0] 			# width of the button
		self.h = dim[1] 			# height of the button

	# Gets upper left corner to print the rectangle using dimensions and centre coordinates
	def get_upper_left(self):
		return self.x - self.w //2, self.y - self.h //2

	# displays the button (rectangle and text)
	def display(self):
		upper_x, upper_y = self.get_upper_left()
		rect(upper_x, upper_y, self.w, self.h)

	# Checks if the mouse has been clicked within the boundary of the button and returns true if it has
	def mouse_click(self):
		upper_x, upper_y = self.get_upper_left()
		if upper_x < mouseX < upper_x + self.w and upper_y < mouseY < upper_y + self.h:
			return True
		return False


class Play(Button):

	def __init__(self, x, y, dim):
		Button.__init__(self, x, y, dim)
		self.start = False								# Flag to check if the player started the game

	def mouse_click(self):
		if Button.mouse_click(self):
			self.start = True							# Games starts on clicking play


class Tutorial(Button):
	def __init__(self, x, y, dim):
		Button.__init__(self, x, y, dim)
		# Dimensions and coordinates of the pop_up screen
		self.pop_x = int(globals.full_screenX * 0.25)		# Upper_left X
		self.pop_y = int(globals.full_screenY * 0.2)		# Upper_left Y
		self.pop_w = int(globals.full_screenX * 0.5)
		self.pop_h = int(globals.full_screenY * 0.65)
		self.pop_up_open = False							# Checks if the pop up is open, mouse behaves differently if it is
		self.prev = Button(int(self.pop_x + self.pop_w * 0.1 + globals.quit_button[0] // 2), int(self.pop_y + self.pop_h * 0.9 - globals.quit_button[1] // 2), globals.quit_button)	# Yes button
		self.next = Button(int(self.pop_x + self.pop_w * 0.9 - globals.quit_button[0] // 2), int(self.pop_y + self.pop_h * 0.9 - globals.quit_button[1] // 2), globals.quit_button) 	# No button
		self.cancel = Button(int(self.pop_x + self.pop_w - globals.mute_button[0] // 2), int(self.pop_y + globals.mute_button[1] // 2), globals.mute_button)

	# Displays a pop_up screen, disabling other buttons
	def display_pop(self):
		rect(self.pop_x, self.pop_y, self.pop_w, self.pop_h)
		self.prev.display()
		self.next.display()
		self.cancel.display()

	# Pop up is displayed on clicking the tutorial button
	def mouse_click(self):
		if not self.pop_up_open:
			if Button.mouse_click(self):
				self.pop_up_open = True
		else:
			if self.prev.mouse_click():					# Goes to previous slide
				print("Previous slide")
			elif self.next.mouse_click():				# Goes to next slide
				print("Next slide")
			elif self.cancel.mouse_click():				# Closes the pop_up
				self.pop_up_open = False


class Mute(Button):
	def __init__(self, x, y, dim, player):
		Button.__init__(self, x, y, dim)
		self.bgMusic = player.loadFile(os.getcwd() + r"\\sounds\background.mp3")
		self.bgMusic.loop()
		self.is_mute = False							# Flag which makes the mute button act as unmute button depending on its value

	# Music is paused and unpaused on clicking the mute button
	def mouse_click(self):
		if Button.mouse_click(self):
			if not self.is_mute:
				self.bgMusic.mute()
				self.is_mute = True
			else:
				self.bgMusic.unmute()
				self.is_mute = False

	# Displaying the cross when the sound is muted
	def display(self):
		Button.display(self)
		if self.is_mute:								# displays a diagonal line indicating a cross if the sound is muted
			upper_x, upper_y = self.get_upper_left()
			upper_x = int(upper_x + 0.15 * self.w)
			upper_y = int(upper_y + 0.15 * self.h)
			lower_x = int(upper_x + 0.7 * self.w)
			lower_y = int(upper_y + 0.7 * self.h)
			stroke(255, 0, 0)							# Red cross to denote mute
			line(upper_x, upper_y, lower_x, lower_y)
			stroke(0)									# Resets the colour for other processes


class Quit(Button):
	def __init__(self, x, y, dim):
		Button.__init__(self, x, y, dim)
		# Dimensions and coordinates of the pop_up screen
		self.pop_x = int(globals.full_screenX * 0.25)		# Upper_left X
		self.pop_y = int(globals.full_screenY * 0.3)		# Upper_left Y
		self.pop_w = int(globals.full_screenX * 0.5)
		self.pop_h = int(globals.full_screenY * 0.45)
		self.pop_up_open = False
		self.yes = Button(int(self.pop_x + self.pop_w * 0.1 + globals.quit_button[0] // 2), int(self.pop_y + self.pop_h * 0.9 - globals.quit_button[1] // 2), globals.quit_button)	# Yes button								# Yes button
		self.no = Button(int(self.pop_x + self.pop_w * 0.9 - globals.quit_button[0] // 2), int(self.pop_y + self.pop_h * 0.9 - globals.quit_button[1] // 2), globals.quit_button) 	# No button

	# Displays a pop_up screen, disabling other buttons
	def display_pop(self):
		rect(self.pop_x, self.pop_y, self.pop_w, self.pop_h)
		self.yes.display()
		self.no.display()

	def mouse_click(self):
		if not self.pop_up_open:
			if Button.mouse_click(self):
				self.pop_up_open = True
		else:
			if self.yes.mouse_click():
				exit()
			elif self.no.mouse_click():
				self.pop_up_open = False
