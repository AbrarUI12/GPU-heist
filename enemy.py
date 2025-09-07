from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from model import *
from classes import Enemy, player
import random
import time
import math
import crouch
import floors

# ---------- Config ----------
WORLD_HALF = 100.0           # match your grid/world size
PATROL_RADIUS = 8.0
ATTACK_RADIUS = 12.0
PLAYER_DETECT_TIME = 0.5     # seconds player must remain in radius to trigger attack from patrol
HIGH_ALERT_MIN = 5.0         # min seconds to stay in high alert
HIGH_ALERT_MAX = 9.0         # max seconds to stay in high alert
DEFAULT_WANDER_SPEED = 0.5
DEFAULT_ATTACK_SPEED = 3.5
DEFAULT_HIGH_ALERT_WANDER_SPEED = 0.8
COLLISION_RADIUS = 1.5
COLLISION_DAMAGE = 1

# List to hold all enemies
enemies = []

# ---------- Utility drawing ----------
def draw_circle(radius, segments=40):
    """Draws a flat circle on the XZ plane (y=0) slightly above ground to avoid z-fighting."""
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        theta = 2.0 * math.pi * float(i) / segments
        x = radius * math.cos(theta)
        z = radius * math.sin(theta)
        glVertex3f(x, 0.01, z)
    glEnd()

def distance(a, b):
    return math.hypot(a[0] - b[0], a[2] - b[2])

def check_wall_collision(pos, floor_num, radius=0.5):
    """Check if position collides with walls on current floor"""
    obstacles = floors.get_floor_obstacles(floor_num)
    px, py, pz = pos
    
    for obs in obstacles:
        ox, oy, oz = obs["pos"]
        w, h, d = obs["size"]
        
        # Check if position is inside obstacle (with radius buffer)
        if (ox - w/2 - radius <= px <= ox + w/2 + radius and
            oy <= py <= oy + h and
            oz - d/2 - radius <= pz <= oz + d/2 + radius):
            return True
    return False

# ---------- Compatibility helper ----------
def ensure_enemy_attrs(enemy):
    """
    Ensure the enemy object has expected AI attributes (useful if classes.py is older).
    This avoids AttributeError and also establishes sane defaults.
    """
    if not hasattr(enemy, "state"):
        enemy.state = "patrol"
    if not hasattr(enemy, "awareness_radius"):
        enemy.awareness_radius = PATROL_RADIUS
    if not hasattr(enemy, "player_in_radius_timer"):
        enemy.player_in_radius_timer = 0.0
    if not hasattr(enemy, "state_timer"):
        enemy.state_timer = 0.0
    if not hasattr(enemy, "move_dir"):
        enemy.move_dir = random.uniform(0, 360)
    if not hasattr(enemy, "change_dir_timer"):
        enemy.change_dir_timer = random.uniform(2.0, 5.0)
    if not hasattr(enemy, "last_attack_time"):
        enemy.last_attack_time = 0.0
    if not hasattr(enemy, "attack_cooldown"):
        enemy.attack_cooldown = 1.0
    # high-alert timing (use wall-clock end-time so length is reliable)
    if not hasattr(enemy, "high_alert_end_time"):
        enemy.high_alert_end_time = 0.0
    if not hasattr(enemy, "high_alert_duration"):
        enemy.high_alert_duration = random.uniform(HIGH_ALERT_MIN, HIGH_ALERT_MAX)

# ---------- Collision / damage ----------
def check_player_collision(enemy, player_obj, damage=COLLISION_DAMAGE, radius=COLLISION_RADIUS):
    """
    Flat XZ collision check -> apply damage with cooldown per enemy.
    Uses time.time() for cooldown (fine to mix here).
    """
    dx = enemy.pos[0] - player_obj.pos[0]
    dz = enemy.pos[2] - player_obj.pos[2]
    dist = math.hypot(dx, dz)
    if dist < radius:
        now = time.time()
        if now - enemy.last_attack_time >= enemy.attack_cooldown:
            player_obj.health = max(0, player_obj.health - damage)
            enemy.last_attack_time = now
            print(f"⚠️ Player hit! Health = {player_obj.health}")

