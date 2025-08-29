from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, time
from helper_fun import *
from model import *
from classes import Player,player
from camera import setupCamera
from draw_world import *
from player_movement import *

# Window and world settings
WIN_W, WIN_H = 1024, 720
ARENA_HALF = 100
GRID_STEP = 5.0
CAMERA_DIST = 10.0
PLAYER_Y = 0.75
MOVE_SPEED = 4.0

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



def draw_menu():
    # --- Draw background and initial text in 2D ---
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Background
    glColor3f(0.1, 0.1, 0.15)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(WIN_W, 0)
    glVertex2f(WIN_W, WIN_H)
    glVertex2f(0, WIN_H)
    glEnd()

    # Main menu text
    glColor3f(1.0, 1.0, 1.0)
    def draw_text(x, y, text):
        glRasterPos2f(x, y)
        for c in text.encode("utf-8"):
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c)

    draw_text(WIN_W*0.35, WIN_H*0.8, "Select Your Character:")
    draw_text(WIN_W*0.35, WIN_H*0.2, "Press 1 for Abrar\n 2 for Sanjoy\n 3 for Ishrak")

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    # --- Draw 3D character models ---
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    # Abrar
    glPushMatrix()
    glTranslatef(-2.0, -1.5, -8.0)
    glRotatef(30, 0, 1, 0)
    Abrar_model()
    glPopMatrix()

    # Sanjoy
    glPushMatrix()
    glTranslatef(0.0, -1.5, -8.0)
    glRotatef(-30, 0, 1, 0)
    Sanjoy_model()
    glPopMatrix()
    
    #ishrak
    glPushMatrix()
    glTranslatef(2.0,-1.5, -8.0)
    glRotatef(-30, 0, 1, 0)
    Ishrak_model()
    glPopMatrix()

    # --- Draw labels for models in 2D again ---
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw model names
    glColor3f(1.0, 1.0, 1.0)
    draw_text(WIN_W*0.35, WIN_H*0.75, "Abrar")
    draw_text(WIN_W*0.65, WIN_H*0.75, "Ishrak")
    draw_text(WIN_W*0.50, WIN_H*0.75, "Sanjoy")
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)



# Display
def on_display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if game_state == MENU:
       pass
       draw_menu()
    elif game_state == PLAYING:
        setupCamera()
        drawGrid(ARENA_HALF, GRID_STEP)
        glPushMatrix()
        glTranslatef(player.pos[0], player.pos[1], player.pos[2])
        glRotatef(player.angDeg, 0, 1, 0)
        if selected_model == "Abrar":
            Abrar_model(player.lying)
        elif selected_model == "Sanjoy":
            Sanjoy_model(player.lying)
        elif selected_model == "Ishrak":
            Ishrak_model(player.lying)
        glPopMatrix()
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

# Keyboard movement
last_time = time.time()
def on_keyboard(key, x, y):
    global last_time,selected_model,game_state
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    
    if game_state == MENU:
        if key == b'1':
            selected_model = "Abrar"
            game_state = PLAYING
        elif key == b'2':
            selected_model = "Sanjoy"
            game_state = PLAYING
        elif key == b'3':
            selected_model = "Ishrak"
            game_state = PLAYING
        glutPostRedisplay()
        return


    key = key.decode('utf-8')
    if key == 'w':  # Forward
        movePlayer(1, dt)
    elif key == 's':  # Backward
        movePlayer(-1, dt)
    elif key == 'd':  # Strafe right
        strafePlayer(-1, dt)
    elif key == 'a':  # Strafe left
        strafePlayer(1, dt)

    glutPostRedisplay()

####mouse movemnt
# Track last mouse position
lastMouseX = None
sensitivity = 0.3  # adjust for faster/slower rotation

def on_mouse_motion(x, y):
    global lastMouseX
    if lastMouseX is None:
        lastMouseX = x
        return

    # Invert deltaX to correct rotation direction
    deltaX = lastMouseX - x  # <-- inversion here
    player.angDeg += deltaX * sensitivity
    player.angDeg %= 360  # wrap angle between 0–360

    lastMouseX = x
    glutPostRedisplay()




def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIN_W, WIN_H)
    glutCreateWindow(b"Simple WASD Movement Example")
    init_gl()
    glutDisplayFunc(on_display)
    glutReshapeFunc(on_reshape)
    glutKeyboardFunc(on_keyboard)
    glutPassiveMotionFunc(on_mouse_motion)
    glutMainLoop()
if __name__ == "__main__":
    main()
