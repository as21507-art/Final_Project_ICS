add_library('minim')
import intro, globals, game, tank
player = Minim(this)

main_game = None

def setup():
    global main_game
    size(globals.full_screenX, globals.full_screenY)
    main_game = game.Cycle(player)                    # Game initalisation

def draw():
    global main_game
    main_game.display()
    
def keyPressed():
    global main_game
    if main_game.phase == 0:
        main_game.intro.name_edit()                    # Enables typing names of players
    if main_game.phase == 1:
        if key == 'p':
            main_game.game_paused = True               # Game can be paused only in gameplay phase
        else:
            main_game.game.key_press()                 # Enables interactivity with tanks
    if main_game.phase == 2:
        main_game.outro.key_press()                 
    
def keyReleased():
    global main_game
    if main_game.phase == 1:
        main_game.game.key_release()
        
def mousePressed():
    global main_game
    if main_game.phase == 1:
        main_game.game.mouse_press()
        
def mouseReleased():
    global main_game
    if main_game.phase == 1:
        main_game.game.mouse_release()
    
def mouseClicked():
    global main_game
    if main_game.phase == 0:
        main_game.intro.handle_mouse()
    if main_game.game_paused:
        main_game.pause.handle_mouse()
        
