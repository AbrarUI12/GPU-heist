# spawn_ammocrate.py
# Single ammo crate that gives player 20 balls when collected

import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutSolidCube

WORLD_HALF = 100.0   # same as your world/grid size
CRATE_SIZE = 0.7    # visual cube size
AMMO_AMOUNT = 20    # balls gained from one crate

ammo_crate = None   # store single crate state


def spawn_ammo_crate():
    """Spawn exactly one ammo crate at a random location."""
    global ammo_crate
    x = random.uniform(-WORLD_HALF + CRATE_SIZE, WORLD_HALF - CRATE_SIZE)
    z = random.uniform(-WORLD_HALF + CRATE_SIZE, WORLD_HALF - CRATE_SIZE)   
    y = 15.8  

    ammo_crate = {"pos": [x, y, z], "collected": False}


def draw_ammo_crate():
    """Draw the ammo crate if not collected."""
    global ammo_crate
    if ammo_crate is None or ammo_crate["collected"]:
        return

    glDisable(GL_LIGHTING)
    glColor3f(0.0, 0.5, 1.0)  # blue crate
    glPushMatrix()
    glTranslatef(*ammo_crate["pos"])
    glutSolidCube(CRATE_SIZE)
    glPopMatrix()
    glEnable(GL_LIGHTING)


def check_crate_collection(player):
    """Check if player collects the ammo crate."""
    global ammo_crate
    if ammo_crate is None or ammo_crate["collected"]:
        return

    dx = player.pos[0] - ammo_crate["pos"][0]
    dy = player.pos[1] - ammo_crate["pos"][1]
    dz = player.pos[2] - ammo_crate["pos"][2]
    distance = (dx*dx + dy*dy + dz*dz)**0.5

    if distance < CRATE_SIZE + 0.6:  # pickup radius
        ammo_crate["collected"] = True
        player.balls += AMMO_AMOUNT


def update_ammocrate(dt):
        # Example: rotate slowly
        ammo_crate.angDeg += 20.0 * dt
        ammo_crate.angDeg %= 360