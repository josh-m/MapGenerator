from definitions import Terrain, Feature, UnitType, UiElement, HexDir
import resources
from util import mapLocToPixelPos

from copy import deepcopy

from constants import MAP_DISPLAY_WIDTH, WINDOW_HEIGHT, MAX_DISTANCE
import unit


class Tile():
    def __init__(self, pos, terr=Terrain.WATER, feature=None, unit=None, ui=None):
        self.pos = deepcopy(pos)
        self.abs_pixel_pos = mapLocToPixelPos(self.pos)
        
        self.move_cost = 0

        self.setTerrain(terr)
        self.setFeature(feature)
        self.unit_list = list()
        self.ui_element = ui

        
        self.neighbors = [None] * HexDir.LENGTH
        #for graph operations
        self.visited = False
        self.distance = MAX_DISTANCE
        self.prev_tile = None
        
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
        if terrain == Terrain.GRASS:
            self.move_cost = 1

    def setFeature(self, feature):
        self.feature = feature
        if feature == Feature.FOREST:
            self.move_cost += 1
        
    def addNewUnit(self, unit_type):
        if unit_type == UnitType.SETTLER:
            settler = unit.Settler()
            self.unit_list.append(settler)
    
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
        if len(self.unit_list) > 0:
            return self.unit_list[0].image()
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
        
    """
    isValidCityLocation:
    Tests whether a tile is a valid place for a city to be built.
    """
    #TODO: Allow additional terrain types.
    #TODO: Check if a city is already present, or other obstacle preventing settling.
    def isValidCityLocation(self):
        return self.terrain == Terrain.GRASS

    def isValidForestLocation(self):
        return self.terrain == Terrain.GRASS
    
    def isEnterableByLandUnit(self):
        return self.terrain == Terrain.GRASS