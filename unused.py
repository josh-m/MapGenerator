"""
functions that are currently unused, but may be useful in the future
"""

def isOffscreen(sprite):
    if whereOffscreen(sprite.x, sprite.y) != DiagDir.NONE:
        return True
    else:
        return False

def whereOffscreen(sprite_x, sprite_y):
    off_dir = DiagDir.NONE
    OFF_MARGIN = 36

    if sprite_x < -OFF_MARGIN:
        if sprite_y < -OFF_MARGIN:
            off_dir = DiagDir.DL
        elif sprite_y > WINDOW_HEIGHT + OFF_MARGIN:
            off_dir = DiagDir.UL
        else:
            off_dir = DiagDir.LEFT
    elif sprite_x > MAP_DISPLAY_WIDTH + OFF_MARGIN:
        if sprite_y < -OFF_MARGIN:
            off_dir = DiagDir.DR
        elif sprite_y > WINDOW_HEIGHT + OFF_MARGIN:
            off_dir = DiagDir.UR
        else:
            off_dir = DiagDir.RIGHT
    elif sprite_y < -OFF_MARGIN:
        off_dir = DiagDir.DOWN
    elif sprite_y > WINDOW_HEIGHT + OFF_MARGIN:
        off_dir = DiagDir.UP

    return off_dir   