from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, time
from helper_fun import *
from model import *
from classes import Player,player
import floors
# camera.py
import math

# Camera position
camX, camY, camZ = 0.0, 0.0, 0.0

def setupCamera():
    global camX, camY, camZ

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Camera settings
    follow_dist = 8.0   # distance behind player
    height_offset = 3.0 # height above player
    lerp_speed = 0.2    # smooth factor

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

    # Look at the player
    lookX = player.pos[0]
    lookY = player.pos[1] + 1.0
    lookZ = player.pos[2]

    gluLookAt(camX, camY, camZ, lookX, lookY, lookZ, 0, 1, 0)