from definitions import Terrain, Feature, UnitType, UiElement, HexDir
import resources
from util import mapLocToPixelPos

from copy import deepcopy

MAP_DISPLAY_WIDTH = 800
WINDOW_HEIGHT = 600

class Tile():
    def __init__(self, pos, terr=Terrain.WATER, feature=None, unit=None, ui=None):
        self.pos = deepcopy(pos)
        self.abs_pixel_pos = mapLocToPixelPos(self.pos)

        self.terrain = terr
        self.setTerrain(terr)
        self.feature = feature
        self.unit = unit #TODO: allow multiple units
        self.ui_element = ui

        
        self.neighbors = [None] * HexDir.LENGTH
        self.visited = False

    def setNeighbor(self, dir, tile):
        self.neighbors[dir] = tile
        
    def getImageList(self):
        
        ls = list()
        if self.terrain:
            terrain_img = self.terrainImg()
            ls.append(self.terr_img)
        if self.feature:
            feature_img = self.featureImg()
            ls.append(feature_img)
        if self.ui_element:
            ui_img = self.uiElementImg()
            ls.append(ui_img)
        if self.unit:
            unit_img = self.unitImg()
            ls.append(unit_img)

        return ls

    def setTerrain(self, terrain):
        self.terrain = terrain

    def setFeature(self, feature):
        self.feature = feature
        
    def addUnit(self, unit):
        self.unit = unit
    
    def terrainImg(self):
        if self.terrain == Terrain.GRASS:
            return resources.random_grass()
        elif self.terrain == Terrain.WATER:
            return resources.ocean_anim
        else:
            return None
    
    def featureImg(self):
        if self.feature == Feature.FOREST:
            return resources.random_forest()
        elif self.feature == Feature.TOWN:
            return resources.town_image
        else:
            return None
            
    def unitImg(self):
        if self.unit == UnitType.SETTLER:
            return resources.settler_image
        else:
            return None
            
    def uiElementImg(self):
        if self.ui_element == UiElement.BORDER:
            return resources.selection_image
        else:
            return None

    def getMapPos(self):
        return deepcopy(self.pos)

    def getAbsolutePixelPos(self):
        return deepcopy(self.abs_pixel_pos)