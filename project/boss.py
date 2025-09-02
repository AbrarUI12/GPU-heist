# boss.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, random, time
from classes import player
from helper_fun import *

class Projectile:
    def __init__(self, start_pos, direction, speed=0.005):
        self.pos = list(start_pos)
        self.dir = direction
        self.speed = speed
        self.radius = 0.3
        self.active = True

    def update(self):
        if not self.active:
            return
        # Move projectile in its direction
        self.pos[0] += self.dir[0] * self.speed
        self.pos[1] += self.dir[1] * self.speed
        self.pos[2] += self.dir[2] * self.speed

        # Deactivate if too far
        if abs(self.pos[0]) > 100 or abs(self.pos[2]) > 100:
            self.active = False

    def draw(self):
        if not self.active:
            return
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glColor3f(0.75, 0.75, 0.75)  # ball color
        glutSolidSphere(self.radius, 12, 12)
        glPopMatrix()


class Boss:
    def __init__(self, x=0.0, y=0.75, z=-20.0):
        self.pos = [x, y, z]
        self.scale = 2.5
        self.color = (0.1, 0.8, 0.1)
        self.health = 100
        self.speed = 0.002
        self.last_shot_time = 0
        self.shot_interval = 2.5  # seconds
        self.projectiles = []

    def draw(self):
        """Draw the boss as a big red cube"""
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glScalef(self.scale, self.scale, self.scale)
        glColor3f(*self.color)
        drawSphere(1.0)
        glPopMatrix()

        # Draw projectiles
        for p in self.projectiles:
            p.draw()

    def update(self, player):
        """Boss AI update"""
        # Move toward player
        dx = player.pos[0] - self.pos[0]
        dz = player.pos[2] - self.pos[2]
        dist = math.sqrt(dx*dx + dz*dz)
        if dist > 0.1:
            self.pos[0] += (dx / dist) * self.speed
            self.pos[2] += (dz / dist) * self.speed

        # Shoot at player
        current_time = time.time()
        if current_time - self.last_shot_time > self.shot_interval:
            self.shoot(player)
            self.last_shot_time = current_time

        # Update projectiles
        for p in self.projectiles:
            p.update()

        # Remove inactive ones
        self.projectiles = [p for p in self.projectiles if p.active]

    def shoot(self, player):
        """Fire a slow projectile toward the player"""
        dx = player.pos[0] - self.pos[0]
        dy = player.pos[1] - self.pos[1]
        dz = player.pos[2] - self.pos[2]
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist == 0:
            return
        dir = [dx/dist, dy/dist, dz/dist]
        self.projectiles.append(Projectile(self.pos, dir))


# ---------------- Global Boss Instance ----------------
boss = Boss()

def spawn_boss():
    boss.pos[0] = random.uniform(-10, 10)
    boss.pos[1] = 0.75
    boss.pos[2] = random.uniform(-25, -15)

def draw_boss():
    boss.draw()

def update_boss():
    boss.update(player)
