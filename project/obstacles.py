# obstacles.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


# Example obstacles: position (x, y, z) and size (w, h, d)
obstacles = [
    {"pos": (5, 0.0, -5), "size": (1, 1.5, 1)},
    {"pos": (-3, 0.0, 3), "size": (2, 2.0, 1)},
    {"pos": (0, 0.0, 8), "size": (1.5, 1.0, 1.5)},
]

def drawCuboid(w, h, d):
    glPushMatrix()
    glScalef(w, h, d)
    glutSolidCube(1)
    glPopMatrix()

def drawObstacles():
    glColor3f(0.8, 0.1, 0.1)  # Red
    for obs in obstacles:
        x, y, z = obs["pos"]
        w, h, d = obs["size"]
        glPushMatrix()
        glTranslatef(x, y + h / 2, z)  # position on ground
        drawCuboid(w, h, d)
        glPopMatrix()

def checkCollision(x, y, z):
    """Return True if (x, y, z) collides with any obstacle."""
    for obs in obstacles:
        ox, oy, oz = obs["pos"]
        w, h, d = obs["size"]
        min_x, max_x = ox - w/2, ox + w/2
        min_y, max_y = oy, oy + h
        min_z, max_z = oz - d/2, oz + d/2
        if min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z:
            return True
    return False
