from helper_fun import *
from classes import player
# from obstacles import checkCollision
import floors  # Add this import


import crouch


PLAYER_Y = 0.75

def checkFloorCollision(x, y, z, floor_num):
    """Check collision with current floor obstacles"""
    obstacles = floors.get_floor_obstacles(floor_num)
    for obs in obstacles:
        ox, oy, oz = obs["pos"]
        w, h, d = obs["size"]
        min_x, max_x = ox - w/2, ox + w/2
        min_y, max_y = oy, oy + h
        min_z, max_z = oz - d/2, oz + d/2
        if min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z:
            return True
    return False

def movePlayer(dirSign, dt, speed):
    print(crouch.is_crouching)
    if crouch.is_crouching:
        speed *= 0.3
    
    fx, fz = forward_vec(player.angDeg)
    # Predict new horizontal position
    nx = player.pos[0] + dirSign * speed * dt * fx
    nz = player.pos[2] + dirSign * speed * dt * fz

    # Keep current vertical position for collision
    ny = player.pos[1]
    
    # Get current floor for collision checking
    current_floor = floors.get_current_floor()

    if insideWalls(nx, nz) and not checkFloorCollision(nx, ny, nz, current_floor):
        player.pos[0] = nx
        player.pos[2] = nz

def strafePlayer(dirSign, dt, speed):
    if crouch.is_crouching:
        speed *= 0.3
    fx, fz = forward_vec(player.angDeg)
    nx = player.pos[0] + dirSign * speed * dt * fz
    nz = player.pos[2] - dirSign * speed * dt * fx
    ny = player.pos[1]
    
    # Get current floor for collision checking
    current_floor = floors.get_current_floor()

    if insideWalls(nx, nz) and not checkFloorCollision(nx, ny, nz, current_floor):
        player.pos[0] = nx
        player.pos[2] = nz