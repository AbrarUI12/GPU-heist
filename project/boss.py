# boss.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, time, random
from classes import player

# ---------------- Boss Settings ----------------
class Boss:
    def __init__(self):
        self.pos = [0.0, 0.75, -20.0]   # spawn location
        self.health = 50
        self.speed = 0.02               # slow movement
        self.size = 2.5                 # larger than player
        self.last_shot_time = time.time()
        self.shot_interval = 3.0        # seconds between shots
        self.projectiles = []           # list of balls shot

boss = Boss()

# ---------------- Projectile ----------------
class Projectile:
    def __init__(self, start_pos, direction):
        self.pos = start_pos[:]
        self.dir = direction
        self.speed = 0.08   # slow speed so player can dodge
        self.radius = 0.3

    def update(self, dt):
        self.pos[0] += self.dir[0] * self.speed
        self.pos[1] += self.dir[1] * self.speed
        self.pos[2] += self.dir[2] * self.speed

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.pos)
        glColor3f(1.0, 0.2, 0.2)  # red projectile
        glutSolidSphere(self.radius, 12, 12)
        glPopMatrix()

# ---------------- Boss Functions ----------------
def draw_boss():
    glPushMatrix()
    glTranslatef(*boss.pos)
    glScalef(boss.size, boss.size, boss.size)
    glColor3f(0.2, 0.0, 0.5)  # dark purple
    glutSolidCube(1.0)
    glPopMatrix()

    # Draw projectiles
    for proj in boss.projectiles:
        proj.draw()

def update_boss(dt):
    # Move boss slowly towards player
    dx = player.pos[0] - boss.pos[0]
    dz = player.pos[2] - boss.pos[2]
    dist = math.sqrt(dx*dx + dz*dz)
    if dist > 1.5:  # stop when close
        boss.pos[0] += (dx / dist) * boss.speed
        boss.pos[2] += (dz / dist) * boss.speed

    # Shooting logic
    now = time.time()
    if now - boss.last_shot_time > boss.shot_interval:
        shoot_at_player()
        boss.last_shot_time = now

    # Update projectiles
    for proj in boss.projectiles:
        proj.update(dt)

    # Remove projectiles too far away
    boss.projectiles = [p for p in boss.projectiles if abs(p.pos[0]) < 100 and abs(p.pos[2]) < 100]

def shoot_at_player():
    dx = player.pos[0] - boss.pos[0]
    dy = (player.pos[1] + 0.5) - boss.pos[1]
    dz = player.pos[2] - boss.pos[2]
    dist = math.sqrt(dx*dx + dy*dy + dz*dz)
    if dist == 0: 
        return
    dir_vec = [dx/dist, dy/dist, dz/dist]
    proj = Projectile(boss.pos[:], dir_vec)
    boss.projectiles.append(proj)
