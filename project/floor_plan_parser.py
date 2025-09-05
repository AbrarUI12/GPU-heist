# floor_plan_parser.py
from floor_plan import floor_0, floor_1, floor_2, meaning

# Grid settings (must match your world settings)
GRID_SIZE = 40
WORLD_MIN = -100  # ARENA_HALF negated
CELL_SIZE = 5.0   # GRID_STEP

def grid_to_world_coords(row, col):
    """Convert grid indices to world coordinates (center of cell)"""
    x = WORLD_MIN + col * CELL_SIZE + CELL_SIZE / 2
    z = WORLD_MIN + row * CELL_SIZE + CELL_SIZE / 2
    return x, z

def parse_floor_matrix(floor_matrix, floor_y_offset):
    """Parse a 40x40 floor matrix and return floor data"""
    obstacles = []
    escalator_up_pos = None
    escalator_down_pos = None
    door_positions = []
    target_object_pos = None
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_value = floor_matrix[row][col]
            x, z = grid_to_world_coords(row, col)
            
            if cell_value == 1:  # Wall
                obstacles.append({
                    "pos": (x, floor_y_offset, z),
                    "size": (CELL_SIZE, 3.0, CELL_SIZE),  # 5x3x5 wall
                    "type": "wall"
                })
            
            elif cell_value == 2:  # Escalator up
                escalator_up_pos = (x, floor_y_offset, z)
            
            elif cell_value == 3:  # Escalator down
                escalator_down_pos = (x, floor_y_offset, z)
            
            elif cell_value == 4:  # Pocket gate/door
                door_positions.append((x, floor_y_offset, z))
            
            elif cell_value == 5:  # GPU/target object
                target_object_pos = (x, floor_y_offset, z)
    
    return {
        "obstacles": obstacles,
        "escalator_up": escalator_up_pos,
        "escalator_down": escalator_down_pos,
        "door_positions": door_positions,
        "target_object": target_object_pos
    }

def generate_all_floors():
    """Generate floor data for all floors from matrices"""
    floors_data = {}
    
    # Floor 0 (Ground)
    floor_0_data = parse_floor_matrix(floor_0, 0.0)
    floors_data[0] = {
        "name": "Ground Floor",
        "y_offset": 0.0,
        "obstacles": floor_0_data["obstacles"],
        "escalator_up": floor_0_data["escalator_up"],
        "escalator_down": floor_0_data["escalator_down"],
        "door_pos": floor_0_data["door_positions"][0] if floor_0_data["door_positions"] else None,
        "target_object": floor_0_data["target_object"]
    }
    
    # Floor 1 (6th Floor)
    floor_1_data = parse_floor_matrix(floor_1, 15.0)
    floors_data[1] = {
        "name": "6th Floor", 
        "y_offset": 15.0,
        "obstacles": floor_1_data["obstacles"],
        "escalator_up": floor_1_data["escalator_up"],
        "escalator_down": floor_1_data["escalator_down"],
        "door_pos": None,  # No external door on middle floors
        "target_object": floor_1_data["target_object"]
    }
    
    # Floor 2 (12th Floor)
    floor_2_data = parse_floor_matrix(floor_2, 30.0)
    floors_data[2] = {
        "name": "12th Floor",
        "y_offset": 30.0, 
        "obstacles": floor_2_data["obstacles"],
        "escalator_up": floor_2_data["escalator_up"],
        "escalator_down": floor_2_data["escalator_down"],
        "door_pos": None,  # No external door on top floor
        "target_object": floor_2_data["target_object"]
    }
    
    return floors_data

def debug_floor_layout(floor_num):
    """Print debug info about a floor's layout"""
    matrices = [floor_0, floor_1, floor_2]
    if floor_num >= len(matrices):
        print(f"Floor {floor_num} doesn't exist")
        return
    
    matrix = matrices[floor_num]
    print(f"\nFloor {floor_num} Layout:")
    print("=" * 50)
    
    # Count different elements
    counts = {}
    positions = {key: [] for key in meaning.keys()}
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = matrix[row][col]
            counts[value] = counts.get(value, 0) + 1
            if value in positions:
                x, z = grid_to_world_coords(row, col)
                positions[value].append((x, z))
    
    # Print summary
    for value, count in counts.items():
        element_type = meaning.get(value, f"unknown({value})")
        print(f"{element_type}: {count} cells")
        
        if value != 0:  # Don't print all empty positions
            print(f"  Positions: {positions[value][:5]}")  # Show first 5 positions
            if len(positions[value]) > 5:
                print(f"  ... and {len(positions[value]) - 5} more")

if __name__ == "__main__":
    # Test the parser
    for floor in range(3):
        debug_floor_layout(floor)
    
    print("\nGenerating floor data...")
    floors = generate_all_floors()
    
    for floor_num, floor_data in floors.items():
        print(f"\nFloor {floor_num}: {floor_data['name']}")
        print(f"  Obstacles: {len(floor_data['obstacles'])}")
        print(f"  Escalator up: {floor_data['escalator_up']}")
        print(f"  Escalator down: {floor_data['escalator_down']}")
        print(f"  Door: {floor_data['door_pos']}")
        print(f"  Target: {floor_data['target_object']}")