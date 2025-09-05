# floor_transitions.py
import math
from floors import *
from classes import player

# Transition states
TRANSITION_NONE = 0
TRANSITION_ESCALATOR = 1
TRANSITION_DOOR = 2

transition_state = TRANSITION_NONE
transition_progress = 0.0
transition_duration = 3.0  # 3 seconds for escalator ride
target_floor = 0

def check_escalator_interaction():
    """Check if player is near an escalator"""
    global transition_state, target_floor
    
    current = get_current_floor()
    floor_data = FLOORS[current]
    
    # Check escalator up
    if floor_data["escalator_up"]:
        pos = floor_data["escalator_up"]
        distance = math.sqrt(
            (player.pos[0] - pos[0])**2 + 
            (player.pos[2] - pos[2])**2
        )
        if distance < 3.0 and current < 2:  # Within range and not top floor
            return "escalator_up", current + 1
    
    # Check escalator down  
    if floor_data["escalator_down"]:
        pos = floor_data["escalator_down"] 
        distance = math.sqrt(
            (player.pos[0] - pos[0])**2 + 
            (player.pos[2] - pos[2])**2
        )
        if distance < 3.0 and current > 0:  # Within range and not ground floor
            return "escalator_down", current - 1
            
    return None, None

def check_door_interaction():
    """Check if player is near the exit door"""
    current = get_current_floor()
    if current != 0:  # Only ground floor has door
        return False
        
    floor_data = FLOORS[current]
    if not floor_data["door_pos"]:
        return False
        
    pos = floor_data["door_pos"]
    distance = math.sqrt(
        (player.pos[0] - pos[0])**2 + 
        (player.pos[2] - pos[2])**2
    )
    return distance < 3.0

def check_target_object_interaction():
    """Check if player can collect the target object"""
    current = get_current_floor()
    if current != 2:  # Only top floor has target
        return False
        
    floor_data = FLOORS[current]
    if "target_object" not in floor_data:
        return False
        
    pos = floor_data["target_object"]
    distance = math.sqrt(
        (player.pos[0] - pos[0])**2 + 
        (player.pos[2] - pos[2])**2
    )
    return distance < 2.0

def start_escalator_transition(direction, new_floor):
    """Start escalator transition"""
    global transition_state, target_floor, transition_progress
    transition_state = TRANSITION_ESCALATOR
    target_floor = new_floor
    transition_progress = 0.0

def update_transitions(dt):
    """Update any ongoing transitions"""
    global transition_state, transition_progress, target_floor
    
    if transition_state == TRANSITION_ESCALATOR:
        transition_progress += dt / transition_duration
        
        # Smoothly move player vertically during transition
        start_y = get_floor_y_offset(get_current_floor()) + 0.75
        end_y = get_floor_y_offset(target_floor) + 0.75
        player.pos[1] = start_y + (end_y - start_y) * transition_progress
        
        if transition_progress >= 1.0:
            # Transition complete
            set_current_floor(target_floor)
            player.pos[1] = get_floor_y_offset(target_floor) + 0.75
            transition_state = TRANSITION_NONE
            transition_progress = 0.0

def is_transitioning():
    """Check if currently in transition"""
    return transition_state != TRANSITION_NONE

def get_transition_progress():
    """Get current transition progress (0.0 to 1.0)"""
    return transition_progress