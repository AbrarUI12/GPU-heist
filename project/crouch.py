# crouch.py
# Handle player crouching state with body scaling and toggle

GROUND_Y = 1.0        # normal standing height
CROUCH_Y = 0.4        # lower height when crouched
GROUND_SCALE = 1.0    # normal model scale
CROUCH_SCALE = 0.6    # smaller body when crouched

is_crouching = False   # global state


def toggle_crouch(player):
    """Toggle crouching on/off."""
    global is_crouching
    if is_crouching:
        # Stand up
        is_crouching = False
        player.pos[1] = GROUND_Y
        player.scale = GROUND_SCALE
    else:
        # Crouch
        is_crouching = True
        player.pos[1] = CROUCH_Y
        player.scale = CROUCH_SCALE
