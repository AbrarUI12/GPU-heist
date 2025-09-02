# throw_ball.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from classes import player
import enemy  # your enemy module

# Constants
BALL_SPEED = 15.0       # units per second
BALL_LIFETIME = 3.0     # seconds before disappearing
BALL_RADIUS = 0.2       # visual radius
THROW_HEIGHT = 0.8      # height from player's position

# Active thrown balls
thrown_balls = []

class ThrownBall:
    def __init__(self, pos, direction):
        self.pos = pos[:]        # current position [x, y, z]
        self.dir = direction[:]  # normalized direction vector
        self.distance_travelled = 0.0
        self.max_distance = BALL_SPEED * BALL_LIFETIME
        self.active = True

def throw_ball():
    """Throw a ball in the direction the player is facing if player has balls."""
    if player.balls <= 0:
        return  # cannot throw

    ang_rad = math.radians(player.angDeg)
    dx = math.sin(ang_rad)
    dz = math.cos(ang_rad)
    start_pos = [player.pos[0], player.pos[1] + THROW_HEIGHT, player.pos[2]]
    direction = [dx, 0.0, dz]  # flat horizontal throw

    thrown_balls.append(ThrownBall(start_pos, direction))
    player.balls -= 1  # decrement available balls

def update_balls(dt):
    """Move all active balls and check collisions with enemies."""
    for ball_obj in thrown_balls:
        if not ball_obj.active:
            continue

        # Move ball
        ball_obj.pos[0] += ball_obj.dir[0] * BALL_SPEED * dt
        ball_obj.pos[1] += ball_obj.dir[1] * BALL_SPEED * dt
        ball_obj.pos[2] += ball_obj.dir[2] * BALL_SPEED * dt

        # Update distance travelled
        ball_obj.distance_travelled += BALL_SPEED * dt
        if ball_obj.distance_travelled >= ball_obj.max_distance:
            ball_obj.active = False
            continue

        # Check collision with enemies
        for e in enemy.enemies:  # enemies list in enemy.py
            dx = ball_obj.pos[0] - e.pos[0]
            dy = ball_obj.pos[1] - e.pos[1]
            dz = ball_obj.pos[2] - e.pos[2]
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if dist < BALL_RADIUS + 0.5:  # assuming enemy radius ~0.5
                e.health -= 1
                ball_obj.active = False
                break

def draw_balls():
    """Render all active thrown balls."""
    glDisable(GL_LIGHTING)
    glColor3f(0.0, 1.0, 0.0)  # green ball
    for ball_obj in thrown_balls:
        if ball_obj.active:
            glPushMatrix()
            glTranslatef(*ball_obj.pos)
            glutSolidSphere(BALL_RADIUS, 12, 12)
            glPopMatrix()
    glEnable(GL_LIGHTING)
