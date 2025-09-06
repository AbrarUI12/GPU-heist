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




# ---------- SECURITY GUARD ----------
def draw_security_guard():
    glPushMatrix()

    leg_length = 1.5
    body_height = 1.5
    body_y_offset = leg_length

    # Body
    glPushMatrix()
    glTranslatef(0.0, body_y_offset, 0.0)
    glColor3f(1.0, 0.5, 0.0)
    drawCuboid(1.0, body_height, 0.6)
    glPopMatrix()

    # Arms
    glColor3f(1.0, 0.5, 0.0)
    glPushMatrix()
    glTranslatef(0.65, body_y_offset + 0.2, 0.0)
    drawCuboid(0.3, 0.9, 0.3)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-0.65, body_y_offset + 0.2, 0.0)
    drawCuboid(0.3, 0.9, 0.3)
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0.0, body_y_offset + 1.1, 0.0)
    glColor3f(0.9, 0.8, 0.7)
    drawSphere(0.35)
    glPopMatrix()

    # Legs
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(-0.3, leg_length/2, 0.0)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0.3, leg_length/2, 0.0)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()

    # Hat / Badge (optional)
    glPushMatrix()
    glTranslatef(0.0, body_y_offset + 1.45, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    drawCuboid(0.5, 0.2, 0.5)
    glPopMatrix()

    glPopMatrix()


# ---------- MALE TEACHER ----------
def draw_male_teacher():
    glPushMatrix()

    leg_length = 1.5
    body_height = 1.5
    body_y_offset = leg_length

    # Body
    glPushMatrix()
    glTranslatef(0.0, body_y_offset, 0.0)
    glColor3f(1.0, 1.0, 1.0)
    drawCuboid(1.0, body_height, 0.6)
    glPopMatrix()

    # Arms
    glColor3f(0.9, 0.7, 0.5)
    glPushMatrix()
    glTranslatef(0.65, body_y_offset + 0.2, 0.0)
    drawCuboid(0.3, 0.9, 0.3)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-0.65, body_y_offset + 0.2, 0.0)
    drawCuboid(0.3, 0.9, 0.3)
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0.0, body_y_offset + 1.1, 0.0)
    glColor3f(0.9, 0.8, 0.7)
    drawSphere(0.35)
    glPopMatrix()

    # Glasses
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0.25, body_y_offset + 1.1, 0.35)
    drawSphere(0.15)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-0.25, body_y_offset + 1.1, 0.35)
    drawSphere(0.15)
    glPopMatrix()

    # Legs
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(-0.3, leg_length/2, 0.0)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0.3, leg_length/2, 0.0)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()

    glPopMatrix()


# ---------- FEMALE TEACHER ----------
def draw_female_teacher():
    glPushMatrix()

    leg_length = 1.5
    body_height = 1.5
    body_y_offset = leg_length

    # Body (dress)
    glPushMatrix()
    glTranslatef(0.0, body_y_offset, 0.0)
    glColor3f(0.8, 0.1, 0.1)
    drawCuboid(1.0, body_height * 1.2, 0.6)
    glPopMatrix()

    # Arms
    glColor3f(0.9, 0.7, 0.5)
    glPushMatrix()
    glTranslatef(0.65, body_y_offset + 0.2, 0.0)
    drawCuboid(0.3, 0.9, 0.3)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-0.65, body_y_offset + 0.2, 0.0)
    drawCuboid(0.3, 0.9, 0.3)
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0.0, body_y_offset + 1.2, 0.0)
    glColor3f(0.9, 0.8, 0.7)
    drawSphere(0.35)
    glPopMatrix()

    # Hair bun
    glPushMatrix()
    glTranslatef(0.0, body_y_offset + 1.5, -0.1)
    glColor3f(0.3, 0.1, 0.0)
    drawSphere(0.25)
    glPopMatrix()

    # Legs / shoes
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(-0.3, leg_length/2, 0.0)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0.3, leg_length/2, 0.0)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()

    glPopMatrix()


def Sru_model(lying=False):
    glPushMatrix()

    if lying:
        glRotatef(-90.0, 1, 0, 0)

    leg_length = 1.66
    body_height = 1.6
    body_y_offset = leg_length  # move body above legs

    # --- Body (suit jacket, black) ---
    glPushMatrix()
    glTranslatef(0.0, body_y_offset, 0.0)
    glColor3f(0.0, 0.0, 0.0)  # Black suit
    drawCuboid(1.2, body_height, 0.6)
    glPopMatrix()

    # --- Shirt (white, slightly inset on chest) ---
    glPushMatrix()
    glTranslatef(0.0, body_y_offset + 0.05, 0.31)  # in front
    glColor3f(1.0, 1.0, 1.0)  # White shirt
    drawCuboid(0.6, body_height - 0.2, 0.05)
    glPopMatrix()

    # --- Right arm (black suit) ---
    glPushMatrix()
    glTranslatef(0.65, body_y_offset + 0.2, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    drawCuboid(0.3, 0.9, 0.3)
    glPopMatrix()

    # --- Left arm (black suit) ---
    glPushMatrix()
    glTranslatef(-0.65, body_y_offset + 0.2, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    drawCuboid(0.3, 0.9, 0.3)
    glPopMatrix()

    # --- Head ---
    glPushMatrix()
    glTranslatef(0.0, body_y_offset + 1.1, 0.0)
    glColor3f(0.9, 0.8, 0.7)  # Skin tone
    drawSphere(0.35)
    glPopMatrix()

    # --- Luffy Hat ---
    # Hat brim
    glPushMatrix()
    glTranslatef(0.0, body_y_offset + 1.25, 0.0)
    glScalef(1.3, 0.1, 1.3)
    glColor3f(0.9, 0.8, 0.4)  # Straw yellow
    drawSphere(0.4)
    glPopMatrix()

    # Hat dome
    glPushMatrix()
    glTranslatef(0.0, body_y_offset + 1.35, 0.0)
    glColor3f(0.9, 0.8, 0.4)
    drawSphere(0.38)
    glPopMatrix()

    # Hat red band
    glPushMatrix()
    glTranslatef(0.0, body_y_offset + 1.28, 0.0)
    glScalef(1.0, 0.3, 1.0)
    glColor3f(1.0, 0.0, 0.0)  # Red band
    drawSphere(0.36)
    glPopMatrix()

    # --- Left leg (black suit pants) ---
    glPushMatrix()
    glTranslatef(-0.3, leg_length / 2, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()

    # --- Right leg (black suit pants) ---
    glPushMatrix()
    glTranslatef(0.3, leg_length / 2, 0.0)
    glColor3f(0.0, 0.0, 0.0)
    drawCuboid(0.3, leg_length, 0.3)
    glPopMatrix()

    glPopMatrix()
