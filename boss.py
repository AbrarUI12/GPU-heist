# boss.py
import random, time, math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutSolidSphere
from model import Sru_model
from classes import player
import enemy
import floors

# ---------------- Settings ----------------
BOSS_RADIUS = 1.5
BOSS_SPEED = 0.4
BOSS_STRAFE_SPEED = 0.05
DESIRED_DIST = 18.0   # tries to maintain this distance from player
SHOOT_DELAY = 1.0     # seconds between shots
STUN_DURATION = 5.0   # seconds stunned after being hit
PROJECTILE_SPEED = .5
PROJECTILE_RADIUS = 0.3
boss_spawned = False

# ---------------- Initial State ----------------
BOSS_INIT = {
    "pos": [57, 30.8, -2.0],   # spawn location (floor 3)
    "health": 100,
    "last_shot": time.time(),
    "stunned_until": 0,
    "strafe_dir": 1,   # +1 right, -1 left
    "hit_count": 0,
}

boss = dict(BOSS_INIT)  # working copy

# ---------------- Projectile ----------------
class Projectile:
    def __init__(self, start_pos, direction):
        self.pos = start_pos[:]
        self.dir = direction
        self.speed = 0.08   # slow speed so player can dodge
        self.radius = 0.3

projectiles = []  # boss bullets

# ---------------- Wall Collision Function ----------------
def check_projectile_wall_collision(pos, floor_num):
    """Check if projectile hits a wall"""
    obstacles = floors.get_floor_obstacles(floor_num)
    px, py, pz = pos
    
    for obs in obstacles:
        ox, oy, oz = obs["pos"]
        w, h, d = obs["size"]
        
        # Check if projectile is inside obstacle
        if (ox - w/2 <= px <= ox + w/2 and
            oy <= py <= oy + h and
            oz - d/2 <= pz <= oz + d/2):
            return True
    return False

def check_boss_wall_collision(pos, floor_num, radius=BOSS_RADIUS):
    """Check if boss position collides with walls"""
    obstacles = floors.get_floor_obstacles(floor_num)
    px, py, pz = pos
    
    for obs in obstacles:
        ox, oy, oz = obs["pos"]
        w, h, d = obs["size"]
        
        # More precise collision detection
        if (ox - w/2 - radius < px < ox + w/2 + radius and
            oy - 1 < py < oy + h + 1 and
            oz - d/2 - radius < pz < oz + d/2 + radius):
            return True
    return False
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
    if dist == 0:
        return
    dx, dy, dz = dx/dist, dy/dist, dz/dist

    projectiles.append({
        "pos": boss["pos"][:],
        "dir": [dx, dy, dz],
    })

def update_boss(dt):
    if not boss_spawned:
        return  # don't update if despawned

    now = time.time()
    current_floor = floors.get_current_floor()

    # ---------------- Stun check ----------------
    if now < boss["stunned_until"]:
        return  # stunned: no move, no shoot

    # ---------------- Movement with Wall Collision ----------------
    dx = player.pos[0] - boss["pos"][0]
    dz = player.pos[2] - boss["pos"][2]
    dist = math.sqrt(dx*dx + dz*dz)

    # Store original position
    original_x = boss["pos"][0]
    original_z = boss["pos"][2]
    
    move_x = 0
    move_z = 0

    if dist > 0:  # avoid division by zero
        nx, nz = dx / dist, dz / dist

        # Calculate movement based on desired distance
        if dist > DESIRED_DIST + 2:
            move_x = nx * BOSS_SPEED * dt * 60
            move_z = nz * BOSS_SPEED * dt * 60
        elif dist < DESIRED_DIST - 2:
            move_x = -nx * BOSS_SPEED * dt * 60
            move_z = -nz * BOSS_SPEED * dt * 60

    # Add strafe movement
    if random.random() < 0.01:  # sometimes flip direction
        boss["strafe_dir"] *= -1
    move_x += boss["strafe_dir"] * BOSS_STRAFE_SPEED * dt * 60

    # Test new position with wall collision
    new_x = original_x + move_x
    new_z = original_z + move_z
    test_pos = [new_x, boss["pos"][1], new_z]
    
    # Only move if no wall collision
    if not check_boss_wall_collision(test_pos, current_floor):
        boss["pos"][0] = new_x
        boss["pos"][2] = new_z
    else:
        # Try moving only in X direction
        test_x_pos = [original_x + move_x, boss["pos"][1], original_z]
        if not check_boss_wall_collision(test_x_pos, current_floor):
            boss["pos"][0] = original_x + move_x
        else:
            # Try moving only in Z direction
            test_z_pos = [original_x, boss["pos"][1], original_z + move_z]
            if not check_boss_wall_collision(test_z_pos, current_floor):
                boss["pos"][2] = original_z + move_z
        # If both fail, don't move at all

    # ---------------- Shooting ----------------
    shoot()

    # ---------------- Update projectiles ----------------
    for proj in projectiles[:]:
        # Move projectile
        proj["pos"][0] += proj["dir"][0] * PROJECTILE_SPEED * dt * 60
        proj["pos"][1] += proj["dir"][1] * PROJECTILE_SPEED * dt * 60
        proj["pos"][2] += proj["dir"][2] * PROJECTILE_SPEED * dt * 60

        # Check wall collision
        if check_projectile_wall_collision(proj["pos"], current_floor):
            projectiles.remove(proj)
            continue

        # Check if projectile went too far (lifetime check)
        start_dist = math.sqrt(
            (proj["pos"][0] - boss["pos"][0])**2 + 
            (proj["pos"][1] - boss["pos"][1])**2 + 
            (proj["pos"][2] - boss["pos"][2])**2
        )
        if start_dist > 50.0:  # Max projectile range
            projectiles.remove(proj)
            continue

        # collision with player
        dx = proj["pos"][0] - player.pos[0]
        dy = proj["pos"][1] - player.pos[1]
        dz = proj["pos"][2] - player.pos[2]
        if dx*dx + dy*dy + dz*dz < (PROJECTILE_RADIUS + 0.5)**2:
            player.health = max(player.health - 2, 0)
            print(f"[BOSS ATTACK] Player hit! Health now {player.health}")
            projectiles.remove(proj)

def draw_boss():
    if not boss_spawned:
        return  # don't draw if despawned

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
    if not boss_spawned:
        return

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

def reset_boss():
    """Despawn boss and clear projectiles"""
    global boss_spawned, projectiles, boss
    boss_spawned = False
    projectiles.clear()
    boss = dict(BOSS_INIT)  # reset to initial values
    boss["last_shot"] = time.time()