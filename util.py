from constants import WINDOW_HEIGHT

def isEven(integer):
    return not (integer % 2)
    
def mapLocToPixelPos(loc, scale = 1.0, relative = False):
    col_idx = loc[0]
    row_idx = loc[1]

    x_offset = 54 * scale
    y_offset = 72 * scale 

    y_pos = WINDOW_HEIGHT - (36 * scale)
    if isEven(col_idx):
        y_margin = y_offset/2
        y_pos = WINDOW_HEIGHT - (36 * scale) - y_margin

    x_pos = x_offset * (col_idx) + (36 * scale)
    y_pos -= y_offset * (row_idx)

    if relative:
        return [x_pos - self.cam[0], y_pos - self.cam[1]]
    else:
        return [x_pos, y_pos]