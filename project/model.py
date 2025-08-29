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

    # Body (main cube)
    glPushMatrix()
    glTranslatef(0.0, 0.5, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(1.0, 1.0, 0.6)  
    glPopMatrix()
   
    #Right arm
    glPushMatrix()
    glTranslatef(.65, 0.7, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(0.3, 0.7, 0.3) 
    glPopMatrix()  

    # Left arm
    glPushMatrix()
    glTranslatef(-0.65, 0.7, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(0.3, 0.7, 0.3)
    glPopMatrix()  

    #head
    glPushMatrix() 
    glTranslatef(0.0, 1.3, 0.0)  
    glColor3f(0.9, 0.8, 0.7)
    drawSphere(0.35)   
    glPopMatrix()  

    # Left leg
    glPushMatrix()
    glTranslatef(-0.3, -0.8, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(0.3, 1.5, 0.3)
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(0.3, -0.8, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(0.3, 1.5, 0.3)
    glPopMatrix()

    glPopMatrix()
    
def Sanjoy_model(lying=False):
    glPushMatrix()

    if lying:
        glRotatef(-90.0, 1, 0, 0)

    # Body (main cube)
    glPushMatrix()
    glTranslatef(0.0, 0.3, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(1.0, 1.0, 0.6)  
    glPopMatrix()
   
    #Right arm
    glPushMatrix()
    glTranslatef(.65, 0.5, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(0.3, 0.7, 0.3) 
    glPopMatrix()  

    # Left arm
    glPushMatrix()
    glTranslatef(-0.65, 0.5, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(0.3, 0.7, 0.3)
    glPopMatrix()  

    #head
    glPushMatrix() 
    glTranslatef(0.0, 1.1, 0.0)  
    glColor3f(0.9, 0.8, 0.7)
    drawSphere(0.35)   
    glPopMatrix()  

    # Left leg
    glPushMatrix()
    glTranslatef(-0.3, -0.8, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(0.3, 1.5, 0.3)
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(0.3, -0.8, 0.0)
    glColor3f(0.09, 0.09, 0.09)
    drawCuboid(0.3, 1.5, 0.3)
    glPopMatrix()

    glPopMatrix()
    