# Player settings
import random
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
        self.max_health = 10
        self.current_floor = 0
        self.has_gpu = False
player = Player()

class Enemy:
    def __init__(self):
        self.pos = [10.0, PLAYER_Y, 10.0]
        self.angDeg = 0.0
        self.scale = 1.0   
        self.health=2
        
        # --- AI State variables ---
        self.state = "patrol"          # can be "patrol", "attack", or "clueless"
        self.awareness_radius = 8.0    # default radius (changes with state/crouch)
        self.state_timer = 0.0         # used in clueless mode to count time
        self.player_in_radius_timer = 0.0  # used to track if player stayed 1s in radius
        self.model_type = "guard"      # default; overridden when spawning

        # --- Movement wandering ---
        self.move_dir = random.uniform(0, 360)   # current movement direction in degrees
        self.change_dir_timer = random.uniform(2.0, 5.0)  # time left before changing dir
        self.last_attack_time = 0.0   # track when enemy last damaged the player
        self.attack_cooldown = 1.0    # seconds between attacks

