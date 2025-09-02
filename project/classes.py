# Player settings
PLAYER_Y = 0.75
MOVE_SPEED = 10.0


class Player:
    def __init__(self):
        self.pos = [0.0, PLAYER_Y, 0.0]
        self.angDeg = 0.0
        self.lying = False
        self.scale = 1.0   
        self.balls=0
        self.health=10
player = Player()

class Enemy:
    def __init__(self):
        self.pos = [10.0, PLAYER_Y, 10.0]
        self.angDeg = 0.0
        self.scale = 1.0   
        self.health=2