# ---------- Movement helpers ----------
def bounce_enemy(enemy, half=WORLD_HALF):
    """
    If the enemy crosses a boundary, push it back to the edge and give it a new random heading.
    This produces a natural-looking bounce with a fresh direction (not a strict 180° flip).
    """
    bounced = False

    if enemy.pos[0] < -half:
        enemy.pos[0] = -half
        bounced = True
    elif enemy.pos[0] > half:
        enemy.pos[0] = half
        bounced = True

    if enemy.pos[2] < -half:
        enemy.pos[2] = -half
        bounced = True
    elif enemy.pos[2] > half:
        enemy.pos[2] = half
        bounced = True

    if bounced:
        # choose a new heading and ensure they keep it for a short random time
        enemy.move_dir = random.uniform(0, 360)
        enemy.angDeg = enemy.move_dir
        enemy.change_dir_timer = random.uniform(2.0, 5.0)

def wander(enemy, dt, speed=DEFAULT_WANDER_SPEED):
    """
    Simple wandering: move in current move_dir; every now and then pick a new random dir.
    This uses dt-based countdown for consistent behavior when update calls vary.
    Now includes wall collision detection.
    """
    enemy.change_dir_timer -= dt
    if enemy.change_dir_timer <= 0:
        enemy.move_dir = random.uniform(0, 360)
        enemy.change_dir_timer = random.uniform(5.0, 10.0)

    rad = math.radians(enemy.move_dir)
    new_x = enemy.pos[0] + math.cos(rad) * speed * dt
    new_z = enemy.pos[2] + math.sin(rad) * speed * dt
    
    # Check for wall collision before moving
    current_floor = floors.get_current_floor()
    if not check_wall_collision([new_x, enemy.pos[1], new_z], current_floor):
        enemy.pos[0] = new_x
        enemy.pos[2] = new_z
        enemy.angDeg = enemy.move_dir
    else:
        # Hit a wall, choose new direction
        enemy.move_dir = random.uniform(0, 360)
        enemy.change_dir_timer = random.uniform(1.0, 3.0)

def move_towards(enemy, target_pos, dt, speed=DEFAULT_ATTACK_SPEED):
    """Move directly toward target_pos on XZ plane; rotate to face movement.
    Now includes wall collision detection."""
    dx = target_pos[0] - enemy.pos[0]
    dz = target_pos[2] - enemy.pos[2]
    dist = math.hypot(dx, dz)
    if dist > 0.1:
        new_x = enemy.pos[0] + (dx / dist) * speed * dt
        new_z = enemy.pos[2] + (dz / dist) * speed * dt
        
        # Check for wall collision before moving
        current_floor = floors.get_current_floor()
        if not check_wall_collision([new_x, enemy.pos[1], new_z], current_floor):
            enemy.pos[0] = new_x
            enemy.pos[2] = new_z
            enemy.angDeg = math.degrees(math.atan2(dz, dx))
        else:
            # Can't move toward target due to wall, try to move around
            # Try moving perpendicular to the wall
            perp_angle = math.degrees(math.atan2(dz, dx)) + 90
            rad = math.radians(perp_angle)
            alt_x = enemy.pos[0] + math.cos(rad) * speed * dt * 0.5
            alt_z = enemy.pos[2] + math.sin(rad) * speed * dt * 0.5
            
            if not check_wall_collision([alt_x, enemy.pos[1], alt_z], current_floor):
                enemy.pos[0] = alt_x
                enemy.pos[2] = alt_z

# ---------- Spawning & drawing ----------
def spawn_enemy(x=None, y=0.75, z=None, health=2):
    e = Enemy()
    if x is None:
        x = random.uniform(-20.0, 20.0)
    if z is None:
        z = random.uniform(-20.0, 20.0)
    e.pos = [x, y, z]
    e.health = health
    e.model_type = random.choice(["guard", "male_teacher", "female_teacher"])

    # ensure attributes exist (compatible with existing classes.py)
    ensure_enemy_attrs(e)
    # randomize high alert duration per enemy
    e.high_alert_duration = random.uniform(HIGH_ALERT_MIN, HIGH_ALERT_MAX)
    e.high_alert_end_time = 0.0

    enemies.append(e)
    print(f"Spawned enemy at {e.pos} with type {e.model_type}")
    return e

