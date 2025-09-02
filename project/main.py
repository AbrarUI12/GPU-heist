from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, time
from helper_fun import *
from model import *
from classes import Player, player
from camera import setupCamera
from draw_world import *
from player_movement import *
from jump import start_jump, update_jump
from obstacles import drawObstacles
import crouch
from jump import start_jump
import balls
import hud
import enemy
import throw_ball



# ---------------- Window / world settings ----------------
WIN_W, WIN_H = 1024, 720
GRID_STEP = 5.0
CAMERA_DIST = 10.0
PLAYER_Y = 0.75

# Camera settings
firstPerson = False
camYawDeg = 30.0
camPitchDeg = 20.0
camDist = CAMERA_DIST
PI = math.pi

# Game states
MENU = 0
PLAYING = 1
game_state = MENU

# Selected model
selected_model = None

# ---------------- Input ----------------
pressed_keys = {}  # key -> True if pressed

lastMouseX = None
sensitivity = 0.3


enemy.spawn_enemy()
# ---------------- Menu / display ----------------
def draw_menu():
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(0.1, 0.1, 0.15)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(WIN_W, 0)
    glVertex2f(WIN_W, WIN_H)
    glVertex2f(0, WIN_H)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)
    def draw_text(x, y, text):
        glRasterPos2f(x, y)
        for c in text.encode("utf-8"):
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c)

    draw_text(WIN_W*0.35, WIN_H*0.8, "Select Your Character:")
    draw_text(WIN_W*0.35, WIN_H*0.2, "Press 1 for Abrar | 2 for Sanjoy | 3 for Ishrak")

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    # Draw 3D models
    glPushMatrix()
    glTranslatef(-2.0, -1.5, -8.0)
    glRotatef(30, 0, 1, 0)
    Abrar_model()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, -1.5, -8.0)
    glRotatef(-30, 0, 1, 0)
    Sanjoy_model()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(2.0,-1.5, -8.0)
    glRotatef(-30, 0, 1, 0)
    Ishrak_model()
    glPopMatrix()

# ---------------- Display / reshape ----------------
def on_display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        setupCamera()
        drawGrid(ARENA_HALF, GRID_STEP)
        drawObstacles()  
        balls.draw_balls() 
        throw_ball.draw_balls()
        enemy.draw_enemies()
        glPushMatrix()
        glTranslatef(player.pos[0], player.pos[1], player.pos[2])
        glRotatef(player.angDeg, 0, 1, 0)
        glScalef(player.scale, player.scale, player.scale)  # apply crouch/stand scale
        if selected_model == "Abrar":
            Abrar_model(player.lying)
        elif selected_model == "Sanjoy":
            Sanjoy_model(player.lying)
        elif selected_model == "Ishrak":
            Ishrak_model(player.lying)
        glPopMatrix()
        hud.draw_hud(player, player.health,selected_model)
    glutSwapBuffers()

def on_reshape(w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, w / float(h), 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW)

def init_gl():
    glClearColor(0.09, 0.09, 0.11, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (5.0, 8.0, 10.0, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.9, 0.9, 0.9, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

# ---------------- Keyboard ----------------
def on_keyboard(key, x, y):
    global selected_model, game_state
    # Menu selection
    if game_state == MENU:
        if key == b'1':
            selected_model = "Abrar"
            player.balls = 2
            player.health = 10
            game_state = PLAYING
        elif key == b'2':
            selected_model = "Sanjoy"
            player.balls = 6
            player.health = 10
            game_state = PLAYING
        elif key == b'3':
            selected_model = "Ishrak"
            player.balls = 2
            player.health = 20
            game_state = PLAYING
        glutPostRedisplay()
        return

    # Add key to pressed_keys
    try:
        ch = key.decode('utf-8').lower()
    except:
        return
    pressed_keys[ch] = True
    
    # Jump on spacebar
    # Jump on spacebar
    if ch == ' ' and not crouch.is_crouching:   # 🚫 cannot jump while crouching
       start_jump()

    # Crouch with "c"
    if ch == 'c':
        crouch.toggle_crouch(player)

    
    
def on_keyboard_up(key, x, y):
    try:
        ch = key.decode('utf-8').lower()
    except:
        return

    pressed_keys[ch] = False



# ---------------- Mouse ----------------
def on_mouse_motion(x, y):
    global lastMouseX
    if lastMouseX is None:
        lastMouseX = x
        return
    deltaX = lastMouseX - x
    player.angDeg += deltaX * sensitivity
    player.angDeg %= 360
    lastMouseX = x
    glutPostRedisplay()

def on_mouse_click(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        import throw_ball
        throw_ball.throw_ball()




# ---------------- Update (per-frame) ----------------
def update():
    if game_state != PLAYING:
        return

    speed = 8.0 if selected_model == "Abrar" else 4.0
    
    dt = 0.016  # fixed timestep ~60FPS

    if pressed_keys.get('w', False):
        movePlayer(1, dt, speed)
    if pressed_keys.get('s', False):
        movePlayer(-1, dt, speed)
    if pressed_keys.get('a', False):
        strafePlayer(1, dt, speed)
    if pressed_keys.get('d', False):
        strafePlayer(-1, dt, speed)

    # Update jump
    update_jump(player, dt)
    
    
    balls.check_collection(player)
    # player.health = max(player.health - 1, 0)  # example damage

    enemy.update_enemies(0.016)
    throw_ball.update_balls(dt)

    glutPostRedisplay()


# ---------------- Main ----------------
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIN_W, WIN_H)
    glutCreateWindow(b"Simple WASD Movement Example")
    init_gl()
    balls.spawn_balls()
    glutDisplayFunc(on_display)
    glutReshapeFunc(on_reshape)
    glutKeyboardFunc(on_keyboard)
    glutKeyboardUpFunc(on_keyboard_up)
    glutPassiveMotionFunc(on_mouse_motion)
    glutIdleFunc(update)# continuous update
    glutMouseFunc(on_mouse_click) 
    glutMainLoop()

if __name__ == "__main__":
    main()
