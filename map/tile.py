from map.definitions import Terrain, Feature, UnitType, UiElement, HexDir
import map.resources as resources
from map.util import mapLocToPixelPos
from map.constants import MAP_DISPLAY_WIDTH, WINDOW_HEIGHT, MAX_DISTANCE

from copy import deepcopy

class Tile():
    def __init__(self, pos, terr=Terrain.WATER, feature=None, unit=None, ui=None):
        self.pos = deepcopy(pos)
        self.abs_pixel_pos = mapLocToPixelPos(self.pos)
        
        self.move_cost = 0

        self.setTerrain(terr)
        self.feature = None
        self.setFeature(feature)
        self.unit_list = list()
        self.ui_element = ui
        
        self.terrain_sprite = None
        self.feature_sprite = None
        self.unit_sprite = None
        self.border_sprites = [] 
        
        self.neighbors = [None] * HexDir.LENGTH
        #for graph operations
        self.visited = False
        self.distance = MAX_DISTANCE
        self.prev_tile = None
        
        self.elevation = None
        self.moisture = None
        self.base_temperature = None
        
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

    def addBorder(self, terrain, hexdir):
        
        if self.terrain == Terrain.WATER:
            if terrain == Terrain.ICE:
                self.border_sprites.append(resources.ice_water_border(hexdir))
                self.border_sprites.append(resources.ice_border(hexdir))
            elif terrain == Terrain.SNOW_TUNDRA:
                self.border_sprites.append(resources.snow_water_border(hexdir))
            elif terrain == Terrain.GRASS:
                self.border_sprites.append(resources.abrupt_grass_border(hexdir))
            elif terrain == Terrain.SEMI_DRY_GRASS:
                self.border_sprites.append(resources.abrupt_semidry_grass_border(hexdir))
            elif terrain == Terrain.DRY_GRASS:
                self.border_sprites.append(resources.abrupt_dry_grass_border(hexdir))
            elif terrain == Terrain.DESERT:
                self.border_sprites.append(resources.desert_border(hexdir))
            elif terrain == Terrain.DESERT_HILLS:
                self.border_sprites.append(resources.desert_hill_border(hexdir))
                
        if self.terrain == Terrain.ICE:
            if terrain == Terrain.SNOW_TUNDRA:
                self.border_sprites.append(resources.snow_border(hexdir))
            elif terrain == Terrain.DRY_GRASS:
                self.border_sprites.append(resources.dry_grass_border(hexdir))
            elif terrain == Terrain.DESERT_HILLS:
                self.border_sprites.append(resources.desert_hill_border(hexdir))
            
        if self.terrain == Terrain.SNOW_TUNDRA:
            if terrain == Terrain.SNOW_HILLS:
                self.border_sprites.append(resources.snow_hill_border(hexdir))            
            elif terrain == Terrain.GRASS:
                self.border_sprites.append(resources.grass_border(hexdir))
            elif terrain == Terrain.SEMI_DRY_GRASS:
                self.border_sprites.append(resources.semidry_grass_border(hexdir))                    
            elif terrain == Terrain.DRY_GRASS:
                self.border_sprites.append(resources.dry_grass_border(hexdir))
            elif terrain == Terrain.DESERT_HILLS:
                self.border_sprites.append(resources.desert_hill_border(hexdir))
                
        if self.terrain == Terrain.GRASS:
            if terrain == Terrain.SNOW_HILLS:
                self.border_sprites.append(resources.snow_hill_border(hexdir))
            elif terrain == Terrain.DESERT_HILLS:
                self.border_sprites.append(resources.desert_hill_border(hexdir))
                
        if self.terrain == Terrain.SEMI_DRY_GRASS:
            if terrain == Terrain.GRASS:
                self.border_sprites.append(resources.grass_border(hexdir))
            elif terrain == Terrain.SNOW_HILLS:
                self.border_sprites.append(resources.snow_hill_border(hexdir))
            elif terrain == Terrain.DESERT_HILLS:
                self.border_sprites.append(resources.desert_hill_border(hexdir))

        if self.terrain == Terrain.DRY_GRASS:
            if terrain == Terrain.GRASS:
                self.border_sprites.append(resources.grass_border(hexdir))
            elif terrain == Terrain.SEMI_DRY_GRASS:
                self.border_sprites.append(resources.semidry_grass_border(hexdir))
            elif terrain == Terrain.SNOW_HILLS:
                self.border_sprites.append(resources.snow_hill_border(hexdir))
            elif terrain == Terrain.DESERT_HILLS:
                self.border_sprites.append(resources.desert_hill_border(hexdir))
                
        if self.terrain == Terrain.DESERT:
            if terrain == Terrain.GRASS:
                self.border_sprites.append(resources.grass_border(hexdir))
            elif terrain == Terrain.SEMI_DRY_GRASS:
                self.border_sprites.append(resources.semidry_grass_border(hexdir))
            elif terrain == Terrain.DRY_GRASS:
                self.border_sprites.append(resources.dry_grass_border(hexdir))
            elif terrain == Terrain.SNOW_TUNDRA:
                self.border_sprites.append(resources.snow_water_border(hexdir))
            elif terrain == Terrain.SNOW_HILLS:
                self.border_sprites.append(resources.snow_hill_border(hexdir))
            elif terrain == Terrain.DESERT_HILLS:
                self.border_sprites.append(resources.desert_hill_border(hexdir))
            
    def setFeature(self, feature):
        if self.feature == Feature.FOREST:
            self.move_cost -= 1
        
        self.feature = feature
        if feature == Feature.FOREST:
            self.move_cost += 1
        
    def addNewUnit(self, unit_type):
        if unit_type == UnitType.SETTLER:
            settler = unit.Settler(self.pos)
            self.unit_list.append(settler)
    
    def addUnit(self, unit):
        self.unit_list.append(unit)
    
    def addUnits(self, units):
        self.unit_list += units
    
    def terrainImg(self):
        if self.terrain == Terrain.WATER:
            return resources.ocean_anim
        elif self.terrain == Terrain.ICE:
            return resources.random_ice()
        elif self.terrain == Terrain.GRASS:
            return resources.random_grass()
        elif self.terrain == Terrain.SEMI_DRY_GRASS:
            return resources.random_semidry_grass()
        elif self.terrain == Terrain.DRY_GRASS:
            return resources.random_dry_grass()
        elif self.terrain == Terrain.DESERT:
            return resources.random_desert()
        elif self.terrain == Terrain.SNOW_TUNDRA:
            return resources.random_snow()
        elif self.terrain ==  Terrain.HILLS:
            return resources.random_hills()
        elif self.terrain == Terrain.SNOW_HILLS:
            return resources.random_snow_hills()
        elif self.terrain == Terrain.DRY_HILLS:
            return resources.random_dry_hills()
        elif self.terrain == Terrain.DESERT_HILLS:
            return resources.random_desert_hill()
        elif self.terrain == Terrain.MOUNTAIN:
            return resources.random_mountain()
        elif self.terrain == Terrain.DRY_MOUNTAIN:
            return resources.random_dry_mountain()
        elif self.terrain == Terrain.SNOW_MOUNTAIN:
            return resources.random_snow_mountains()
        else:
            return None
    
    def featureImg(self):
        if self.feature == Feature.FOREST:
            return resources.random_forest()
        elif self.feature == Feature.SAVANNA:
            return resources.random_savanna()
        elif self.feature == Feature.PINE:
            return resources.random_pine()
        elif self.feature == Feature.JUNGLE:
            return resources.random_jungle()
        elif self.feature == Feature.RAINFOREST:
            return resources.random_rainforest()
        elif self.feature == Feature.PALM:
            return resources.random_palm()
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
            
    def borderImgs(self):
        return self.border_sprites

    def getMapPos(self):
        return deepcopy(self.pos)

    def getAbsolutePixelPos(self):
        return deepcopy(self.abs_pixel_pos)
        
    def getPixelPos(self, scale=1.0):
        return mapLocToPixelPos(self.pos, scale)
        
    """
    isValidCityLocation:
    Tests whether a tile is a valid place for a city to be built.
    """
    #TODO: Allow additional terrain types.
    #TODO: Check if a city is already present, or other obstacle preventing settling.
    def isValidCityLocation(self):
        return self.isFlatland() or self.isHills()

    def isFlatland(self):
        return (
            self.terrain == Terrain.GRASS or
            self.terrain == Terrain.SEMI_DRY_GRASS or
            self.terrain == Terrain.DRY_GRASS or
            self.terrain == Terrain.DESERT or
            self.terrain == Terrain.SNOW_TUNDRA)
            
    def isHills(self):
        return (
            self.terrain == Terrain.HILLS or
            self.terrain == Terrain.DRY_HILLS or
            self.terrain == Terrain.DESERT_HILLS or
            self.terrain == Terrain.SNOW_HILLS)
            
    def isMountain(self):
        return (
            self.terrain == Terrain.MOUNTAIN or
            self.terrain == Terrain.SNOW_MOUNTAIN or
            self.terrain == Terrain.DRY_MOUNTAIN)
            
    def hasForest(self):
        return (
            self.feature == Feature.FOREST or
            self.feature == Feature.PINE or
            self.feature == Feature.RAINFOREST or
            self.feature == Feature.JUNGLE or
            self.feature == Feature.SAVANNA or
            self.feature == Feature.PALM)
    
    def isEnterableByLandUnit(self):
        return self.isFlatland() or self.isHills()
        
    def hasUnit(self):
        return len(self.unit_list) > 0
        
    def notVisited(self):
        return not self.visited
