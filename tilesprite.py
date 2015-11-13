import pyglet
from constants import MAP_DISPLAY_WIDTH, WINDOW_HEIGHT
from util import mapLocToPixelPos

class TileSprite(pyglet.sprite.Sprite):

    def __init__(self, sprite_type, map_pos, *args, **kwargs):
        super(TileSprite, self).__init__(*args, **kwargs)
        self.map_pos = map_pos
        self.pix_pos = mapLocToPixelPos(self.map_pos)
        self.sprite_type = sprite_type
        
    def moveToMapIdx(self, idx):
        self.map_pos = idx
        self.pix_pos = mapLocToPixelPos(self.map_pos)