# enemy.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from model import Abrar_model  # you can change to an enemy model if needed
from classes import Enemy

# List to hold all enemies
enemies = []

# Example: spawn one enemy at a fixed location
def spawn_enemy(x=10.0, y=0.75, z=10.0, health=2):
    enemy = Enemy()
    enemy.pos = [x, y, z]
    enemy.health = health
    enemies.append(enemy)
    return enemy

# Draw all enemies
def draw_enemies():
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy.pos[0], enemy.pos[1], enemy.pos[2])
        glRotatef(enemy.angDeg, 0, 1, 0)
        glScalef(enemy.scale, enemy.scale, enemy.scale)
        # Use Abrar_model or any enemy model
        Abrar_model(False)
        glPopMatrix()

# Optional: update enemies (movement, AI, etc.)
def update_enemies(dt):
    for enemy in enemies:
        # Example: rotate slowly
        enemy.angDeg += 20.0 * dt
        enemy.angDeg %= 360
