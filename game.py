import intro, tank, globals, bullet, bar
import random, os


# Background music for the game
class Music:

    def __init__(self, music_player):
        self.bgMusic = music_player.loadFile(os.getcwd() + r"\\sounds\background.mp3")
        self.bgMusic.loop()

    def toggle_music(self, is_mute):
        if not is_mute:
            self.bgMusic.mute()                 # if it was unmuted, it mutes
        else:
            self.bgMusic.unmute()              # if it was muted, it unmutes


# Class for the gameplay
class Game:

    def __init__(self, music_player):
        self.music_player = music_player
        self.turn = random.randint(0, 1)						            # Current player turn
        self.player = [tank.Tank(1, globals.p1_start_x, 0), tank.Tank(2, globals.p2_start_x, 0)]	# Stores the list of players
        self.healths = [bar.Health(1), bar.Health(2)]
        self.player_names = []
        self.shoot = False														# Flag for if the player has shot the bullet
        self.air_time = False													# Flag for when the player is controlling the tank
        self.bullet = None	                                                    # Initialising the bullet
        self.next_player = True													# Initialising the game
        self.bgImg = loadImage(os.getcwd() + r"\\images\gameplay.png")
        self.playerFont = createFont("PressStart2P-Regular.ttf", 20)
        self.announcement_font = createFont("PressStart2P-Regular.ttf", 70)
        self.announce = True                                                    # Flag to indicate if the player's turn should be announced, turned off when player interacts with the tank

    # Switches turn between players
    def change_turn(self):
        self.turn = (self.turn + 1) % 2

    # Displays the background image for the game phase
    def display_background(self):
        image(self.bgImg, 0, 0)

    # Displays the names of the players near the health bar
    def display_texts(self):
        textFont(self.playerFont)
        textAlign(CENTER)
        for i in range(2):
            fill(255 * (1 - i), 0, 255 * i)                                         # Colour switching
            text(self.player_names[i], self.healths[i].x, self.healths[i].y - 20)

    # Displays the overall structure of the game
    def display(self):
        self.display_background()
        self.display_texts()
        for i in range(2):
            self.player[i].display()
            self.healths[i].display()

    # Checks if the player has shot the bullet or not
    def interact(self):
        self.shoot = self.player[self.turn].tank_action()

    # Initialises bullet for the player everytime it is shot
    def initialise_bullet(self):
        self.bullet = bullet.Bullet(self.turn + 1, self.player[self.turn].x, self.player[self.turn].y, globals.default_tank_radius, self.player[self.turn].velocity, self.player[self.turn].angle, self.music_player)

    # Shooting the bullet
    def shoot_bullet(self):
        if self.bullet.landed:
            self.bullet.explosion()
            if self.bullet.explode_count == self.bullet.explosion_frames:                                   # Animates explosion until the frames are done
                afflicted_damage = self.bullet.get_damage(self.player[(self.turn + 1) % 2].x)               # Calculates the damage after the bullet has landed
                self.healths[(self.turn + 1) % 2].change_health(afflicted_damage)                           # Uses the damage to reduce opponent's health
                self.next_player = True                                                                     # Change turns
                self.air_time = False
        else:
            self.bullet.display()                                                                           # Continues displaying the bullet
            self.bullet.move()                                                                              # Continues updating the position of the bullet

    # Uses the key and mouse inputs to control the tank
    def key_press(self):
        self.announce = False
        self.player[self.turn].key_press()

    def key_release(self):
        self.player[self.turn].key_release()

    def mouse_press(self):
        self.announce = False
        self.player[self.turn].mouse_press()

    def mouse_release(self):
        self.player[self.turn].mouse_release()

    # Initialises parameters for next tank's turn
    def prepare_next_tank(self):
        self.change_turn()
        self.next_player = False                                    # Turn already switched
        self.player[self.turn].moving_phase = True					# Initialises the next tank from moving phase
        self.player[self.turn].velocity = 0							# Rests the bullet velocity for next turn
        self.announce = True                                        # Announce next player's turn

    # Announcement of whose turn it is
    def announce_tank(self):
        textFont(self.announcement_font)
        textAlign(CENTER)
        fill(255 * (1 - self.turn), 0, 255 * self.turn)
        text(self.player_names[self.turn] + r"'s Turn", globals.full_screenX // 2, int(globals.full_screenY * 0.2))

    # Returns the current player
    def get_other_player(self):
        return self.player_names[self.turn - 1]

    # Running the game
    def run(self):
        self.display()                                              # Display the game
        if int(self.healths[self.turn].health) == 0:		        # Check if the game has ended
            return False
        if self.announce:
            self.announce_tank()                                    # Checks if announcement of the turn has to be made
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
        self.h = int(globals.full_screenY * 0.65)
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
        self.end = False                                                        # Flag for when the player decides to go to main screen
        self.bgImg = loadImage(os.getcwd() + r"\\images\outro_background.png")
        self.winner_font = createFont("PressStart2P-Regular.ttf", 60)
        self.exit_font = createFont("PressStart2P-Regular.ttf", 15)
        self.victory_text = ""                                                  # Stores the text that displays the winner

    # Generates message declaring the winner
    def write_winner(self, winner_name):
        self.victory_text = winner_name + " Wins"

    # Outro screen closes when the user presses C
    def key_press(self):
        if key == 'c':
            self.end = True

    # Displays the outro screen with messages
    def display(self):
        image(self.bgImg, 0, 0)
        textAlign(CENTER)
        fill(06, 140, 20)
        textFont(self.winner_font)
        text(self.victory_text, globals.full_screenX // 2, int(globals.full_screenY * 0.25))
        fill(0, 0, 0)
        textFont(self.exit_font)
        text("Thank you for playing. Press C to continue....",  globals.full_screenX // 2, int(globals.full_screenY * 0.25 + 50))


class Cycle:

    def __init__(self, music_player):
        self.music_player = music_player                # Initialises background music
        self.soundtrack = Music(self.music_player)      # Initialises the music for the game
        self.intro = intro.Intro(["Player 1", "Player 2"])
        self.game = Game(self.music_player)
        self.outro = Outro()
        self.phase = 0 									# Takes 0 (intro), 1 (game), 2 (outro)
        self.pause = Pause()                            # Class for the pop-up screen when the game is paused
        self.game_paused = False                        # Flag for when the user decides to pause the game

    # Resets all the required parameters for the next game
    def restart(self):
        self.intro.play.start = False
        self.intro.names = self.game.player_names
        self.phase = 0
        self.game = Game(self.music_player)
        self.outro.end = False

    # Maintains sync between the two mute buttons (One at the intro and the other with the pause)
    def check_sound(self):
        if self.phase == 0:
            self.pause.mute.is_unmute = self.intro.mute.is_unmute           # Both mute buttons are in the same state
        elif self.phase == 1:
            self.intro.mute.is_unmute = self.pause.mute.is_unmute
        self.soundtrack.toggle_music(self.intro.mute.is_unmute)             # Mutes or unmutes the music depending on whether the button is clicked

    # Main structure of the game
    def display(self):
        # Intro phase
        self.check_sound()
        if self.phase == 0:
            if self.intro.play.start:
                self.phase = 1							        # If the player clicked "Play" then go to game phase
                self.game.player_names = self.intro.names       # Use the names entered by user on intro screen for game phase
            else:
                self.intro.display()					        # Otherwise continue on display screen
        # Game phase
        elif self.phase == 1:
            if self.game_paused:                               # If game is paused then display pause pop up overlapping the game background
                self.game.display()
                self.pause.display()
                if self.pause.play:                            # If the user resumes then set paused to false
                    self.game_paused = False
                    self.pause.play = False                    # Resets the value of play for next pause
                elif self.pause.home:                          # If user wants to go back to home screen
                    self.pause.home = False                    # Resets the value of home for next pause
                    self.game_paused = False
                    self.restart()                             # restarts the game from the intro screen
            elif not self.game.run():                          # If the game is still running then continue, else change to outro phase
                self.phase = 2
                self.outro.write_winner(self.game.get_other_player())           # The current player is the winner, as turns have not been changed
        # Outro phase
        elif self.phase == 2:
            self.outro.display()
            if self.outro.end:
                self.restart()                              # Reinitialize the game from the beginning
