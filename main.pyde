add_library('minim')
import intro, globals, game, tank
player = Minim(this)

main_game = game.Cycle(player)

def setup():
    size(globals.full_screenX, globals.full_screenY)
    
def draw():
    background(255)
    main_game.display()
    
def keyPressed():
    if main_game.phase == 1:
        if key == 'p':
            main_game.game_paused = True               # Game can be paused only in gameplay phase
        else:
            main_game.game.key_press(key, keyCode)
    if main_game.phase == 2:
        main_game.outro.key_press(key)
    
def keyReleased():
    if main_game.phase == 1:
        main_game.game.key_release(key, keyCode)
        
def mousePressed():
    if main_game.phase == 1:
        main_game.game.mouse_press(mouseX, mouseY)
        
def mouseReleased():
    if main_game.phase == 1:
        main_game.game.mouse_release()
    
def mouseClicked():
    if main_game.phase == 0:
        main_game.intro.handle_mouse()
    if main_game.game_paused:
        main_game.pause.handle_mouse()
