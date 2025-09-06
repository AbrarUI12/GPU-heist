from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, time
from helper_fun import *
from model import *
from classes import Player, player
import floors

# Camera position
camX, camY, camZ = 0.0, 0.0, 0.0

def setupCamera():
    global camX, camY, camZ

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Camera settings
    follow_dist = 7   # distance behind player
    height_offset = 6 # height above player
    lerp_speed = 0.2     # smooth factor
    side_offset = 0.5    # <-- new: shift camera look slightly to left

    # Calculate target camera position behind player
    ang_rad = deg2rad(player.angDeg)
    targetX = player.pos[0] - follow_dist * math.sin(ang_rad)
    targetY = player.pos[1] + height_offset
    targetZ = player.pos[2] - follow_dist * math.cos(ang_rad)

    # Ensure camera doesn't go below current floor
    current_floor = floors.get_current_floor()
    floor_y = floors.get_floor_y_offset(current_floor)
    min_camera_y = floor_y + 2.0  # Minimum camera height above floor
    
    if targetY < min_camera_y:
        targetY = min_camera_y

    # Smooth camera movement
    camX += (targetX - camX) * lerp_speed
    camY += (targetY - camY) * lerp_speed
    camZ += (targetZ - camZ) * lerp_speed

    # --- Look at the player ---
    # Shift lookX to move player slightly left on screen
    lookX = player.pos[0] + side_offset
    lookY = player.pos[1] + 1.8
    lookZ = player.pos[2]

    gluLookAt(camX, camY, camZ, lookX, lookY, lookZ, 0, 1, 0)


def drawCrosshair():
    """Draws a simple crosshair in the center of the screen."""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)  # Assuming window size 800x600

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)  # So it always draws on top
    glColor3f(1.0, 1.0, 1.0)  # White crosshair
    glLineWidth(2.0)

    cx, cy = 400, 300  # center of screen
    size = 10          # crosshair half-size

    glBegin(GL_LINES)
    # Horizontal line
    glVertex2f(cx - size, cy)
    glVertex2f(cx + size, cy)
    # Vertical line
    glVertex2f(cx, cy - size)
    glVertex2f(cx, cy + size)
    glEnd()

    glEnable(GL_DEPTH_TEST)

    # Restore matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
