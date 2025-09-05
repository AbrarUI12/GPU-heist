from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from model import *  
from classes import Enemy
import random
WORLD_HALF = 100.0  # should match your grid/world size
# List to hold all enemies
enemies = []
def draw_circle(radius, segments=40):
    """Draws a flat circle on the XZ plane (y=0)"""
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        theta = 2.0 * math.pi * float(i) / segments
        x = radius * math.cos(theta)
        z = radius * math.sin(theta)
        glVertex3f(x, 0.01, z)  # slightly above ground (y=0.01) to prevent z-fighting
    glEnd()

def bounce_enemy(enemy, half=WORLD_HALF):
    """Bounce enemy back into the world and turn them around if they hit boundary"""
    bounced = False

    # Check X boundaries
    if enemy.pos[0] < -half:
        enemy.pos[0] = -half
        bounced = True
    elif enemy.pos[0] > half:
        enemy.pos[0] = half
        bounced = True

    # Check Z boundaries
    if enemy.pos[2] < -half:
        enemy.pos[2] = -half
        bounced = True
    elif enemy.pos[2] > half:
        enemy.pos[2] = half
        bounced = True

    # If bounced, turn enemy 180° so they move back in
    if bounced:
        # Instead of 180°, pick a new random direction
        enemy.move_dir = random.uniform(0, 360)
        enemy.angDeg = enemy.move_dir
        # Reset timer so they keep this new direction a bit
        enemy.change_dir_timer = random.uniform(2.0, 5.0)

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
            # draw_female_teacher()
            draw_female_teacher

        glPopMatrix()

        # --- Draw awareness radius circle ---
        glPushMatrix()
        glTranslatef(enemy.pos[0], 0, enemy.pos[2])  # circle on ground
        glColor3f(1.0, 0.0, 0.0)  # red
        draw_circle(enemy.awareness_radius)
        glColor3f(1.0, 1.0, 1.0)  # reset to white
        glPopMatrix()

# Optional: update enemies (movement, AI, etc.)
import crouch
from classes import player
import math, random

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[2]-b[2])**2)

def wander(enemy, dt, speed=0.5):
    """Wander around with random direction changes"""
    # Countdown until direction change
    enemy.change_dir_timer -= dt
    if enemy.change_dir_timer <= 0:
        # Pick a new random direction
        enemy.move_dir = random.uniform(0, 360)
        enemy.change_dir_timer = random.uniform(5.0, 10.0)

    # Move in current direction
    rad = math.radians(enemy.move_dir)
    enemy.pos[0] += math.cos(rad) * speed * dt
    enemy.pos[2] += math.sin(rad) * speed * dt

    # Face towards move direction
    enemy.angDeg = enemy.move_dir

def move_towards(enemy, target, dt, speed=2.0):
    """Move enemy towards a target position (attack mode)"""
    dx = target[0] - enemy.pos[0]
    dz = target[2] - enemy.pos[2]
    dist = math.sqrt(dx*dx + dz*dz)
    if dist > 0.1:
        enemy.pos[0] += (dx/dist) * speed * dt
        enemy.pos[2] += (dz/dist) * speed * dt
        enemy.angDeg = math.degrees(math.atan2(dz, dx))

def update_enemies(dt):
    for enemy in enemies:
        # Awareness radius is smaller if crouching
        base_radius = 8.0 if enemy.state == "patrol" else 12.0
        if crouch.is_crouching:
            base_radius *= 0.7
        enemy.awareness_radius = base_radius

        dist = distance(enemy.pos, player.pos)

        # ---- STATE MACHINE ----
        if enemy.state == "patrol":
            wander(enemy, dt, speed=0.5)
            if dist < enemy.awareness_radius:
                # Player must stay for 1s to trigger attack
                if enemy.last_player_detect_time is None:
                    enemy.last_player_detect_time = time.time()
                elif time.time() - enemy.last_player_detect_time > 0.2:
                    enemy.state = "attack"
                    print("Enemy switched to ATTACK mode")
            else:
                enemy.last_player_detect_time = None

        elif enemy.state == "attack":
            move_towards(enemy, player.pos, dt, speed=1.0)
            if dist > enemy.awareness_radius:
                enemy.state = "clueless"
                enemy.state_timer = 0.0
                print("Enemy lost player → CLUELESS mode")

        elif enemy.state == "clueless":
            wander(enemy, dt, speed=1.2)
            if dist < enemy.awareness_radius:
                # Player re-enters radius, reset timer
                enemy.state = "attack"
                print("Enemy re-engaged → ATTACK mode")
            else:
                enemy.state_timer += dt
                if enemy.state_timer > 5.0:
                    enemy.state = "patrol"
                    enemy.last_player_detect_time = None
                    print("Enemy calmed down → PATROL mode")
        bounce_enemy(enemy)
        # Remove dead enemy
        if enemy.health <= 0:
            enemies.remove(enemy)

