# mini_boss.py
import random, time, math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutSolidSphere
from model import draw_security_guard
from classes import player
import spawn_ammocrate
import floors

# ---------------- Settings ----------------
MINI_BOSS_RADIUS = 1.0
ACTIVATION_RADIUS = 15.0  # Distance to start shooting
SHOOT_DELAY = 1.5         # seconds between shots
PROJECTILE_SPEED = 0.4    # Slower than main boss
PROJECTILE_RADIUS = 0.25

# ---------------- Floor Control ----------------
# Set which floors should have mini bosses (0=Ground, 1=6th, 2=12th)
MINI_BOSS_FLOORS = [0]  # Currently only ground floor - MODIFY THIS TO CHANGE FLOORS

# ---------------- Mini Boss Data ----------------
mini_bosses = {}  # floor_num -> mini_boss_data

def create_mini_boss(floor_num, spawn_pos):
    """Create a mini boss for a specific floor"""
    return {
        "pos": list(spawn_pos),
        "health": 5,
        "max_health": 5,
        "last_shot": time.time(),
        "active": True,
        "defeated": False,
        "projectiles": [],
        "activation_radius": ACTIVATION_RADIUS,
        "floor": floor_num,
        # Add movement states like enemies
        "state": "patrol",
        "awareness_radius": ACTIVATION_RADIUS,
        "player_in_radius_timer": 0.0,
        "move_dir": random.uniform(0, 360),
        "change_dir_timer": random.uniform(2.0, 5.0),
        "angDeg": 0.0,
        "high_alert_end_time": 0.0,
        "high_alert_duration": random.uniform(5.0, 9.0)
    }

def spawn_mini_boss_on_floor(floor_num):
    """Spawn mini boss on specified floor if enabled"""
    if floor_num not in MINI_BOSS_FLOORS:
        return False
    
    if floor_num in mini_bosses and mini_bosses[floor_num]["active"]:
        return False  # Already exists
    
    # Get safe spawn position away from walls
    spawn_pos = get_safe_spawn_position(floor_num)
    if spawn_pos:
        mini_bosses[floor_num] = create_mini_boss(floor_num, spawn_pos)
        print(f"[MINI-BOSS] Spawned on floor {floor_num} at {spawn_pos}")
        return True
    return False

def get_safe_spawn_position(floor_num):
    """Find a safe spawn position away from walls"""
    obstacles = floors.get_floor_obstacles(floor_num)
    y_offset = floors.get_floor_y_offset(floor_num)
    
    # Try multiple random positions
    for _ in range(20):
        x = random.uniform(-80, 80)
        z = random.uniform(-80, 80)
        pos = [x, y_offset + 0.75, z]
        
        # Check if position is clear of obstacles
        if is_position_clear(pos, obstacles, 3.0):  # 3 unit clearance
            return pos
    
    # Fallback to center of floor
    return [0, y_offset + 0.75, 0]

def is_position_clear(pos, obstacles, clearance):
    """Check if position is clear of obstacles"""
    px, py, pz = pos
    
    for obs in obstacles:
        ox, oy, oz = obs["pos"]
        w, h, d = obs["size"]
        
        # Check if too close to obstacle
        if (abs(px - ox) < (w/2 + clearance) and 
            abs(pz - oz) < (d/2 + clearance)):
            return False
    return True

def is_line_clear(start_pos, end_pos, floor_num):
    """Check if line of sight is clear between two points"""
    obstacles = floors.get_floor_obstacles(floor_num)
    
    # Simple ray-box intersection check
    dx = end_pos[0] - start_pos[0]
    dz = end_pos[2] - start_pos[2]
    distance = math.sqrt(dx*dx + dz*dz)
    
    if distance == 0:
        return True
    
    # Normalize direction
    dx /= distance
    dz /= distance
    
    # Check points along the ray
    steps = int(distance / 2.0)  # Check every 2 units
    for i in range(1, steps):
        check_x = start_pos[0] + dx * i * 2.0
        check_z = start_pos[2] + dz * i * 2.0
        check_y = start_pos[1]
        
        # Check if this point intersects any obstacle
        for obs in obstacles:
            ox, oy, oz = obs["pos"]
            w, h, d = obs["size"]
            
            if (ox - w/2 <= check_x <= ox + w/2 and
                oy <= check_y <= oy + h and
                oz - d/2 <= check_z <= oz + d/2):
                return False
    
    return True

