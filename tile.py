from definitions import Terrain, Feature, UiElement, HexDir
import resources

from copy import deepcopy

MAP_DISPLAY_WIDTH = 800
WINDOW_HEIGHT = 600

def isEven(integer):
    return not (integer % 2)

def mapLocToPixelPos(loc, relative = False):
    col_idx = loc[0]
    row_idx = loc[1]

    x_offset = 54
    y_offset = 72 #image size

    y_pos = WINDOW_HEIGHT - 36
    if isEven(col_idx):
        y_margin = y_offset/2
        y_pos = WINDOW_HEIGHT - 36 - y_margin

    x_pos = x_offset * (col_idx) + 36
    y_pos -= y_offset * (row_idx)

    if relative:
        return [x_pos - self.cam[0], y_pos - self.cam[1]]
    else:
        return [x_pos, y_pos]

def PixelPosToMapLoc(pix_pos):
    x_offset = 54
    y_offset = 72
    y_margin = y_offset/2

    col_idx = (pix_pos[0] - 36) / x_offset

    if isEven(col_idx):
        row_idx -= y_margin

    row_idx = row_idx / y_offset

    return [int(col_idx), int(row_idx)]

class Tile():
    def __init__(self, pos, terr=Terrain.WATER, feature=None, ui=None):
        self.pos = deepcopy(pos)
        self.abs_pixel_pos = mapLocToPixelPos(self.pos)

        self.animated = False
        self.terrain = terr
        self.setTerrain(terr)
        self.feature = feature
        self.ui_element = ui

        self.neighbors = [None] * HexDir.LENGTH
        self.visited = False
        self.depth = -1

        #self.terrain_sprite = None
        #self.feature_sprite = None


    def setNeighbor(self, dir, tile):
        self.neighbors[dir] = tile

    def getImageList(self):
        if self.terr_img:
            terr = self.terr_img

        feat = self.featureImg()
        elem = self.uiElementImg()

        ls = list()
        if self.terr_img:
            ls.append(self.terr_img)
        if feat:
            ls.append(feat)
        if elem:
            ls.append(elem)

        return ls

    def setTerrain(self, terrain):
        self.terrain = terrain
        if terrain == Terrain.GRASS:
            self.terr_img = resources.random_grass()
        elif terrain == Terrain.WATER:
            self.terr_img = resources.ocean_anim
            self.animated = True

    def setFeature(self, feature):
        self.feature = feature
        
            
    def featureImg(self):
        if self.feature == Feature.FOREST:
            return resources.random_forest()
        elif self.feature == Feature.TOWN:
            return resources.town_image
        else:
            return None

    def uiElementImg(self):
        if self.ui_element == UiElement.BORDER:
            return resources.selection_image
        else:
            return None

    def getMapPos(self):
        return deepcopy(self.pos)

    def getPixPos(self):
        return deepcopy(self.abs_pixel_pos)