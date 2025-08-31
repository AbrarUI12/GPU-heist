from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import math, random, sys, time
from helper_fun import *

PI = math.pi




def Abrar_model(lying=False):
    glPushMatrix()

    if lying:
        glRotatef(-90.0, 1, 0, 0)

    leg_length = 1.5
    body_height = 1.5
    body_y_offset = leg_length  # move body above legs

    # Body (main cube)
    glPushMatrix()
    glTranslatef(0.0, body_y_offset, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(1.0, body_height, 0.6)  
    glPopMatrix()
   
    # Right arm
    glPushMatrix()
    glTranslatef(.65, body_y_offset + 0.2, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(0.3, 0.9, 0.3) 
    glPopMatrix()  

    # Left arm
    glPushMatrix()
    glTranslatef(-0.65, body_y_offset + 0.2, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(0.3, 0.9, 0.3)
    glPopMatrix()  

    # Head
    glPushMatrix() 
    glTranslatef(0.0, body_y_offset + 1.1, 0.0)  
    glColor3f(0.9, 0.8, 0.7)
    drawSphere(0.35)   
    glPopMatrix()  

    # Left leg
    glPushMatrix()
    glTranslatef(-0.3, leg_length/2, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(0.3, leg_length/2, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()

    glPopMatrix()

    
def Sanjoy_model(lying=False):
    glPushMatrix()

    if lying:
        glRotatef(-90.0, 1, 0, 0)

    leg_length = 1
    body_height = 1
    body_y_offset = leg_length # body sits on top of legs

    # Dark blue color
    body_color = (0.0, 0.0, 0.3)

    # Body (main cube)
    glPushMatrix()
    glTranslatef(0.0, body_y_offset+.2, 0.0)
    glColor3f(*body_color)
    drawCuboid(1.0, body_height, 0.6)  
    glPopMatrix()
   
    # Right arm
    glPushMatrix()
    glTranslatef(.65, body_y_offset + 0.2, 0.0)
    glColor3f(*body_color)
    drawCuboid(0.3, 0.9, 0.3) 
    glPopMatrix()  

    # Left arm
    glPushMatrix()
    glTranslatef(-0.65, body_y_offset + 0.2, 0.0)
    glColor3f(*body_color)
    drawCuboid(0.3, 0.9, 0.3)
    glPopMatrix()  

    # Head
    glPushMatrix() 
    glTranslatef(0.0, body_y_offset + 1.1, 0.0)  
    glColor3f(0.9, 0.8, 0.7)  # skin color
    drawSphere(0.35)   
    glPopMatrix()  

    # Left leg
    glPushMatrix()
    glTranslatef(-0.3, leg_length/2, 0.0)
    glColor3f(*body_color)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(0.3, leg_length/2, 0.0)
    glColor3f(*body_color)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()

    glPopMatrix()


def Ishrak_model(lying=False):
    glPushMatrix()

    if lying:
        glRotatef(-90.0, 1, 0, 0)

    leg_length = 1.66
    body_height = 1.6
    body_y_offset = leg_length  # move body above legs

    # Body (main cuboid)
    glPushMatrix()
    glTranslatef(0.0, body_y_offset, 0.0)
    glColor3f(0.5, 0.0, 0.5)  # Purple
    drawCuboid(1.2, body_height, 0.6)
    glPopMatrix()

    # Right arm
    glPushMatrix()
    glTranslatef(0.65, body_y_offset + 0.2, 0.0)
    glColor3f(0.5, 0.0, 0.5)
    drawCuboid(0.3, 0.9, 0.3)
    glPopMatrix()

    # Left arm
    glPushMatrix()
    glTranslatef(-0.65, body_y_offset + 0.2, 0.0)
    glColor3f(0.5, 0.0, 0.5)
    drawCuboid(0.3, 0.9, 0.3)
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0.0, body_y_offset + 1.1, 0.0)
    glColor3f(0.9, 0.8, 0.7)  # Skin tone
    drawSphere(0.35)
    glPopMatrix()

    # Left leg
    glPushMatrix()
    glTranslatef(-0.3, leg_length / 2, 0.0)
    glColor3f(0.5, 0.0, 0.5)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(0.3, leg_length / 2, 0.0)
    glColor3f(0.5, 0.0, 0.5)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()

    glPopMatrix()

    