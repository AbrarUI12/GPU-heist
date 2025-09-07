from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, time, random
from helper_fun import *
from model import *
from classes import Player, player
from camera import setupCamera
from draw_world import *
from player_movement import *
from jump import start_jump, update_jump
from obstacles import drawObstacles
import crouch
from jump import start_jump
import balls
import hud
import enemy
import throw_ball
import boss
import floors
import floor_transitions  
import game_states
import spawn_ammocrate
import mini_boss
from camera import setupCamera, drawCrosshair

# ---------------- Window / world settings ----------------
WIN_W, WIN_H = 1024, 720
GRID_STEP = 5.0
CAMERA_DIST = 10.0
PLAYER_Y = 0.75
dt = 0.016

# Camera settings
firstPerson = False
camYawDeg = 30.0
camPitchDeg = 20.0
camDist = CAMERA_DIST
PI = math.pi

# Game states
MENU = 0
PLAYING = 1
game_state = MENU

# Selected model
selected_model = None

# Floor spawning tracking
floors_initialized = set()
boss_battle_prompted = False

# ---------------- Input ----------------
pressed_keys = {}  # key -> True if pressed

lastMouseX = None
sensitivity = 0.3

def spawn_floor_entities(floor_num):
    """Spawn entities based on floor number"""
    global floors_initialized
    
    if floor_num in floors_initialized:
        return  # Already spawned for this floor
    
    print(f"[SPAWN] Initializing floor {floor_num}")
    
    if floor_num == 0:  # Ground floor
        # Spawn 5 enemies
        spawn_enemies_on_floor(floor_num, 5)
        # Spawn mini boss
        mini_boss.spawn_mini_boss_on_floor(floor_num)
        
    elif floor_num == 1:  # 6th floor
        # Spawn 5 enemies
        spawn_enemies_on_floor(floor_num, 5)
        # Spawn ammo crate
        spawn_ammocrate.spawn_ammo_crate()
        
    elif floor_num == 2:  # 12th floor
        # Boss is handled separately in main display loop
        pass
    
    floors_initialized.add(floor_num)

def spawn_enemies_on_floor(floor_num, count):
    """Spawn enemies on specific floor avoiding walls"""
    obstacles = floors.get_floor_obstacles(floor_num)
    y_offset = floors.get_floor_y_offset(floor_num)
    
    spawned = 0
    attempts = 0
    max_attempts = 50
    
    while spawned < count and attempts < max_attempts:
        # Random position
        x = random.uniform(-80, 80)
        z = random.uniform(-80, 80)
        y = y_offset + 0.75
        
        # Check if position is clear
        if is_spawn_position_safe([x, y, z], obstacles):
            enemy.spawn_enemy(x, y, z)
            spawned += 1
            print(f"[SPAWN] Enemy {spawned}/{count} spawned at ({x:.1f}, {y:.1f}, {z:.1f})")
        
        attempts += 1
    
    if spawned < count:
        print(f"[SPAWN] Warning: Only spawned {spawned}/{count} enemies after {max_attempts} attempts")

def is_spawn_position_safe(pos, obstacles, clearance=3.0):
    """Check if spawn position is safe from walls"""
    px, py, pz = pos
    
    for obs in obstacles:
        ox, oy, oz = obs["pos"]
        w, h, d = obs["size"]
        
        # Check if too close to obstacle
        if (abs(px - ox) < (w/2 + clearance) and 
            abs(pz - oz) < (d/2 + clearance)):
            return False
    return True

# ---------------- Menu / display ----------------
def draw_menu():
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(0.1, 0.1, 0.15)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(WIN_W, 0)
    glVertex2f(WIN_W, WIN_H)
    glVertex2f(0, WIN_H)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)
    def draw_text(x, y, text):
        glRasterPos2f(x, y)
        for c in text.encode("utf-8"):
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c)

    draw_text(WIN_W*0.35, WIN_H*0.8, "Select Your Character:")
    draw_text(WIN_W*0.35, WIN_H*0.2, "Press 1 for Abrar | 2 for Sanjoy | 3 for Ishrak")

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    # Draw 3D models
    glPushMatrix()
    glTranslatef(-2.0, -1.5, -8.0)
    glRotatef(30, 0, 1, 0)
    Abrar_model()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, -1.5, -8.0)
    glRotatef(-30, 0, 1, 0)
    Sanjoy_model()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(2.0,-1.5, -8.0)
    glRotatef(-30, 0, 1, 0)
    Ishrak_model()
    glPopMatrix()

