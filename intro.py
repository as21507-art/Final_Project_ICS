import os
import globals

class Intro:

	def __init__(self, player_names):
		# Initialising the buttons
		self.play = Play(int(globals.full_screenX * 0.5), int(globals.full_screenY * globals.play_position), globals.play_button, "play.png", "hover.png")																	
		self.tutorial = Tutorial(globals.full_screenX // 2 - globals.tutorial_button[0] // 2 - globals.mute_button[0] //2 - globals.button_spacing, int(globals.full_screenY * globals.other_position), globals.tutorial_button, "tutorial.png")
		self.mute = Mute(globals.full_screenX // 2, int(globals.full_screenY * globals.other_position), globals.mute_button,"mute.png", True)
		self.quit = Quit(globals.full_screenX // 2 + globals.mute_button[0] //2 + globals.button_spacing + globals.quit_button[0] //2, int(globals.full_screenY * globals.other_position), globals.quit_button, "quit.png")	
		self.logo = loadImage(os.getcwd() + r"\\images\logo.png")
		self.bgImg = loadImage(os.getcwd() + r"\\images\intro_background.png")
		# Attributes to allow changing names of players in intro screen
		self.names = player_names
		self.intro_font = createFont("PressStart2P-Regular.ttf", 15)
		self.names_spaceX = [700, 1000]
		self.names_spaceY = 0.8
		self.name_spaceW = 200
		self.name_spaceH = 60
		self.edit_name = -1													# -1 if nothing is highlighted, 0 and 1 if the user wants to change names of players
		self.vs = loadImage(os.getcwd() + r"\\images\vs.png")

	# Displays the background for intro screen
	def display_background(self):
		image(self.bgImg, 0, 0)

	# Upper_left corner for the boxes where the players can enter their names (Name Box)
	def upper_left(self, i, x):								# Returns upper X if x = true, returns upper y if x = False
		if x:
			return self.names_spaceX[i] - self.name_spaceW // 2
		else:
			return int(globals.full_screenY * self.names_spaceY) - self.name_spaceH // 2

	# Displays Name Box for both players
	def display_names(self):
		stroke(255)
		strokeWeight(1)
		textAlign(CENTER, CENTER)
		textFont(self.intro_font)
		image(self.vs, globals.full_screenX // 2 - 25, int(globals.full_screenY * self.names_spaceY) - 50)
		for i in range(2):
			fill(0)
			rect(self.upper_left(i, True), self.upper_left(i, False), self.name_spaceW, self.name_spaceH)	# Displays the box
			if self.edit_name == i:
				fill(255)																						# If highlighted
			else:
				fill(155)																						# Not highlighted
			text(self.names[i] + "_", self.names_spaceX[i], int(globals.full_screenY * self.names_spaceY))		# Displays the text


	# Editing the name
	def name_edit(self):
		if self.edit_name != -1:
			if key == BACKSPACE and len(self.names[self.edit_name]) > 0:						# Deleting if backspace is pressed
				self.names[self.edit_name] = self.names[self.edit_name][:-1]
			elif key != BACKSPACE and len(self.names[self.edit_name]) < 12:						# Adding characters if the key is not backspace
				try:
					self.names[self.edit_name] = self.names[self.edit_name] + key
				except TypeError:																# Handles error if the key can not be added to the string
					return

	# Check if the user clicked on Name Box
	def check_name_box(self):
		for i in range(2):
			if self.upper_left(i, True) < mouseX < self.upper_left(i, True) + self.name_spaceW and self.upper_left(i, False) < mouseY < self.upper_left(i, False) + self.name_spaceH:
				self.edit_name = i
				break

	# Displays the logo of the game
	def display_logo(self):
		image(self.logo, (globals.full_screenX * 0.5 - globals.logo_width //2), int(globals.full_screenY * 0.3 - globals.logo_height //2))

	# Displays all the logos and button
	def display(self):
		self.display_background()
		self.display_logo()
		self.play.display()
		self.tutorial.display()
		self.mute.display()
		self.quit.display()
		self.display_names()
		# Pop ups are displayed only if they are activated by the user
		if self.tutorial.pop_up_open:
			self.tutorial.display_pop()
		if self.quit.pop_up_open:
			self.quit.display_pop()

	# Handles mouse_clicks
	def handle_mouse(self):
		self.edit_name = -1 				# Do not highlight the name box if the user clicks off the box
		if self.quit.pop_up_open:			# if Quit pop up is open then only enable features within the pop-up
			self.quit.mouse_click()
		elif self.tutorial.pop_up_open:		# if Tutorial pop up is open then only enable features within the pop-up
			self.tutorial.mouse_click()
		else:								# otherwise enable the features of all buttons
			self.play.mouse_click()
			self.tutorial.mouse_click()
			self.mute.mouse_click()
			self.quit.mouse_click()
			self.check_name_box()


class Button:

	def __init__(self, x, y, dim, name):
		self.x = x 					# x coordinate of the center
		self.y = y  				# y coordinate of the center
		self.w = dim[0] 			# width of the button
		self.h = dim[1] 			# height of the button
		self.image = loadImage(os.getcwd() + r"\\images" + "\\" + name)		# stores the image of the button

	# Gets upper left corner to print the rectangle using dimensions and centre coordinates
	def get_upper_left(self):
		return self.x - self.w //2, self.y - self.h //2

	# Displays the button image 
	def display(self):
		upper_x, upper_y = self.get_upper_left()
		image(self.image, upper_x, upper_y)

	# Checks if the mouse has been clicked within the boundary of the button and returns true if it has
	def mouse_click(self):
		upper_x, upper_y = self.get_upper_left()
		if upper_x < mouseX < upper_x + self.w and upper_y < mouseY < upper_y + self.h:
			return True
		return False


class PopUp:

	def __init__(self, x, y, w, h, img_name):
		self.x = x		# Upper_left X
		self.y = y		# Upper_left Y
		self.w = w
		self.h = h
		self.bgimg = loadImage(os.getcwd() + r"\\images" + "\\" + img_name)

	def display(self):
		image(self.bgimg, self.x, self.y, self.w, self.h, 0, 0, self.w, self.h)


class Play(Button):

	def __init__(self, x, y, dim, name, hover):
		Button.__init__(self, x, y, dim, name)
		self.start = False								# Flag to check if the player started the game
		self.hover_image = loadImage(os.getcwd() + r"\\images" + "\\" + hover)

	def mouse_click(self):
		if Button.mouse_click(self):
			self.start = True							# Games starts on clicking play

	# Returns true if the mouse is within the bounds of the button (hovering over the button)
	def hover(self):
		upper_x, upper_y = self.get_upper_left()
		if upper_x < mouseX < upper_x + self.w and upper_y < mouseY < upper_y + self.h:
			return True
		return False

	def display(self): 										# Polymorphism to implement the hover effect
		if not self.hover():
			Button.display(self)
		else:												# Display a different image when the user is hovering
			upper_x, upper_y = self.get_upper_left()
			image(self.hover_image, upper_x, upper_y)


class Tutorial(Button):
	def __init__(self, x, y, dim, name):
		Button.__init__(self, x, y, dim, name)
		# Dimensions and coordinates of the pop_up screen
		self.pop_up = []
		for i in range(1, 7):
			self.pop_up.append(PopUp(int(globals.full_screenX * 0.25), int(globals.full_screenY * 0.2), int(globals.full_screenX * 0.5), int(globals.full_screenY * 0.65), str(i) + ".png"))
		self.pop_up_open = False												# Checks if the pop-up is open, mouse behaves differently if it is
		self.slide = 0															# Stores the current slide of tutorial displayed on the screen
		self.prev = Button(int(self.pop_up[0].x + self.pop_up[0].w * 0.1 + globals.quit_button[0] // 2), int(self.pop_up[0].y + self.pop_up[0].h * 0.9 - globals.tutorial_button[1] // 2), globals.tutorial_button, "prev.png")
		self.next = Button(int(self.pop_up[0].x + self.pop_up[0].w * 0.9 - globals.quit_button[0] // 2), int(self.pop_up[0].y + self.pop_up[0].h * 0.9 - globals.tutorial_button[1] // 2), globals.tutorial_button, "next.png")
		self.cancel = Button(int(self.pop_up[0].x + self.pop_up[0].w - globals.mute_button[0] // 2), int(self.pop_up[0].y + globals.cancel_button[1] // 2), globals.cancel_button, "cancel.png")

	# Displays a pop_up screen, disabling other buttons
	def display_pop(self):
		self.pop_up[self.slide].display()				# Displays the current slide of pop_up
		# Buttons within the pop-up screen that can be accessed
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
				if self.slide > 0:
					self.slide -= 1
			elif self.next.mouse_click():				# Goes to next slide
				if self.slide < 5:
					self.slide += 1
			elif self.cancel.mouse_click():				# Closes the pop_up
				self.pop_up_open = False


class Mute(Button):
	def __init__(self, x, y, dim, name, is_unmute):
		Button.__init__(self, x, y, dim, name)
		self.is_unmute = is_unmute							# Flag which makes the mute button act as unmute button depending on its value

	# Music is mutes or unmuted on clicking the mute button
	def mouse_click(self):
		if Button.mouse_click(self):
			if self.is_unmute:
				self.is_unmute = False
			else:
				self.is_unmute = True

	# Displaying the cross when the sound is muted
	def display(self):
		Button.display(self)
		if not self.is_unmute:								# displays a diagonal line indicating a cross if the sound is muted
			upper_x, upper_y = self.get_upper_left()
			upper_x = int(upper_x + 0.2 * self.w)
			upper_y = int(upper_y + 0.2 * self.h)
			lower_x = int(upper_x + 0.6 * self.w)
			lower_y = int(upper_y + 0.6 * self.h)
			stroke(255, 0, 0)							# Red cross to denote mute
			strokeWeight(4)
			line(upper_x, upper_y, lower_x, lower_y)
			stroke(0)									# Resets the colour for other processes


class Quit(Button):
	def __init__(self, x, y, dim, name):
		Button.__init__(self, x, y, dim, name)
		# Dimensions and coordinates of the pop_up screen
		self.pop_up = PopUp(int(globals.full_screenX * 0.25), int(globals.full_screenY * 0.2), int(globals.full_screenX * 0.5), int(globals.full_screenY * 0.45), "quit pop.png")
		self.pop_up_open = False
		self.yes = Button(int(self.pop_up.x + self.pop_up.w * 0.1 + globals.quit_button[0] // 2), int(self.pop_up.y + self.pop_up.h * 0.9 - globals.quit_button[1] // 2), globals.quit_button, "yes.png")	# Yes button								# Yes button
		self.no = Button(int(self.pop_up.x + self.pop_up.w * 0.9 - globals.quit_button[0] // 2), int(self.pop_up.y + self.pop_up.h * 0.9 - globals.quit_button[1] // 2), globals.quit_button, "no.png") 	# No button

	# Displays a pop_up screen, disabling other buttons
	def display_pop(self):
		self.pop_up.display()
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
