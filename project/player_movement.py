from helper_fun import *
from classes import player
from obstacles import checkCollision

PLAYER_Y = 0.75

def movePlayer(dirSign, dt, speed):
    fx, fz = forward_vec(player.angDeg)
    # Predict new horizontal position
    nx = player.pos[0] + dirSign * speed * dt * fx
    nz = player.pos[2] + dirSign * speed * dt * fz

    # Keep current vertical position for collision
    ny = player.pos[1]

    if insideWalls(nx, nz) and not checkCollision(nx, ny, nz):
        player.pos[0] = nx
        player.pos[2] = nz

def strafePlayer(dirSign, dt, speed):
    fx, fz = forward_vec(player.angDeg)
    nx = player.pos[0] + dirSign * speed * dt * fz
    nz = player.pos[2] - dirSign * speed * dt * fx
    ny = player.pos[1]

    if insideWalls(nx, nz) and not checkCollision(nx, ny, nz):
        player.pos[0] = nx
        player.pos[2] = nz
