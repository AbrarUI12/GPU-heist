from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from model import *  
from classes import Enemy
import random

# List to hold all enemies
enemies = []

# Example: spawn one enemy at a fixed location
def spawn_enemy(x=None, y=.75, z=None, health=2):
    enemy = Enemy()

    if x is None:
        x = random.uniform(-20.0, 20.0)  # random X
    if z is None:
        z = random.uniform(-20.0, 20.0)  # random Z

    enemy.pos = [x, y, z]
    enemy.health = health

    # 🔥 Assign a random type ONCE
    enemy.model_type = random.choice(["guard", "male_teacher", "female_teacher"])

    print(f"Spawned enemy at {enemy.pos} with type {enemy.model_type}")
    enemies.append(enemy)
    return enemy

# Draw all enemies
def draw_enemies():
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy.pos[0], enemy.pos[1], enemy.pos[2])
        glRotatef(enemy.angDeg, 0, 1, 0)
        glScalef(enemy.scale, enemy.scale, enemy.scale)

        # 🔥 Stick to their assigned model_type
        if enemy.model_type == "guard":
            draw_security_guard()
        elif enemy.model_type == "male_teacher":
            draw_male_teacher()
        else:
            draw_female_teacher()

        glPopMatrix()

# Optional: update enemies (movement, AI, etc.)
def update_enemies(dt):
    for enemy in enemies:
        #Example: rotate slowly
        enemy.angDeg += 20.0 * dt
        enemy.angDeg %= 360
        if enemy.health <= 0:
            enemies.remove(enemy)