def wander_mini_boss(mini_boss, dt, speed=0.1):
    """Mini boss wandering movement"""
    mini_boss["change_dir_timer"] -= dt
    if mini_boss["change_dir_timer"] <= 0:
        mini_boss["move_dir"] = random.uniform(0, 360)
        mini_boss["change_dir_timer"] = random.uniform(5.0, 10.0)

    rad = math.radians(mini_boss["move_dir"])
    new_x = mini_boss["pos"][0] + math.cos(rad) * speed * dt * 60
    new_z = mini_boss["pos"][2] + math.sin(rad) * speed * dt * 60
    
    # Check for wall collision before moving
    if not check_mini_boss_wall_collision([new_x, mini_boss["pos"][1], new_z], mini_boss["floor"]):
        mini_boss["pos"][0] = new_x
        mini_boss["pos"][2] = new_z
        mini_boss["angDeg"] = mini_boss["move_dir"]
    else:
        # Hit a wall, choose new direction
        mini_boss["move_dir"] = random.uniform(0, 360)
        mini_boss["change_dir_timer"] = random.uniform(1.0, 3.0)

def move_towards_player(mini_boss, target_pos, dt, speed=0.1):
    """Move mini boss toward player"""
    dx = target_pos[0] - mini_boss["pos"][0]
    dz = target_pos[2] - mini_boss["pos"][2]
    dist = math.sqrt(dx*dx + dz*dz)
    
    if dist > 0.1:
        new_x = mini_boss["pos"][0] + (dx / dist) * speed * dt * 60
        new_z = mini_boss["pos"][2] + (dz / dist) * speed * dt * 60
        
        # Check for wall collision before moving
        if not check_mini_boss_wall_collision([new_x, mini_boss["pos"][1], new_z], mini_boss["floor"]):
            mini_boss["pos"][0] = new_x
            mini_boss["pos"][2] = new_z
            mini_boss["angDeg"] = math.degrees(math.atan2(dz, dx))
        else:
            # Can't move toward target due to wall, try to move around
            perp_angle = math.degrees(math.atan2(dz, dx)) + 90
            rad = math.radians(perp_angle)
            alt_x = mini_boss["pos"][0] + math.cos(rad) * speed * dt * 60 * 0.5
            alt_z = mini_boss["pos"][2] + math.sin(rad) * speed * dt * 60 * 0.5
            
            if not check_mini_boss_wall_collision([alt_x, mini_boss["pos"][1], alt_z], mini_boss["floor"]):
                mini_boss["pos"][0] = alt_x
                mini_boss["pos"][2] = alt_z

def check_mini_boss_wall_collision(pos, floor_num, radius=0.8):
    """Check if mini boss position collides with walls"""
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

def shoot_at_player(mini_boss):
    """Mini boss shoots at player if in range and line of sight is clear"""
    now = time.time()
    if now - mini_boss["last_shot"] < SHOOT_DELAY:
        return
    
    # Check distance to player
    dx = player.pos[0] - mini_boss["pos"][0]
    dy = player.pos[1] - mini_boss["pos"][1]
    dz = player.pos[2] - mini_boss["pos"][2]
    distance = math.sqrt(dx*dx + dy*dy + dz*dz)
    
    if distance > mini_boss["activation_radius"]:
        return
    
    # Check line of sight
    if not is_line_clear(mini_boss["pos"], player.pos, mini_boss["floor"]):
        return
    
    mini_boss["last_shot"] = now
    
    # Create projectile toward player
    if distance > 0:
        direction = [dx/distance, dy/distance, dz/distance]
        projectile = {
            "pos": mini_boss["pos"][:],
            "dir": direction,
            "lifetime": 5.0  # 5 second lifetime
        }
        mini_boss["projectiles"].append(projectile)

