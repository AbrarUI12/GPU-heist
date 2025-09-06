# jump.py
# Smooth parabolic jump for your player
import floors

GRAVITY = -20.0       # acceleration downward (units/sec^2)
JUMP_SPEED = 10.0     # initial upward velocity
GROUND_Y = 0.75       # normal player Y position

# Track jump state
is_jumping = False
vertical_velocity = 0.0

def start_jump():
    """Call this when the jump key is pressed (e.g., spacebar)."""
    global is_jumping, vertical_velocity
    if not is_jumping:
        vertical_velocity = JUMP_SPEED
        is_jumping = True

from obstacles import obstacles  # your obstacle list/dict

def update_jump(player, dt):
    """
    Update player's vertical position, including landing on floor obstacles.
    """
    global is_jumping, vertical_velocity

    if not is_jumping:
        return

    # Apply velocity to position
    new_y = player.pos[1] + vertical_velocity * dt

    # Apply gravity
    vertical_velocity += GRAVITY * dt

    landed = False
    current_floor = floors.get_current_floor()
    floor_y_offset = floors.get_floor_y_offset(current_floor)
    ground_y = floor_y_offset + 0.75  # Floor level + player height offset

    # Check collision with current floor obstacles
    obstacles = floors.get_floor_obstacles(current_floor)
    for obs in obstacles:
        ox, oy, oz = obs["pos"]   # obstacle center
        w, h, d = obs["size"]     # obstacle width/height/depth

        # obstacle bounds
        min_x, max_x = ox - w/2, ox + w/2
        min_y, max_y = oy, oy + h
        min_z, max_z = oz - d/2, oz + d/2

        # Check if player is above obstacle and within its xz bounds
        if min_x <= player.pos[0] <= max_x and min_z <= player.pos[2] <= max_z:
            if player.pos[1] >= max_y and new_y <= max_y:
                new_y = max_y
                vertical_velocity = 0.0
                is_jumping = False
                landed = True
                break

    # Check collision with current floor ground
    if not landed and new_y <= ground_y:
        new_y = ground_y
        vertical_velocity = 0.0
        is_jumping = False

    player.pos[1] = new_y