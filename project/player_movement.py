
from math import sin, cos, radians
from helper_fun import *
from classes import player

PLAYER_Y = 0.75
MOVE_SPEED = 4.0
# Movement
def movePlayer(dirSign, dt):
    fx, fz = forward_vec(player.angDeg)
    nx = player.pos[0] + dirSign * MOVE_SPEED * dt * fx
    nz = player.pos[2] + dirSign * MOVE_SPEED * dt * fz
    if insideWalls(nx, nz):
        player.pos[0] = nx
        player.pos[2] = nz

def strafePlayer(dirSign, dt):
    fx, fz = forward_vec(player.angDeg)
    nx = player.pos[0] + dirSign * MOVE_SPEED * dt * fz
    nz = player.pos[2] - dirSign * MOVE_SPEED * dt * fx
    if insideWalls(nx, nz):
        player.pos[0] = nx
        player.pos[2] = nz