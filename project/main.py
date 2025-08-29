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
ARENA_HALF = 25.0
GRID_STEP = 1.0
CAMERA_DIST = 10.0
PLAYER_Y = 0.75
MOVE_SPEED = 4.0

# Camera settings
firstPerson = False
camYawDeg = 30.0
camPitchDeg = 20.0
camDist = CAMERA_DIST
PI = math.pi



# Display
def on_display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setupCamera()
    drawGrid(ARENA_HALF, GRID_STEP)
    glPushMatrix()
    glTranslatef(player.pos[0], player.pos[1], player.pos[2])
    glRotatef(player.angDeg, 0, 1, 0)
    Sanjoy_model(player.lying)
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
    global last_time
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

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
