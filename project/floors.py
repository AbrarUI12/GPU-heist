# floors.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from helper_fun import *
import obstacles

# Import the floor plan parser
try:
    from floor_plan_parser import generate_all_floors
    # Generate floors from matrices
    FLOORS = generate_all_floors()
    print("Loaded floors from floor plan matrices")
except ImportError:
    print("Warning: Could not import floor_plan_parser, using fallback data")
    # Fallback floor configuration (your original hardcoded data)
    FLOORS = {
        0: {  # Ground Floor
            "name": "Ground Floor",
            "y_offset": 0.0,
            "obstacles": [
                {"pos": (-20, 0.0, -20), "size": (5, 3, 1), "type": "wall"},
                {"pos": (15, 0.0, -25), "size": (3, 3, 2), "type": "wall"},
                {"pos": (-10, 0.0, 20), "size": (2, 3, 8), "type": "wall"},
            ],
            "door_pos": (0, 0, -45),
            "escalator_up": (30, 0, 30),
            "escalator_down": None,
        },
        1: {  # 6th Floor equivalent
            "name": "6th Floor",
            "y_offset": 15.0,
            "obstacles": [
                {"pos": (-15, 15.0, -15), "size": (4, 3, 1), "type": "wall"},
                {"pos": (10, 15.0, -20), "size": (6, 3, 2), "type": "wall"},
                {"pos": (0, 15.0, 15), "size": (8, 3, 1), "type": "wall"},
            ],
            "door_pos": None,
            "escalator_up": (25, 15, 25),
            "escalator_down": (30, 15, 30),
        },
        2: {  # 12th Floor equivalent
            "name": "12th Floor", 
            "y_offset": 30.0,
            "obstacles": [
                {"pos": (-20, 30.0, -10), "size": (3, 3, 6), "type": "wall"},
                {"pos": (20, 30.0, 10), "size": (4, 3, 4), "type": "wall"},
                {"pos": (0, 30.0, -25), "size": (10, 3, 2), "type": "wall"},
            ],
            "door_pos": None,
            "escalator_up": None,
            "escalator_down": (25, 30, 25),
            "target_object": (0, 30, 30),
        }
    }

current_floor = 0

def get_current_floor():
    return current_floor

def set_current_floor(floor_num):
    global current_floor
    if floor_num in FLOORS:
        current_floor = floor_num
        return True
    return False

def get_floor_obstacles(floor_num):
    """Get obstacles for specific floor"""
    if floor_num in FLOORS:
        return FLOORS[floor_num]["obstacles"]
    return []

def get_floor_y_offset(floor_num):
    """Get Y offset for specific floor"""
    if floor_num in FLOORS:
        return FLOORS[floor_num]["y_offset"]
    return 0.0

def draw_floor_specific_elements(floor_num):
    """Draw floor-specific elements like escalators, doors, etc."""
    if floor_num not in FLOORS:
        return
    
    floor_data = FLOORS[floor_num]
    
    # Draw door (if exists)
    if floor_data.get("door_pos"):
        draw_door(floor_data["door_pos"], floor_data["y_offset"])
    
    # Draw escalators
    if floor_data.get("escalator_up"):
        draw_escalator(floor_data["escalator_up"], floor_data["y_offset"], "up")
    
    if floor_data.get("escalator_down"):
        draw_escalator(floor_data["escalator_down"], floor_data["y_offset"], "down")
    
    # Draw target object (if exists)
    if floor_data.get("target_object"):
        draw_target_object(floor_data["target_object"], floor_data["y_offset"])

def draw_door(pos, y_offset):
    """Draw entry/exit door"""
    glPushMatrix()
    glTranslatef(pos[0], y_offset + 1.5, pos[2])
    glColor3f(0.6, 0.3, 0.1)  # Brown door
    drawCuboid(3, 3, 0.2)
    glPopMatrix()

def draw_escalator(pos, y_offset, direction):
    """Draw escalator"""
    glPushMatrix()
    glTranslatef(pos[0], y_offset + 0.5, pos[2])
    if direction == "up":
        glColor3f(0.0, 1.0, 0.0)  # Green for up
    else:
        glColor3f(1.0, 0.0, 0.0)  # Red for down
    drawCuboid(4, 1, 6)
    glPopMatrix()

def draw_target_object(pos, y_offset):
    """Draw the target object (GPU) to collect"""
    glPushMatrix()
    glTranslatef(pos[0], y_offset + 1, pos[2])
    glColor3f(1.0, 1.0, 0.0)  # Gold color
    drawCuboid(1, 0.5, 2)  # GPU-like shape
    glPopMatrix()

def debug_current_floor():
    """Debug function to print current floor info"""
    current = get_current_floor()
    if current in FLOORS:
        floor_data = FLOORS[current]
        print(f"\nCurrent Floor: {current} ({floor_data['name']})")
        print(f"Y Offset: {floor_data['y_offset']}")
        print(f"Obstacles: {len(floor_data['obstacles'])}")
        print(f"Escalator Up: {floor_data.get('escalator_up', 'None')}")
        print(f"Escalator Down: {floor_data.get('escalator_down', 'None')}")
        print(f"Door: {floor_data.get('door_pos', 'None')}")
        print(f"Target: {floor_data.get('target_object', 'None')}")