def draw_enemies():
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy.pos[0], enemy.pos[1], enemy.pos[2])
        glRotatef(enemy.angDeg, 0, 1, 0)
        glScalef(enemy.scale, enemy.scale, enemy.scale)

        if enemy.model_type == "guard":
            draw_security_guard()
        elif enemy.model_type == "male_teacher":
            draw_male_teacher()
        else:
            draw_female_teacher()  

        glPopMatrix()

        # draw awareness radius circle on the ground
        glPushMatrix()
        glTranslatef(enemy.pos[0], 0, enemy.pos[2])
        glColor3f(1.0, 0.0, 0.0)
        draw_circle(enemy.awareness_radius)
        glColor3f(1.0, 1.0, 1.0)
        glPopMatrix()

# ---------- Main AI update ----------
def update_enemies(dt):
    """Call this each frame with dt (seconds)."""
    now = time.time()
    for enemy in list(enemies):  # iterate a copy since we may remove
        # make sure enemy has all expected fields (backwards compatibility)
        ensure_enemy_attrs(enemy)

        # choose appropriate base radius depending on state
        if enemy.state == "patrol":
            base_radius = PATROL_RADIUS
        elif enemy.state == "attack":
            base_radius = ATTACK_RADIUS
        elif enemy.state == "high_alert":
            base_radius = ATTACK_RADIUS
        else:
            base_radius = PATROL_RADIUS

        # crouching global flag reduces awareness
        if crouch.is_crouching:
            base_radius *= 0.7
        enemy.awareness_radius = base_radius

        dist = distance(enemy.pos, player.pos)

        # ----- STATE MACHINE -----
        if enemy.state == "patrol":
            # normal wandering, require PLAYER_DETECT_TIME seconds to trigger attack
            wander(enemy, dt, speed=DEFAULT_WANDER_SPEED)
            if dist < enemy.awareness_radius:
                enemy.player_in_radius_timer += dt
                if enemy.player_in_radius_timer >= PLAYER_DETECT_TIME:
                    # player stayed long enough → attack
                    enemy.player_in_radius_timer = 0.0
                    enemy.state = "attack"
                    print("Enemy switched to ATTACK mode")
            else:
                enemy.player_in_radius_timer = 0.0

        elif enemy.state == "attack":
            # chase player
            move_towards(enemy, player.pos, dt, speed=DEFAULT_ATTACK_SPEED)
            # if player escapes attack radius → enter high alert (set wall-clock end time)
            if dist > enemy.awareness_radius:
                enemy.state = "high_alert"
                # Pick a random high-alert duration per instance to avoid synchronized calm-downs
                enemy.high_alert_duration = random.uniform(HIGH_ALERT_MIN, HIGH_ALERT_MAX)
                enemy.high_alert_end_time = now + enemy.high_alert_duration
                print(f"Enemy lost player → HIGH_ALERT for {enemy.high_alert_duration:.1f}s")

        elif enemy.state == "high_alert":
            # more alert wandering; immediate re-attack if player re-enters radius
            wander(enemy, dt, speed=DEFAULT_HIGH_ALERT_WANDER_SPEED)
            if dist < enemy.awareness_radius:
                # immediate re-engage
                enemy.state = "attack"
                enemy.player_in_radius_timer = 0.0
                enemy.high_alert_end_time = 0.0
                print("Enemy re-engaged → ATTACK mode")
            else:
                # rely on wall clock so we don't accidentally rush through due to dt issues
                if enemy.high_alert_end_time == 0.0:
                    enemy.high_alert_duration = random.uniform(HIGH_ALERT_MIN, HIGH_ALERT_MAX)
                    enemy.high_alert_end_time = now + enemy.high_alert_duration
                if now >= enemy.high_alert_end_time:
                    enemy.state = "patrol"
                    enemy.player_in_radius_timer = 0.0
                    enemy.high_alert_end_time = 0.0
                    print("Enemy calmed down → PATROL mode")

        # bounce at world edges with a random new heading on bounce
        bounce_enemy(enemy)

        # collision & damage (has its own cooldown)
        check_player_collision(enemy, player, damage=COLLISION_DAMAGE, radius=COLLISION_RADIUS)

        # remove dead
        if enemy.health <= 0:
            try:
                enemies.remove(enemy)
            except ValueError:
                pass