# ---------------- Display / reshape ----------------
def draw_game_over_screen():
    """Draw the game over screen"""
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Background - dark red for game over
    glColor3f(0.3, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(WIN_W, 0)
    glVertex2f(WIN_W, WIN_H)
    glVertex2f(0, WIN_H)
    glEnd()

    # Draw text function
    def draw_text(x, y, text, color=(1.0, 1.0, 1.0)):
        glColor3f(*color)
        glRasterPos2f(x, y)
        for c in text.encode("utf-8"):
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c)

    # Game over message
    glColor3f(1.0, 0.0, 0.0)  # Red
    draw_text(WIN_W*0.15, WIN_H*0.6, "Haha tore maira laisi. GPU shopner modhe rakh", (1.0, 0.0, 0.0))
    
    # Additional message
    draw_text(WIN_W*0.35, WIN_H*0.4, "You have been defeated!", (1.0, 1.0, 1.0))
    
    # Continue instruction
    draw_text(WIN_W*0.3, WIN_H*0.2, "Press any key to restart the game", (0.8, 0.8, 0.8))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)


def on_display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    if game_states.get_current_game_state() == game_states.GAME_MENU:
        draw_menu()
    
    elif game_states.get_current_game_state() == game_states.GAME_VICTORY:
        draw_victory_screen()

    elif game_states.get_current_game_state() == game_states.GAME_GAME_OVER:  # Add this
        draw_game_over_screen()

    elif game_states.get_current_game_state() == game_states.GAME_PLAYING:
        setupCamera()
        
        # Get current floor
        current_floor = floors.get_current_floor()
        
        # Spawn entities for current floor
        spawn_floor_entities(current_floor)
        
        # Show boss battle prompt for floor 2
        if current_floor == 2 and not boss_battle_prompted:
            show_boss_battle_prompt()
        
        # Draw current floor
        y_offset = floors.get_floor_y_offset(current_floor)
        glPushMatrix()
        glTranslatef(0, y_offset, 0)
        drawGrid(ARENA_HALF, GRID_STEP)
        glPopMatrix()
        
        # Draw floor-specific obstacles
        draw_floor_obstacles(current_floor)
        
        # Draw floor-specific elements (escalators, doors, etc.)
        floors.draw_floor_specific_elements(current_floor) 
        
        # Draw game objects only if on same floor as player
        if current_floor == 0:  # Ground floor items
          spawn_ammocrate.draw_ammo_crate()      
       
       
        if current_floor == 1:  # Ground floor items
            spawn_ammocrate.draw_ammo_crate()
        
        balls.draw_balls() 
        enemy.draw_enemies()
        
        # Draw mini boss for current floor
        mini_boss.draw_mini_boss(current_floor)
        
        throw_ball.draw_balls()
        
        # Boss on floor 2
        if current_floor == 2:
            if not boss.boss_spawned:
                boss.boss_spawned = True
                print("[BOSS SPAWNED] The final boss has appeared!")
            boss.update_boss(dt)
            boss.draw_boss()
        else:
            if boss.boss_spawned:
                boss.reset_boss()
                print("[BOSS DESPAWNED] Player left floor 3")
        
        # Draw player
        drawCrosshair()
        glPushMatrix()
        glTranslatef(player.pos[0], player.pos[1], player.pos[2])
        glRotatef(player.angDeg, 0, 1, 0)
        glScalef(player.scale, player.scale, player.scale)
        if selected_model == "Abrar":
            Abrar_model(player.lying)
        elif selected_model == "Sanjoy":
            Sanjoy_model(player.lying)
        elif selected_model == "Ishrak":
            Ishrak_model(player.lying)
        glPopMatrix()
        
        # Draw HUD with mission info
        draw_game_hud()
        
    glutSwapBuffers()

