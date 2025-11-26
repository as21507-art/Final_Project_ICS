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
        main_game.game.key_press(key, keyCode)
    
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

    
    
