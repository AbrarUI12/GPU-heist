from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import math, random, sys, time
PI = math.pi
ARENA_HALF = 25.0



def deg2rad(d): return d * (PI / 180.0)
def rad2deg(r): return r * (180.0 / PI)
def clamp(v, a, b): return max(a, min(b, v))
def angle_wrap_deg(x): return (x + 180.0) % 360.0 - 180.0

def forward_vec(angDeg):
    t = deg2rad(angDeg)
    return math.sin(t), math.cos(t)  


def draw_square():
    glBegin(GL_QUADS)
    glVertex3f(-0.5, -0.5, 0.0)
    glVertex3f( 0.5, -0.5, 0.0)
    glVertex3f( 0.5,  0.5, 0.0)
    glVertex3f(-0.5,  0.5, 0.0)
    glEnd()

def drawCuboid(w, h, d):
    glPushMatrix()
    glScalef(w, h, d)
    glutSolidCube(1.0)
    glPopMatrix()

def drawSphere(r):
    glutSolidSphere(r, 24, 16)

def drawCylinder(r, h):
    q = gluNewQuadric()
    gluCylinder(q, r, r, h, 16, 1)
    gluDeleteQuadric(q)


def insideWalls(x, z, margin=0.5):
    return (-ARENA_HALF + margin < x < ARENA_HALF - margin and
            -ARENA_HALF + margin < z < ARENA_HALF - margin)