def draw_floor_obstacles(floor_num):
    """Draw obstacles for current floor"""
    obstacles = floors.get_floor_obstacles(floor_num)
    y_offset = floors.get_floor_y_offset(floor_num)
    
    for obs in obstacles:
        x, y, z = obs["pos"]
        w, h, d = obs["size"]
        
        # Color walls differently from other obstacles
        if obs.get("type") == "wall":
            glColor3f(0.6, 0.6, 0.6)  # Gray walls
        else:
            glColor3f(0.8, 0.1, 0.1)  # Red obstacles
            
        glPushMatrix()
        glTranslatef(x, y + h / 2, z)
        drawCuboid(w, h, d)
        glPopMatrix()

def draw_gpu_theft_progress():
    """Draw GPU theft progress bar"""
    progress = game_states.get_gpu_theft_progress()
    
    # Center of screen
    bar_width = 300
    bar_height = 30
    bar_x = WIN_W // 2 - bar_width // 2
    bar_y = WIN_H // 2
    
    # Background
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(bar_x, bar_y)
    glVertex2f(bar_x + bar_width, bar_y)
    glVertex2f(bar_x + bar_width, bar_y + bar_height)
    glVertex2f(bar_x, bar_y + bar_height)
    glEnd()
    
    # Progress fill
    fill_width = bar_width * progress
    glColor3f(0.0, 1.0, 0.0)  # Green
    glBegin(GL_QUADS)
    glVertex2f(bar_x, bar_y)
    glVertex2f(bar_x + fill_width, bar_y)
    glVertex2f(bar_x + fill_width, bar_y + bar_height)
    glVertex2f(bar_x, bar_y + bar_height)
    glEnd()
    
    # Text
    glColor3f(1.0, 1.0, 1.0)
    steal_text = "Hold E to steal GPU..."
    glRasterPos2f(bar_x, bar_y + bar_height + 10)
    for c in steal_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    
    # Progress percentage
    percent_text = f"{int(progress * 100)}%"
    glRasterPos2f(bar_x + bar_width // 2 - 20, bar_y + bar_height // 2)
    for c in percent_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

def show_boss_battle_prompt():
    """Show boss battle prompt on floor 2"""
    global boss_battle_prompted
    boss_battle_prompted = True
    print("[BOSS BATTLE] Final floor reached!")

def draw_boss_battle_hud():
    """Draw boss battle prompt on HUD"""
    if floors.get_current_floor() == 2:
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WIN_W, 0, WIN_H)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Boss battle text
        glColor3f(1.0, 0.0, 0.0)  # Red
        boss_text = "BOSS BATTLE!"
        glRasterPos2f(WIN_W//2 - 60, WIN_H - 100)
        for c in boss_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

def draw_game_hud():
    """Enhanced HUD with mission information and debug info"""
    hud.draw_hud(player, player.health, selected_model)
    
    # Draw boss battle prompt if on floor 2
    draw_boss_battle_hud()
    
    # Add mission text and debug info
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Mission text
    glColor3f(1.0, 1.0, 0.0)  # Yellow
    mission_text = game_states.get_mission_text()
    glRasterPos2f(50, 50)
    for c in mission_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    
    # Floor indicator
    current_floor = floors.get_current_floor()
    floor_name = floors.FLOORS[current_floor]["name"]
    floor_text = f"Floor: {current_floor} ({floor_name})"
    glRasterPos2f(WIN_W - 250, WIN_H - 50)
    for c in floor_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    
    # Player position (debug info)
    pos_text = f"Pos: ({player.pos[0]:.1f}, {player.pos[1]:.1f}, {player.pos[2]:.1f})"
    glRasterPos2f(WIN_W - 250, WIN_H - 80)
    for c in pos_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    
    # Controls help
    glColor3f(0.7, 0.7, 0.7)  # Light gray
    help_text = "Controls: P-Debug, M-Matrix, R-Reset, E-Interact"
    glRasterPos2f(50, 20)
    for c in help_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    
    # GPU theft progress bar
    if game_states.is_gpu_theft_in_progress():
        draw_gpu_theft_progress()
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

def on_reshape(w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, w / float(h), 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW)

def init_gl():
    glClearColor(0.09, 0.09, 0.11, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (5.0, 8.0, 10.0, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.9, 0.9, 0.9, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

# ---------------- Keyboard ----------------
def on_keyboard(key, x, y):
    global selected_model
    
    # Handle game over screen - any key returns to menu
    if game_states.get_current_game_state() == game_states.GAME_GAME_OVER:
        game_states.reset_game_to_menu()
        glutPostRedisplay()
        return
    # Handle victory screen - any key returns to menu
    if game_states.get_current_game_state() == game_states.GAME_VICTORY:
        game_states.reset_game_to_menu()
        glutPostRedisplay()
        return

    # Menu selection
    if game_states.get_current_game_state() == game_states.GAME_MENU:
        if key == b'1':
            selected_model = "Abrar"
            player.balls = 6
            player.health = 10
            game_states.set_game_state(game_states.GAME_PLAYING)
            set_player_spawn_at_door()
        elif key == b'2':
            selected_model = "Sanjoy"
            player.balls = 12
            player.health = 10
            game_states.set_game_state(game_states.GAME_PLAYING)
            set_player_spawn_at_door()
        elif key == b'3':
            selected_model = "Ishrak"
            player.balls = 6
            player.health = 20
            game_states.set_game_state(game_states.GAME_PLAYING)
            set_player_spawn_at_door()
        glutPostRedisplay()
        return

    # Game playing controls
    if game_states.get_current_game_state() != game_states.GAME_PLAYING:
        return

    try:
        ch = key.decode('utf-8').lower()
    except:
        return
    pressed_keys[ch] = True
    
    # Debug keys
    if ch == 'p':  # Print floor debug info
        floors.debug_current_floor()
    elif ch == 'm':  # Print floor matrices info
        try:
            from floor_plan_parser import debug_floor_layout
            debug_floor_layout(floors.get_current_floor())
        except ImportError:
            print("Floor plan parser not available")
    elif ch == 'r':  # Reset player position to door entrance
        set_player_spawn_at_door()
        print("Reset player to door entrance")
    
    # Interaction key 'e'
    if ch == 'e':
        handle_interactions()
    
    # Jump on spacebar
    if ch == ' ' and not crouch.is_crouching:
        start_jump()

    # Crouch with "c"
    if ch == 'c':
        crouch.toggle_crouch(player)

def handle_interactions():
    """Handle player interactions with environment"""
    # Check escalator interaction
    escalator_type, new_floor = floor_transitions.check_escalator_interaction()
    if escalator_type and not floor_transitions.is_transitioning():
        floor_transitions.start_escalator_transition(escalator_type, new_floor)
        return
    
    # Check object collection
    if game_states.handle_object_collection():
        print("GPU Collection initiated!")
        return
    
    # Check door interaction
    door_result = game_states.handle_door_interaction()
    if door_result == "victory":
        print("VICTORY! You escaped with the GPU!")
    elif door_result == "enter":
        print("Entered the building")

def on_keyboard_up(key, x, y):
    try:
        ch = key.decode('utf-8').lower()
    except:
        return
    pressed_keys[ch] = False

# ---------------- Mouse ----------------
def on_mouse_motion(x, y):
    global lastMouseX
    if lastMouseX is None:
        lastMouseX = x
        return
    deltaX = lastMouseX - x
    player.angDeg += deltaX * sensitivity
    player.angDeg %= 360
    lastMouseX = x
    glutPostRedisplay()

def on_mouse_click(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        import throw_ball
        throw_ball.throw_ball()

# ---------------- Update (per-frame) ----------------
def update():
    if game_states.get_current_game_state() != game_states.GAME_PLAYING:
        return

    speed = 8.0 if selected_model == "Abrar" else 4.0
    dt = 0.01
    
    # Don't allow movement during transitions
    if not floor_transitions.is_transitioning():
        if pressed_keys.get('w', False):
            movePlayer(1, dt, speed)
        if pressed_keys.get('s', False):
            movePlayer(-1, dt, speed)
        if pressed_keys.get('a', False):
            strafePlayer(1, dt, speed)
        if pressed_keys.get('d', False):
            strafePlayer(-1, dt, speed)

    # Update systems
    floor_transitions.update_transitions(dt)
    game_states.update_mission_progress()
    update_jump(player, dt)
    
    # Get current floor
    current_floor = floors.get_current_floor()
    
    # Update mini boss for current floor
    mini_boss.update_mini_boss(current_floor, dt)
    
    # Update GPU theft progress
    holding_e = pressed_keys.get('e', False)
    game_states.update_gpu_theft(dt, holding_e)
    
    # **FIXED: Update enemies on ALL floors, not just floor 0**
    enemy.update_enemies(dt)
    
    # Update other game objects
    balls.check_collection(player)
    throw_ball.update_balls(dt)
    spawn_ammocrate.check_crate_collection(player)
    boss.update_boss(dt)

    glutPostRedisplay()

def set_player_spawn_at_door():
    """Set player spawn position at the building entrance door"""
    global floors_initialized
    from classes import player
    
    # Reset floor spawning when player respawns
    floors_initialized.clear()
    mini_boss.reset_mini_bosses()
    
    player.pos[0] = -87.5  # X coordinate (inside building)
    player.pos[1] = 0.75   # Y coordinate (ground level + player height)
    player.pos[2] = 67.5   # Z coordinate (aligned with middle door)
    
    print(f"Player spawned at door entrance: ({player.pos[0]}, {player.pos[1]}, {player.pos[2]})")

def draw_victory_screen():
    """Draw the victory screen"""
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Background - dark green for victory
    glColor3f(0.0, 0.3, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(WIN_W, 0)
    glVertex2f(WIN_W, WIN_H)
    glVertex2f(0, WIN_H)
    glEnd()

    # Draw text function
    def draw_text(x, y, text, color=(1.0, 1.0, 1.0)):
        glColor3f(*color)
        glRasterPos2f(x, y)
        for c in text.encode("utf-8"):
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c)

    # Victory message
    glColor3f(1.0, 1.0, 0.0)  # Yellow
    draw_text(WIN_W*0.25, WIN_H*0.6, "HAHA KIPTA BRAC RE HARAISI!", (1.0, 1.0, 0.0))
    
    # Additional messages
    draw_text(WIN_W*0.35, WIN_H*0.5, "Mission Accomplished!", (0.0, 1.0, 0.0))
    draw_text(WIN_W*0.3, WIN_H*0.4, "You successfully stole the GPU!", (1.0, 1.0, 1.0))
    
    # Continue instruction
    draw_text(WIN_W*0.3, WIN_H*0.2, "Press any key to return to menu", (0.8, 0.8, 0.8))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

# ---------------- Main ----------------
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIN_W, WIN_H)
    glutCreateWindow(b"BRAC University GPU Heist")
    init_gl()
    set_player_spawn_at_door()
    balls.spawn_balls()
    spawn_ammocrate.spawn_ammo_crate()
    
    glutDisplayFunc(on_display)
    glutReshapeFunc(on_reshape)
    glutKeyboardFunc(on_keyboard)
    glutKeyboardUpFunc(on_keyboard_up)
    glutPassiveMotionFunc(on_mouse_motion)
    glutIdleFunc(update)
    glutMouseFunc(on_mouse_click) 
    
    print("="*50)
    print("BRAC UNIVERSITY GPU HEIST - FLOOR PLAN LOADED")
    print("="*50)
    try:
        from floor_plan_parser import debug_floor_layout
        for floor in range(3):
            debug_floor_layout(floor)
    except ImportError:
        print("Using fallback floor data")
    
    print("\nDebug Controls:")
    print("P - Print current floor debug info")
    print("M - Print current floor matrix layout") 
    print("R - Reset player position to floor origin")
    print("E - Interact with escalators/doors/objects")
    print("="*50)
    
    glutMainLoop()

if __name__ == "__main__":
    main()