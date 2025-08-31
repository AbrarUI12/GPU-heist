from helper_fun import *
from classes import player

PLAYER_Y = 0.75

def movePlayer(dirSign, dt, speed):
    fx, fz = forward_vec(player.angDeg)
    nx = player.pos[0] + dirSign * speed * dt * fx
    nz = player.pos[2] + dirSign * speed * dt * fz
    if insideWalls(nx, nz):
        player.pos[0] = nx
        player.pos[2] = nz

def strafePlayer(dirSign, dt, speed):
    fx, fz = forward_vec(player.angDeg)
    nx = player.pos[0] + dirSign * speed * dt * fz
    nz = player.pos[2] - dirSign * speed * dt * fx
    if insideWalls(nx, nz):
        player.pos[0] = nx
        player.pos[2] = nz
