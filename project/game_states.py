# game_states.py
from floors import *
from floor_transitions import *

# Game states
GAME_MENU = 0
GAME_MISSION_BRIEFING = 1
GAME_PLAYING = 2
GAME_MISSION_COMPLETE = 3
GAME_GAME_OVER = 4

# Mission states
MISSION_ENTER_BUILDING = 0    # Enter through door
MISSION_REACH_6TH_FLOOR = 1   # Navigate to 6th floor
MISSION_REACH_12TH_FLOOR = 2  # Navigate to 12th floor  
MISSION_COLLECT_OBJECT = 3    # Get the GPU
MISSION_RETURN_6TH = 4        # Go back to 6th floor
MISSION_RETURN_GROUND = 5     # Go back to ground floor
MISSION_EXIT_BUILDING = 6     # Exit through door

current_game_state = GAME_MENU
current_mission_state = MISSION_ENTER_BUILDING

mission_text = {
    MISSION_ENTER_BUILDING: "Enter the building through the main door",
    MISSION_REACH_6TH_FLOOR: "Take the escalator to the 6th floor",
    MISSION_REACH_12TH_FLOOR: "Take the escalator to the 12th floor", 
    MISSION_COLLECT_OBJECT: "Collect the GPU from the server room",
    MISSION_RETURN_6TH: "Return to the 6th floor using the escalator",
    MISSION_RETURN_GROUND: "Return to the ground floor using the escalator",
    MISSION_EXIT_BUILDING: "Exit the building through the main door"
}

def get_current_game_state():
    return current_game_state

def set_game_state(state):
    global current_game_state
    current_game_state = state

def get_current_mission():
    return current_mission_state

def get_mission_text():
    return mission_text.get(current_mission_state, "")

def update_mission_progress():
    """Check and update mission progress based on player actions"""
    global current_mission_state
    
    current_floor = get_current_floor()
    
    # Mission state transitions
    if current_mission_state == MISSION_ENTER_BUILDING:
        if current_floor == 0:  # Player entered building
            current_mission_state = MISSION_REACH_6TH_FLOOR
            
    elif current_mission_state == MISSION_REACH_6TH_FLOOR:
        if current_floor == 1:  # Reached 6th floor
            current_mission_state = MISSION_REACH_12TH_FLOOR
            
    elif current_mission_state == MISSION_REACH_12TH_FLOOR:
        if current_floor == 2:  # Reached 12th floor
            current_mission_state = MISSION_COLLECT_OBJECT
            
    elif current_mission_state == MISSION_COLLECT_OBJECT:
        if hasattr(player, 'has_gpu') and player.has_gpu:  # Collected GPU
            current_mission_state = MISSION_RETURN_6TH
            
    elif current_mission_state == MISSION_RETURN_6TH:
        if current_floor == 1 and player.has_gpu:  # Back to 6th with GPU
            current_mission_state = MISSION_RETURN_GROUND
            
    elif current_mission_state == MISSION_RETURN_GROUND:
        if current_floor == 0 and player.has_gpu:  # Back to ground with GPU
            current_mission_state = MISSION_EXIT_BUILDING
            
    elif current_mission_state == MISSION_EXIT_BUILDING:
        # Check if player exited building (implement door exit logic)
        pass

def handle_object_collection():
    """Handle collecting the target object"""
    if check_target_object_interaction() and current_mission_state == MISSION_COLLECT_OBJECT:
        player.has_gpu = True
        return True
    return False

def is_mission_complete():
    """Check if all missions are complete"""
    return current_mission_state >= MISSION_EXIT_BUILDING

def reset_mission():
    """Reset mission progress"""
    global current_mission_state
    current_mission_state = MISSION_ENTER_BUILDING
    player.has_gpu = False
    set_current_floor(0)