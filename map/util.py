from map.constants import WINDOW_HEIGHT
from map.definitions import Terrain

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
        
def tileMinimapColor(tile):
    color = (0,0,0)
    
    if tile.hasUnit():
        color = (255,0,0)
    elif tile.hasForest():
        color = (30,50,5)
    elif tile.terrain == Terrain.WATER:
        color = (0,0,225)
    elif tile.terrain == Terrain.GRASS:
        color = (0,200,0)
    elif tile.terrain == Terrain.SEMI_DRY_GRASS:
        color = (30, 180, 0)
    elif tile.terrain == Terrain.DRY_GRASS:
        color = (130, 150, 0)
    elif tile.terrain ==  Terrain.HILLS:
        color = (150,200,130)
    elif tile.terrain == Terrain.DRY_HILLS:
        color = (120,120,100)
    elif (
    tile.terrain == Terrain.MOUNTAIN or 
    tile.terrain == Terrain.DRY_MOUNTAIN or
    tile.terrain == Terrain.SNOW_MOUNTAIN):
        color = (56,52,47)
    elif tile.terrain ==  Terrain.DESERT:
        color = (255,200,0)
    elif tile.terrain == Terrain.DESERT_HILLS:
        color = (205,160, 0)
    elif tile.terrain == Terrain.SNOW_TUNDRA:
        color = (255,255,255)
    elif tile.terrain == Terrain.SNOW_HILLS:
        color = (220,220,220)
    elif tile.terrain == Terrain.ICE:
        color = (100,190,215)
        
    return color