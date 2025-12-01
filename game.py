import intro, tank, globals, bullet, health
import random, os


# Background music for the game
class Music:

    def __init__(self, player):
        self.bgMusic = player.loadFile(os.getcwd() + r"\\sounds\background.mp3")
        self.bgMusic.loop()

    def toggle_music(self, is_mute):
        if not is_mute:
            self.bgMusic.mute()                 # if it was unmuted, it mutes
        else:
            self.bgMusic.unmute()              # if it was muted, it unmutes


# Class for the gameplay
class Game:

    def __init__(self):
        self.turn = random.randint(0, 1)													    # Current player turn
        self.player = [tank.Tank(1, globals.p1_start_x, 0), tank.Tank(2, globals.p2_start_x, 0)]	# Stores the list of players
        self.healths = [health.Health(1), health.Health(2)]
        self.shoot = False																			# Flag for if the player has shot the bullet
        self.air_time = False																		# Flag for when the player is controlling the tank
        self.bullet = bullet.Bullet(0, 0, 0, 0, 0, 0)	# Initialising the bullet
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
        self.healths[0].display()
        self.healths[1].display()

    # Checks if the player has shot the bullet or not
    def interact(self):
        self.shoot = self.player[self.turn].tank_action()

    # Initialises bullet for the player everytime it is shot
    def initialise_bullet(self):
        self.bullet = bullet.Bullet(self.turn + 1, self.player[self.turn].x, self.player[self.turn].y, globals.default_tank_radius, self.player[self.turn].velocity, self.player[self.turn].angle)

    # Shooting the bullet
    def shoot_bullet(self):
        self.bullet.display()
        if self.bullet.landed:
            afflicted_damage = self.bullet.get_damage(self.player[(self.turn + 1) % 2].x)               # Calculates the damage after the bullet has landed
            self.healths[(self.turn + 1) % 2].change_health(afflicted_damage)                           # Uses the damage to reduce opponent's health
            self.next_player = True                                                                     # Change turns
            self.air_time = False


    # Uses the key and mouse inputs to control the tank
    def key_press(self, input_key, input_key_code):
        self.player[self.turn].key_press(input_key, input_key_code)

    def key_release(self, input_key, input_key_code):
        self.player[self.turn].key_release(input_key, input_key_code)

    def mouse_press(self, centreX, centreY):
        self.player[self.turn].mouse_press(centreX, centreY)

    def mouse_release(self):
        self.player[self.turn].mouse_release()

    # Initialises parameters for next tank's turn
    def prepare_next_tank(self):
        self.change_turn()
        self.next_player = False                                    # Turn already switched
        self.player[self.turn].moving_phase = True					# Initialises the next tank from moving phase
        self.player[self.turn].velocity = 0							# Rests the bullet velocity for next turn

    # Returns the current player
    def get_current_player(self):
        return self.turn + 1

    # Running the game
    def run(self):
        self.display()                                              # Display the game
        if self.healths[(self.turn + 1) % 2].health <= 0.0:			# Check if the game has ended
            return False
        self.interact()                                             # User can manipulate the tank
        if self.next_player:										# If the turn needs to be changed, reset required parameters and switch the value of turn
            self.prepare_next_tank()
        else:
            if self.air_time:
                self.shoot_bullet()                                 # Display and update the bullet while it is still in the air
            if self.shoot:
                self.player[self.turn].bullet_phase = False			# All phases of the tank are now false
                self.air_time = True                                # The bullet is currently in air
                self.shoot = False                                  # Rests the flag for having just shot the bullet
                self.initialise_bullet()                            # Initialised the bullet for the current tank
        return True


class Pause:
    def __init__(self):
        self.x = int(globals.full_screenX * 0.25)
        self.y = int(globals.full_screenY * 0.2)
        self.w = int(globals.full_screenX * 0.5)
        self.h = int(globals.full_screenY * 0.6)
        self.play = False                                       # Flag for when the player decides to resume the game
        self.home = False                                       # Flag for when the player decides to exit the current session
        self.resume = intro.Button(int(self.x + self.w * 0.2), int(self.y + self.h * 0.8), globals.resume_button, "resume.png")
        self.mute = intro.Mute(int(self.x + self.w * 0.375), int(self.y + self.h * 0.8), globals.mute_button,"mute_2.png", True)
        self.tutorial = intro.Tutorial(int(self.x + self.w * 0.55), int(self.y + self.h * 0.8), globals.tutorial_button, "tutorial_2.png")
        self.bgImg = loadImage(os.getcwd() + r"\\images\pause.png")
        self.exit = intro.Button(int(self.x + self.w * 0.8), int(self.y + self.h * 0.8), globals.exit_button, "exit.png")

    # Displays pop up and all the buttons
    def display(self):
        image(self.bgImg, self.x, self.y, self.w, self.h, 0, 0, self.w, self.h)
        self.resume.display()
        self.mute.display()
        self.tutorial.display()
        self.exit.display()
        if self.tutorial.pop_up_open:
            self.tutorial.display_pop()

    def handle_mouse(self):
        if self.tutorial.pop_up_open:           # If Tutorial pop up is open then only enable features within the pop-up
            self.tutorial.mouse_click()
        else:                                   # Otherwise enable the features of all buttons
            self.tutorial.mouse_click()
            self.mute.mouse_click()
            if self.resume.mouse_click():
                self.play = True
            elif self.exit.mouse_click():
                self.home = True


class Outro:

    def __init__(self):
        self.end = False
        self.winner = 0

    def key_press(self, input_key):
        if input_key == 'c':
            self.end = True


class Cycle:

    def __init__(self, player):
        self.soundtrack = Music(player)                 # Initialises the music for the game
        self.intro = intro.Intro()
        self.game = Game()
        self.outro = Outro()
        self.phase = 0 									# Takes 0 (intro), 1 (game), 2 (outro)
        self.pause = Pause()                            # Class for the pop-up screen when the game is paused
        self.game_paused = False                        # Flag for when the user decides to pause the game

    def restart(self):
        self.intro.play.start = False
        self.phase = 0
        self.game = Game()

    def check_sound(self):
        if self.phase == 0:
            self.pause.mute.is_unmute = self.intro.mute.is_unmute           # Both mute buttons are in the same state
        elif self.phase == 1:
            self.intro.mute.is_unmute = self.pause.mute.is_unmute
        self.soundtrack.toggle_music(self.intro.mute.is_unmute)         # Mutes or unmutes the music depending on whether the button is clicked

    def display(self):
        # Intro phase
        self.check_sound()
        if self.phase == 0:
            if self.intro.play.start:
                print("Play clicked")
                self.phase = 1							# If the player clicked "Play" then go to game phase
            else:
                self.intro.display()					# Otherwise continue on display screen
        # Game phase
        elif self.phase == 1:
            if self.game_paused:
                self.game.display()
                self.pause.display()
                if self.pause.play:
                    self.game_paused = False
                    self.pause.play = False
                elif self.pause.home:
                    self.pause.home = False
                    self.game_paused = False
                    self.restart()
            elif not self.game.run():                     # If the game is still running then continue, else change to outro phase
                print('Hello world, game over')
                self.phase = 2
                self.outro.end = True
                self.outro.winner = self.game.get_current_player()          # The current player is the winner, as turns have not been changed
        # Outro phase
        elif self.phase == 2:
            print(self.outro.winner)
            if self.outro.end:
                self.restart()