def update_mini_boss(floor_num, dt):
    """Update mini boss on specific floor with movement and shooting"""
    if floor_num not in mini_bosses:
        return
    
    mini_boss = mini_bosses[floor_num]
    if not mini_boss["active"] or mini_boss["defeated"]:
        return
    
    # Only update if player is on same floor
    if floors.get_current_floor() != floor_num:
        return
    
    now = time.time()
    
    # Calculate distance to player
    dx = player.pos[0] - mini_boss["pos"][0]
    dz = player.pos[2] - mini_boss["pos"][2]
    distance = math.sqrt(dx*dx + dz*dz)
    
    # ----- STATE MACHINE (like enemies) -----
    if mini_boss["state"] == "patrol":
        # Wander around, detect player if they get close
        wander_mini_boss(mini_boss, dt, speed=0.1)
        
        if distance < mini_boss["awareness_radius"]:
            mini_boss["player_in_radius_timer"] += dt
            if mini_boss["player_in_radius_timer"] >= 0.5:  # 0.5 second detection time
                mini_boss["state"] = "attack"
                mini_boss["player_in_radius_timer"] = 0.0
                print(f"[MINI-BOSS] Floor {floor_num} switching to ATTACK mode")
        else:
            mini_boss["player_in_radius_timer"] = 0.0
    
    elif mini_boss["state"] == "attack":
        # Chase player and shoot
        move_towards_player(mini_boss, player.pos, dt, speed=0.1)
        
        # Shoot at player if in range and line of sight is clear
        shoot_at_player(mini_boss)
        
        # If player escapes, go to high alert
        if distance > mini_boss["awareness_radius"] + 3:
            mini_boss["state"] = "high_alert"
            mini_boss["high_alert_duration"] = random.uniform(5.0, 9.0)
            mini_boss["high_alert_end_time"] = now + mini_boss["high_alert_duration"]
            print(f"[MINI-BOSS] Floor {floor_num} lost player → HIGH_ALERT")
    
    elif mini_boss["state"] == "high_alert":
        # Alert wandering, ready to re-engage quickly
        wander_mini_boss(mini_boss, dt, speed=0.1)
        
        if distance < mini_boss["awareness_radius"]:
            # Immediate re-engage
            mini_boss["state"] = "attack"
            mini_boss["player_in_radius_timer"] = 0.0
            mini_boss["high_alert_end_time"] = 0.0
            print(f"[MINI-BOSS] Floor {floor_num} re-engaged → ATTACK mode")
        else:
            # Check if high alert time is over
            if mini_boss["high_alert_end_time"] == 0.0:
                mini_boss["high_alert_duration"] = random.uniform(5.0, 9.0)
                mini_boss["high_alert_end_time"] = now + mini_boss["high_alert_duration"]
            if now >= mini_boss["high_alert_end_time"]:
                mini_boss["state"] = "patrol"
                mini_boss["player_in_radius_timer"] = 0.0
                mini_boss["high_alert_end_time"] = 0.0
                print(f"[MINI-BOSS] Floor {floor_num} calmed down → PATROL mode")
    
    # Update projectiles (existing code)
    for proj in mini_boss["projectiles"][:]:
        # Move projectile
        proj["pos"][0] += proj["dir"][0] * PROJECTILE_SPEED * dt * 60
        proj["pos"][1] += proj["dir"][1] * PROJECTILE_SPEED * dt * 60
        proj["pos"][2] += proj["dir"][2] * PROJECTILE_SPEED * dt * 60
        
        # Check lifetime
        proj["lifetime"] -= dt
        if proj["lifetime"] <= 0:
            mini_boss["projectiles"].remove(proj)
            continue
        
        # Check wall collision
        if check_projectile_wall_collision(proj["pos"], floor_num):
            mini_boss["projectiles"].remove(proj)
            continue
        
        # Check player collision
        dx = proj["pos"][0] - player.pos[0]
        dy = proj["pos"][1] - player.pos[1]
        dz = proj["pos"][2] - player.pos[2]
        if dx*dx + dy*dy + dz*dz < (PROJECTILE_RADIUS + 0.5)**2:
            player.health = max(player.health - 3, 0)
            print(f"[MINI-BOSS] Player hit! Health: {player.health}")
            mini_boss["projectiles"].remove(proj)


