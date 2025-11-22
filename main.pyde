import bullet as blt
import health as hlt
import tank as tnk
import globals as gb

# my_bullet = blt.Bullet(100, 650, 50, 50, 30)            # Parameters(tank_x, tank_y, bullet_radius, velocity, angle)
# my_bar = hlt.Health(1)
# his_bar = hlt.Health(0)
# show = False

my_tank = tnk.Tank(1, 300, 20)

def setup():
    size(gb.full_screenX, gb.full_screenY)
    
def draw():
    
    # global show
    # frameRate(20)
    background(255)
    # if show:
    #     my_bullet.display()
    #     my_bar.display()
    #     his_bar.display()
    line(0, gb.ground_level, gb.full_screenX, gb.ground_level)
    my_tank.display()   
    my_tank.tank_action() 
    
def keyPressed():
    my_tank.key_press(key, keyCode)
    
def keyReleased():
    my_tank.key_release(key, keyCode)
    
def mouseClicked():
    my_tank.mouse_click(mouseX, mouseY)
    
    
