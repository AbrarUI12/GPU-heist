# balls.py
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutSolidSphere


# World bounds (should match your grid/world size)
WORLD_HALF = 100.0  # example: same as your drawGrid half

BALL_RADIUS = 0.3   # visual size of ball
NUM_BALLS = 20      # number of balls in the world

balls = []  # list of active balls


def spawn_balls(num=NUM_BALLS):
    """Generate random ball positions within the world bounds."""
    global balls
    balls = []
    for _ in range(num):
        x = random.uniform(-WORLD_HALF + BALL_RADIUS, WORLD_HALF - BALL_RADIUS)
        z = random.uniform(-WORLD_HALF + BALL_RADIUS, WORLD_HALF - BALL_RADIUS)
        y = 0.75 + BALL_RADIUS  # slightly above ground
        balls.append({"pos": [x, y, z], "collected": False})


def draw_balls():
    """Render all uncollected balls."""
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 1.0, 0.0)  # yellow balls
    for ball in balls:
        if not ball["collected"]:
            glPushMatrix()
            glTranslatef(*ball["pos"])
            glutSolidSphere(BALL_RADIUS, 16, 16)
            glPopMatrix()
    glEnable(GL_LIGHTING)


def check_collection(player):
    """Check if player collects any balls."""
    collected_count = 0
    for ball in balls:
        if not ball["collected"]:
            dx = player.pos[0] - ball["pos"][0]
            dy = player.pos[1] - ball["pos"][1]
            dz = player.pos[2] - ball["pos"][2]  # fixed index
            distance = (dx*dx + dy*dy + dz*dz)**0.5
            if distance < BALL_RADIUS + 0.5:  # 0.5 ~ player radius
                ball["collected"] = True
                collected_count += 1
    player.balls += collected_count
