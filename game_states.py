# game_states.py
from floors import *
from floor_transitions import *

# Game states
GAME_MENU = 0
GAME_MISSION_BRIEFING = 1
GAME_PLAYING = 2
GAME_MISSION_COMPLETE = 3
GAME_GAME_OVER = 4
GAME_VICTORY = 5  # New victory state

# Mission states
MISSION_ENTER_BUILDING = 0    # Enter through door
MISSION_REACH_6TH_FLOOR = 1   # Navigate to 6th floor
MISSION_REACH_12TH_FLOOR = 2  # Navigate to 12th floor  
MISSION_COLLECT_OBJECT = 3    # Get the GPU
MISSION_RETURN_6TH = 4        # Go back to 6th floor
MISSION_RETURN_GROUND = 5     # Go back to ground floor
MISSION_EXIT_BUILDING = 6     # Exit through door

# GPU theft state
gpu_theft_progress = 0.0
gpu_theft_duration = 5.0  # 5 seconds
is_stealing_gpu = False

current_game_state = GAME_MENU
current_mission_state = MISSION_ENTER_BUILDING

mission_text = {
    MISSION_ENTER_BUILDING: "Enter the building through the main door",
    MISSION_REACH_6TH_FLOOR: "Take the escalator to the 6th floor",
    MISSION_REACH_12TH_FLOOR: "Take the escalator to the 12th floor", 
    MISSION_COLLECT_OBJECT: "Find and steal the GPU from the server room",
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

def start_gpu_theft():
    """Start GPU theft process"""
    global is_stealing_gpu, gpu_theft_progress
    if check_target_object_interaction() and current_mission_state == MISSION_COLLECT_OBJECT:
        is_stealing_gpu = True
        gpu_theft_progress = 0.0
        print("[GPU THEFT] Hold E to steal the GPU...")

def update_gpu_theft(dt, holding_e=False):
    """Update GPU theft progress"""
    global is_stealing_gpu, gpu_theft_progress
    
    if not is_stealing_gpu:
        return False
    
    if not check_target_object_interaction():
        # Player moved away, cancel theft
        is_stealing_gpu = False
        gpu_theft_progress = 0.0
        print("[GPU THEFT] Cancelled - moved away from GPU")
        return False
    
    if holding_e:
        gpu_theft_progress += dt
        progress_percent = (gpu_theft_progress / gpu_theft_duration) * 100
        if gpu_theft_progress % 1.0 < dt:  # Print every second
            print(f"[GPU THEFT] Progress: {progress_percent:.0f}%")
        
        if gpu_theft_progress >= gpu_theft_duration:
            # Theft complete!
            player.has_gpu = True
            is_stealing_gpu = False
            gpu_theft_progress = 0.0
            print("[GPU THEFT] GPU STOLEN! Now escape the building!")
            return True
    else:
        # Not holding E, cancel theft
        is_stealing_gpu = False
        gpu_theft_progress = 0.0
        print("[GPU THEFT] Cancelled - stopped holding E")
    
    return False

def get_gpu_theft_progress():
    """Get current GPU theft progress (0.0 to 1.0)"""
    if not is_stealing_gpu:
        return 0.0
    return min(gpu_theft_progress / gpu_theft_duration, 1.0)

def is_gpu_theft_in_progress():
    """Check if GPU theft is in progress"""
    return is_stealing_gpu

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
        # Check if player with GPU is at the door - this triggers victory
        if player.has_gpu and check_door_interaction():
            set_game_state(GAME_VICTORY)
            print("MISSION ACCOMPLISHED! Player escaped with the GPU!")

def handle_object_collection():
    """Start GPU collection process"""
    if check_target_object_interaction() and current_mission_state == MISSION_COLLECT_OBJECT:
        if not is_stealing_gpu:
            start_gpu_theft()
        return True
    return False

def handle_door_interaction():
    """Handle door interaction - exit or victory"""
    if check_door_interaction():
        if current_mission_state == MISSION_EXIT_BUILDING and player.has_gpu:
            # Victory condition met!
            set_game_state(GAME_VICTORY)
            return "victory"
        else:
            # Regular door interaction (entering building)
            return "enter"
    return None

def is_mission_complete():
    """Check if all missions are complete"""
    return current_mission_state >= MISSION_EXIT_BUILDING

def reset_mission():
    """Reset mission progress"""
    global current_mission_state, is_stealing_gpu, gpu_theft_progress
    current_mission_state = MISSION_ENTER_BUILDING
    is_stealing_gpu = False
    gpu_theft_progress = 0.0
    player.has_gpu = False
    set_current_floor(0)

def reset_game_to_menu():
    """Reset everything back to character selection"""
    global current_game_state, current_mission_state, is_stealing_gpu, gpu_theft_progress
    
    # Reset game state
    current_game_state = GAME_MENU
    current_mission_state = MISSION_ENTER_BUILDING
    
    # Reset GPU theft state
    is_stealing_gpu = False
    gpu_theft_progress = 0.0
    
    # Reset player
    player.pos = [0.0, 0.75, 0.0]
    player.angDeg = 0.0
    player.lying = False
    player.scale = 1.0
    player.balls = 0
    player.health = 10
    player.current_floor = 0
    player.has_gpu = False
    
    # Reset floor
    set_current_floor(0)
    
    print("Game reset to character selection")

def trigger_game_over():
    """Trigger game over state when player dies"""
    global current_game_state
    current_game_state = GAME_GAME_OVER
    print("[GAME OVER] Player has died!")