def draw_mini_boss(floor_num):
    """Draw mini boss on specific floor"""
    if floor_num not in mini_bosses:
        return
    
    mini_boss = mini_bosses[floor_num]
    if not mini_boss["active"] or mini_boss["defeated"]:
        return
    
    # Only draw if player is on same floor
    if floors.get_current_floor() != floor_num:
        return
    
    # Draw mini boss with rotation
    glPushMatrix()
    glTranslatef(*mini_boss["pos"])
    glRotatef(mini_boss["angDeg"], 0, 1, 0)  # Add rotation
    glColor3f(0.8, 0.0, 0.0)  # Red color for mini boss
    draw_security_guard()
    glPopMatrix()
    
    # Draw health bar above mini boss
    draw_mini_boss_health_bar(mini_boss)
    
    # Draw projectiles
    glDisable(GL_LIGHTING)
    glColor3f(0.8, 0.4, 0.0)  # Orange projectiles
    for proj in mini_boss["projectiles"]:
        glPushMatrix()
        glTranslatef(*proj["pos"])
        glutSolidSphere(PROJECTILE_RADIUS, 8, 8)
        glPopMatrix()
    glEnable(GL_LIGHTING)

def draw_mini_boss_health_bar(mini_boss):
    """Draw health bar above mini boss"""
    if mini_boss["health"] <= 0:
        return
    
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    
    # Position above mini boss
    bar_y = mini_boss["pos"][1] + 3.0
    bar_width = 2.0
    bar_height = 0.3
    
    # Background (red)
    glColor3f(0.8, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(mini_boss["pos"][0], bar_y, mini_boss["pos"][2])
    glBegin(GL_QUADS)
    glVertex3f(-bar_width/2, 0, 0)
    glVertex3f(bar_width/2, 0, 0)
    glVertex3f(bar_width/2, bar_height, 0)
    glVertex3f(-bar_width/2, bar_height, 0)
    glEnd()
    glPopMatrix()
    
    # Health fill (green)
    health_ratio = mini_boss["health"] / mini_boss["max_health"]
    health_width = bar_width * health_ratio
    glColor3f(0.0, 0.8, 0.0)
    glPushMatrix()
    glTranslatef(mini_boss["pos"][0], bar_y, mini_boss["pos"][2])
    glBegin(GL_QUADS)
    glVertex3f(-bar_width/2, 0, 0)
    glVertex3f(-bar_width/2 + health_width, 0, 0)
    glVertex3f(-bar_width/2 + health_width, bar_height, 0)
    glVertex3f(-bar_width/2, bar_height, 0)
    glEnd()
    glPopMatrix()
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

def hit_mini_boss(floor_num, damage=1):
    """Damage mini boss on specific floor"""
    if floor_num not in mini_bosses:
        return False
    
    mini_boss = mini_bosses[floor_num]
    if not mini_boss["active"] or mini_boss["defeated"]:
        return False
    
    mini_boss["health"] -= damage
    print(f"[MINI-BOSS] Floor {floor_num} hit! Health: {mini_boss['health']}")
    
    if mini_boss["health"] <= 0:
        mini_boss["defeated"] = True
        mini_boss["active"] = False
        
        # Spawn ammo crate nearby
        crate_pos = [
            mini_boss["pos"][0] + random.uniform(-3, 3),
            mini_boss["pos"][1],
            mini_boss["pos"][2] + random.uniform(-3, 3)
        ]
        
        # Force spawn ammo crate
        spawn_ammocrate.ammo_crate = {
            "pos": crate_pos,
            "collected": False
        }
        
        print(f"[MINI-BOSS] Floor {floor_num} defeated! Ammo crate spawned.")
        return True
    
    return False

def reset_mini_bosses():
    """Reset all mini bosses"""
    global mini_bosses
    mini_bosses.clear()
    print("[MINI-BOSS] All mini bosses reset")

def get_mini_boss_count():
    """Get number of active mini bosses"""
    return sum(1 for mb in mini_bosses.values() if mb["active"] and not mb["defeated"])

def initialize_mini_bosses():
    """Initialize mini bosses on enabled floors"""
    for floor_num in MINI_BOSS_FLOORS:
        spawn_mini_boss_on_floor(floor_num)