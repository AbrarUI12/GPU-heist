# boss.py
import random, time, math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutSolidSphere
from model import Sru_model
from classes import player
import enemy

# ---------------- Boss Settings ----------------
class Boss:
    def __init__(self):
        self.pos = [57, 30.8, -2.0]   # spawn location
        self.health = 50
        self.speed = 0.02               # slow movement
        self.size = 2.5                 # larger than player
        self.last_shot_time = time.time()
        self.shot_interval = 3.0        # seconds between shots
        self.projectiles = []           # list of balls shot
# ---------------- Settings ----------------
BOSS_RADIUS = 1.5
BOSS_SPEED = 0.005
BOSS_STRAFE_SPEED = 0.005
DESIRED_DIST = 18.0   # tries to maintain this distance from player
SHOOT_DELAY = 2.0     # seconds between shots
STUN_DURATION = 3.0   # seconds stunned after being hit
PROJECTILE_SPEED = 10
PROJECTILE_RADIUS = 0.3
boss_spawned = False

# ---------------- State ----------------
boss = {
    "pos": [57, 30.8, -2.0],
    "health": 100,
    "last_shot": time.time(),
    "stunned_until": 0,
    "strafe_dir": 1,   # +1 right, -1 left
    "hit_count": 0,
}

# ---------------- Projectile ----------------
class Projectile:
    def __init__(self, start_pos, direction):
        self.pos = start_pos[:]
        self.dir = direction
        self.speed = 0.08   # slow speed so player can dodge
        self.radius = 0.3
projectiles = []  # boss bullets

# ---------------- Logic ----------------
def shoot():
    now = time.time()
    if now - boss["last_shot"] < SHOOT_DELAY:
        return
    boss["last_shot"] = now

    # Direction toward player
    dx = player.pos[0] - boss["pos"][0]
    dy = (player.pos[1] + 0.75) - boss["pos"][1]
    dz = player.pos[2] - boss["pos"][2]
    dist = math.sqrt(dx*dx + dy*dy + dz*dz)
    if dist == 0: return
    dx, dy, dz = dx/dist, dy/dist, dz/dist

    projectiles.append({
        "pos": boss["pos"][:],
        "dir": [dx, dy, dz],
    })


def update_boss(dt):
    now = time.time()

    # ---------------- Stun check ----------------
    if now < boss["stunned_until"]:
        return  # stunned: no move, no shoot

    # ---------------- Movement ----------------
    dx = player.pos[0] - boss["pos"][0]
    dz = player.pos[2] - boss["pos"][2]
    dist = math.sqrt(dx*dx + dz*dz)

    if dist > 0:  # avoid division by zero
        nx, nz = dx / dist, dz / dist

        # maintain distance from player
        if dist > DESIRED_DIST + 2:
            boss["pos"][0] += nx * BOSS_SPEED * dt * 60
            boss["pos"][2] += nz * BOSS_SPEED * dt * 60
        elif dist < DESIRED_DIST - 2:
            boss["pos"][0] -= nx * BOSS_SPEED * dt * 60
            boss["pos"][2] -= nz * BOSS_SPEED * dt * 60

    # strafe randomly
    if random.random() < 0.01:  # sometimes flip direction
        boss["strafe_dir"] *= -1
    boss["pos"][0] += boss["strafe_dir"] * BOSS_STRAFE_SPEED * dt * 60

    # ---------------- Shooting ----------------
    shoot()

    # ---------------- Update projectiles ----------------
    for proj in projectiles[:]:
        proj["pos"][0] += proj["dir"][0] * PROJECTILE_SPEED * dt * 60
        proj["pos"][1] += proj["dir"][1] * PROJECTILE_SPEED * dt * 60
        proj["pos"][2] += proj["dir"][2] * PROJECTILE_SPEED * dt * 60

        # collision with player
        dx = proj["pos"][0] - player.pos[0]
        dy = proj["pos"][1] - player.pos[1]
        dz = proj["pos"][2] - player.pos[2]
        if dx*dx + dy*dy + dz*dz < (PROJECTILE_RADIUS + 0.5)**2:
            player.health = max(player.health - 5, 0)
            projectiles.remove(proj)


def draw_boss():
    # draw boss
    glPushMatrix()
    glTranslatef(*boss["pos"])
    Sru_model()
    glPopMatrix()

    # draw projectiles
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 0.0, 0.0)
    for proj in projectiles:
        glPushMatrix()
        glTranslatef(*proj["pos"])
        glutSolidSphere(PROJECTILE_RADIUS, 12, 12)
        glPopMatrix()
    glEnable(GL_LIGHTING)


def hit_by_player():
    """Call this when the player's projectile hits the boss"""
    boss["health"] -= 10
    boss["stunned_until"] = time.time() + STUN_DURATION
    boss["hit_count"] += 1

    print(f"[BOSS HIT] Boss health: {boss['health']} (Hit count: {boss['hit_count']})")

    if boss["hit_count"] % 4 == 0:  # spawn 2 enemies every 4 hits
        print("[BOSS SUMMON] Spawning 2 new enemies!")
        bx, by, bz = boss["pos"]

        # spawn two enemies slightly offset from boss but not exactly on top
        for _ in range(2):
            ox = random.choice([-1, 1]) * random.uniform(1.0, 2.0)
            oz = random.choice([-1, 1]) * random.uniform(1.0, 2.0)
            enemy.spawn_enemy(x=bx + ox, y=by, z=bz + oz)


# boss.py
def reset_boss():
    """Despawn boss and clear projectiles"""
    global boss_spawned, projectiles
    boss_spawned = False
    projectiles.clear()
    boss["pos"] = [-87.5, 0.75, 67.5]  # reset spawn position
    boss["health"] = 100
    boss["hit_count"] = 0
    boss["stunned_until"] = 0
    boss["last_shot"] = time.time()
