import intro, tank, globals, bullet, health
import random

class Game:

	def __init__(self):
		self.turn = random.randint(0, 1)															# Current player turn
		self.player = [tank.Tank(1, globals.p1_start_x, 0), tank.Tank(2, globals.p2_start_x, 0)]	# Stores the list of players
		self.healths = [health.Health(1), health.Health(2)]
		self.shoot = False																			# Flag for if the player has shot the bullet
		self.shooting = False																		# Flag for when the player is controlling the tank
		self.bullet = bullet.Bullet(0, 0, 0, 0, 0, 0)												# Initialising the bullet
		self.next_player = True																		# Initialising the game

	# Switches turn between players
	def change_turn(self):
		self.turn = (self.turn + 1) % 2

	# Displays the background image for the game phase
	def display_background(self):
		stroke(0, 255, 0)
		line(0, globals.ground_level, globals.full_screenX, globals.ground_level)

	# Displays the overall structure of the game
	def display(self):
		self.display_background()
		self.player[0].display()
		self.player[1].display()
		self.shoot = self.player[self.turn].tank_action()

	# Initialises bullet everytime it is shot
	def initialise_bullet(self):
		self.bullet = bullet.Bullet(self.turn + 1, self.player[self.turn].x, self.player[self.turn].y, globals.default_tank_radius, self.player[self.turn].velocity, self.player[self.turn].angle)
	
	# Shooting the bullet
	def shoot_bullet(self):
		self.bullet.display()
		if self.bullet.landed:
			afflicted_damage = self.bullet.get_damage(self.player[(self.turn + 1) % 2].x)
			self.healths[(self.turn + 1) % 2].health -= afflicted_damage
			print('Landed', self.healths[(self.turn + 1) % 2].health)
			self.next_player = True

	# Uses the key and mouse inputs to control the tank
	def key_press(self, input_key, input_key_code):
	    self.player[self.turn].key_press(input_key, input_key_code)
	    
	def key_release(self, input_key, input_key_code):
		self.player[self.turn].key_release(input_key, input_key_code)

	def mouse_press(self, centreX, centreY):
		self.player[self.turn].mouse_press(centreX, centreY)

	def mouse_release(self):
		self.player[self.turn].mouse_release()

	# Initalises parameters for next tank's turn
	def prepare_next_tank(self):
		self.shooting = False
		self.shoot = False
		self.next_player = False
		self.change_turn()
		self.player[self.turn].moving_phase = True					# Initalises the next tank from moving phase

	# Running the game
	def run(self):
		self.display()
		if self.healths[(self.turn + 1) % 2].health <= 0.0:			# Check if the game has ended
			print((self.turn + 1) % 2 + 1)
			return (self.turn + 1) % 2 + 1
		if self.next_player:										# If the turn needs to be changed, reset everything and switch the value of turn
			self.prepare_next_tank()				
		else:
			if self.shooting:
				self.shoot_bullet()
			if self.shoot:
				self.player[self.turn].bullet_phase = False			# All phases of the tank are now false
				self.shooting = True
				self.shoot = False	
				self.initialise_bullet()
		return 0
		


class Cycle:

	def __init__(self, player):
		self.intro = intro.Intro(player)
		self.phase = 0 									# Takes 0 (intro), 1 (game), 2 (outro)
		self.game = Game()

	def display(self):
		# Intro phase
		if self.phase == 0:					
			if self.intro.play.start:		
				self.phase = 1							# if the player clicked "Play" then go to game phase
				self.intro.play.start = False			# rests the play button for the next time user are on intro page
			else:
				self.intro.display()					# otherwise continue on display screen
		# Game phase
		elif self.phase == 1:
			if self.game.run() != 0:
				print('Hello world, game over')
				self.phase = 2
		# Outro phase
		elif self.phase == 2:
			self.game = Game()							# initalises the game for next session
