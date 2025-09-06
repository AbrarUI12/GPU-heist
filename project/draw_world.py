from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def drawGrid(half, step):
    glDisable(GL_LIGHTING)
    glColor3f(0.396, 0.263, 0.129)  # Brown ground
    glBegin(GL_QUADS)
    glVertex3f(-half, 0, -half)
    glVertex3f(half, 0, -half)
    glVertex3f(half, 0, half)
    glVertex3f(-half, 0, half)
    glEnd()

    # Grid lines
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    x = -half
    while x <= half + 1e-6:
        glVertex3f(x, 0.001, -half)
        glVertex3f(x, 0.001, half)
        x += step
    z = -half
    while z <= half + 1e-6:
        glVertex3f(-half, 0.001, z)
        glVertex3f(half, 0.001, z)
        z += step
    glEnd()
    glEnable(GL_LIGHTING)
