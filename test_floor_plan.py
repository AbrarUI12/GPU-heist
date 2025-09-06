# test_floor_plan.py
# Run this to test your floor plan implementation

from floor_plan_parser import generate_all_floors, debug_floor_layout, grid_to_world_coords
from floor_plan import floor_0, floor_1, floor_2, meaning

def test_coordinate_mapping():
    """Test that grid coordinates map correctly to world coordinates"""
    print("Testing coordinate mapping:")
    print("-" * 30)
    
    # Test corners and center
    test_points = [
        (0, 0),      # Top-left of grid
        (0, 39),     # Top-right of grid  
        (39, 0),     # Bottom-left of grid
        (39, 39),    # Bottom-right of grid
        (19, 19),    # Center of grid
    ]
    
    for row, col in test_points:
        x, z = grid_to_world_coords(row, col)
        print(f"Grid [{row:2d}, {col:2d}] -> World ({x:6.1f}, {z:6.1f})")
    
    print()

def find_specific_elements():
    """Find positions of specific elements in each floor"""
    matrices = [floor_0, floor_1, floor_2]
    floor_names = ["Ground Floor", "6th Floor", "12th Floor"]
    
    for floor_idx, (matrix, name) in enumerate(zip(matrices, floor_names)):
        print(f"{name} Elements:")
        print("-" * 30)
        
        # Find each type of element
        for value, element_type in meaning.items():
            if value == 0:  # Skip empty spaces
                continue
                
            positions = []
            for row in range(40):
                for col in range(40):
                    if matrix[row][col] == value:
                        x, z = grid_to_world_coords(row, col)
                        positions.append((x, z, row, col))
            
            if positions:
                print(f"{element_type.capitalize()}s ({len(positions)} found):")
                for x, z, row, col in positions[:3]:  # Show first 3
                    print(f"  Grid[{row:2d},{col:2d}] -> World({x:6.1f}, {z:6.1f})")
                if len(positions) > 3:
                    print(f"  ... and {len(positions) - 3} more")
            else:
                print(f"{element_type.capitalize()}s: None found")
        print()

def test_floor_generation():
    """Test the floor generation from matrices"""
    print("Testing floor generation:")
    print("-" * 30)
    
    floors = generate_all_floors()
    
    for floor_num, floor_data in floors.items():
        print(f"Floor {floor_num}: {floor_data['name']}")
        print(f"  Y Offset: {floor_data['y_offset']}")
        print(f"  Obstacles: {len(floor_data['obstacles'])}")
        
        # Show escalator positions
        escalator_up = floor_data.get('escalator_up')
        escalator_down = floor_data.get('escalator_down')
        print(f"  Escalator Up: {escalator_up if escalator_up else 'None'}")
        print(f"  Escalator Down: {escalator_down if escalator_down else 'None'}")
        
        # Show door and target
        door = floor_data.get('door_pos')
        target = floor_data.get('target_object')
        print(f"  Door: {door if door else 'None'}")
        print(f"  Target Object: {target if target else 'None'}")
        
        # Show a few obstacle positions
        if floor_data['obstacles']:
            print(f"  First few obstacles:")
            for i, obs in enumerate(floor_data['obstacles'][:3]):
                pos = obs['pos']
                size = obs['size']
                print(f"    {i+1}. Pos({pos[0]:6.1f}, {pos[1]:4.1f}, {pos[2]:6.1f}) Size{size}")
        print()

def validate_floor_connectivity():
    """Check if escalators connect floors properly"""
    print("Validating floor connectivity:")
    print("-" * 30)
    
    floors = generate_all_floors()
    
    for floor_num in range(3):
        floor_data = floors[floor_num]
        print(f"Floor {floor_num}:")
        
        # Check escalator up
        if floor_data.get('escalator_up') and floor_num < 2:
            up_pos = floor_data['escalator_up']
            next_floor = floors[floor_num + 1]
            down_pos = next_floor.get('escalator_down')
            if down_pos:
                # Check if positions are reasonably close (allowing for Y offset difference)
                dx = abs(up_pos[0] - down_pos[0])
                dz = abs(up_pos[2] - down_pos[2])
                if dx < 10 and dz < 10:  # Within 10 units
                    print(f"  ✓ Escalator connects to floor {floor_num + 1}")
                else:
                    print(f"  ✗ Escalator mismatch: Up{up_pos} vs Down{down_pos}")
            else:
                print(f"  ✗ Escalator up exists but no corresponding down on floor {floor_num + 1}")
        
        # Check escalator down
        if floor_data.get('escalator_down') and floor_num > 0:
            down_pos = floor_data['escalator_down']
            prev_floor = floors[floor_num - 1]
            up_pos = prev_floor.get('escalator_up')
            if up_pos:
                dx = abs(down_pos[0] - up_pos[0])
                dz = abs(down_pos[2] - up_pos[2])
                if dx < 10 and dz < 10:
                    print(f"  ✓ Escalator connects to floor {floor_num - 1}")
                else:
                    print(f"  ✗ Escalator mismatch: Down{down_pos} vs Up{up_pos}")
        print()

def main():
    print("FLOOR PLAN TESTING")
    print("=" * 50)
    
    test_coordinate_mapping()
    find_specific_elements()
    test_floor_generation()
    validate_floor_connectivity()
    
    print("Testing complete!")
    print("\nTo run the game with your floor plans:")
    print("1. Make sure floor_plan_parser.py is in the same directory")
    print("2. Run your main.py")
    print("3. Use debug keys P, M, R during gameplay")

if __name__ == "__main__":
    main()