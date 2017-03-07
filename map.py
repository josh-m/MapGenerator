"""
Map

Map generates and stores the list of tiles and their indexes.
Also keeps track of the currently selected tile.
"""

import random
import math
from queue import Queue
from opensimplex import OpenSimplex

from tile import Tile
from definitions import HexDir, Terrain, Feature, UnitType, UiElement
from constants import MAP_COL_COUNT, MAP_ROW_COUNT, MAX_DISTANCE, WRAP_X, WRAP_Y
from util import isEven

ELEVATION_SEALEVEL = 0.05
ELEVATION_HILL = 0.4
ELEVATION_MOUNTAIN = 0.6

MOISTURE_DESERT = -0.5
MOISTURE_DRY = -0.1
MOISTURE_SEMIDRY = 0.2
MOISTURE_NORMAL = 0.5
MOISTURE_WET = 0.8

TEMPERATURE_FROZEN = -0.5
TEMPERATURE_COLD = -0.2
TEMPERATURE_TEMPERATE = 0.3
TEMPERATURE_HOT = 0.5
    
class Map():
    """
    __init__:
    By default creates a map with the default size.
    Supply two integers to constructor to generate a different size.
    """
    def __init__(self, n_cols=MAP_COL_COUNT, n_rows=MAP_ROW_COUNT):
        self.size = (n_cols, n_rows)
        self.columns = list()

        #generate the tiles for the map
        for col in range(n_cols):
            column = list()
            for row in range(n_rows):
                column.append(Tile([col, row]))

            self.columns.append(column)

        self.generateElevation()
        self.generateMoisture()
        self.determineTemperature()
        self.determineBiomes()
        
        self.generateTerrainBorders()
        
        self.generateForests()
        

        self.selectStartTile()
        
        self.selected_tile = None

    def selectStartTile(self):
        walkable_tiles = [tile for tile in self.allTiles() if tile.isEnterableByLandUnit()]
        
        print( len(walkable_tiles))
        
        self.start_tile = random.choice(walkable_tiles)

        self.start_tile.addNewUnit(UnitType.SETTLER)
        
    """
    selectTile:
    Given a tile, sets its UI element to a border and
    tracks the tile as the currently selected tile.
    """
    #TODO: Check that this tile is within this map.
    #TODO: Consider removal, is never called.    
    def selectTile(self, tile):
        if tile:
            if self.selected_tile:
                self.selected_tile.ui_element = None
            tile.ui_element = UiElement.BORDER
            self.selected_tile = tile

    """
    tileAt:
    Returns the tile object at the position (pos) given.
    Supports indices larger than the map for world wrap support.
    """
    def tileAt(self, pos):
        x = pos[0]
        y = pos[1]
        
        if WRAP_X:
            x = x % (self.size[0])
        if WRAP_Y:
            y = y % (self.size[1])
        
        #is requested tile out of bounds?
        if (x < 0 or x >= MAP_COL_COUNT
            or y < 0 or y >= MAP_ROW_COUNT):
            return None
            
        tile = self.columns[x][y]
            
        return tile

    """
    Returns the column at the given index (col_idx).
    Supports specifying a subset of the col.
    """
    def column(self, col_idx, start_row=0, end_row=MAP_ROW_COUNT):
        ls = list()
        for row_idx in range(start_row, end_row):
            tile = self.tileAt([col_idx, row_idx])
            if tile:
                ls.append(tile)

        return ls
    
    """
    Returns the column at the given index (row_idx).
    Supports specifying a subset of the row.
    """
    def row(self, row_idx, start_col=0, end_col=MAP_COL_COUNT):
        ls = list()
        for col_idx in range(start_col, end_col):
            tile = self.tileAt([col_idx, row_idx])
            if tile:
                ls.append(tile)

        return ls

    """
    notVisited:
    Checks if a tile's visited attribute is set.
    (The visited attribute is used as a temporary state variable for
    generation algorithms)
    """
    def notVisited(self, tile):
        if (not tile.visited):
            return True
        else:
            return False
    """
    resetAllVisited:
    Sets the visited attribute to false for every tile in this Map.
    """
    def resetAllVisited(self):
        for col in self.columns:
            for tile in col:
                tile.visited = False
                tile.prev_tile = None
                tile.distance = MAX_DISTANCE

    
    #
    #World building methods
    #

    """
    generateElevation:
    Generates elevation using simplex noise.
    """
    def generateElevation(self, seed=None, freq=6.0):
        if not seed:
            seed = random.randint(0,999999)
        else:
            seed =  int(seed)
            
        simplex = OpenSimplex(seed)
        seed += 1
        simplex2 = OpenSimplex(seed)
        seed += 1
        simplex3 = OpenSimplex(seed)
        
        """
        a = 0.6
        b = 1.2
        c = 0.7
        """
        a = 0.1
        b = 1.0
        c = 1.0
        
        low = 100
        high = -100
        sum = 0
        i=0
        
        low_nx = 100
        high_nx = -100
        low_d = 100
        high_d = -100
        
        for col in self.columns:
            for tile in col:                
                #set noise values for tiles between [0,1],
                #makes input normalized across disparate map sizes
                nx = tile.pos[0] / self.size[0] - 0.5
                ny = tile.pos[1] / self.size[1] - 0.5
                
                
                elevation = (
                    simplex.noise2d(freq * nx, freq * ny) + 
                    0.5 * simplex2.noise2d(3.0*freq * nx, 3.0*freq*ny) + #higher freq less effect
                    0.25 * simplex3.noise2d(100.0*freq * nx, 100.0*freq*ny)
                )
                
                d = 2.0 * max(abs(nx) , abs(ny)) #manhattan distance
                
                
                elevation = (elevation + a) * (1 - d**2)
                    
                #elevation = elevation + a - b*d**c
                #elevation = elevation ** 2
                
                tile.elevation =  elevation
                                    
                #DEBUG
                if elevation < low:
                    low = elevation
                elif elevation > high:
                    high = elevation
                sum += elevation
                i += 1
                    
                if  nx < low_nx:
                    low_nx = nx
                elif nx > high_nx:
                    high_nx = nx
                if  d < low_d:
                    low_d = d
                elif d > high_d:
                    high_d = d
           
        #DEBUG
        avg = sum /  i
                    
        print('Elevation: MIN={} MAX={} AVG={}'.format(low,high,avg))
        print('Input nx: MIN={} MAX={}'.format(low_nx,high_nx))
        print('Manhattan Distance: MIN={} MAX={}'.format(low_d,high_d))
          

    def generateMoisture(self, seed=None):
        if not seed:
            seed = random.randint(0,999999)
        else:
            seed =  int(seed)
            
        simplex = OpenSimplex(seed)

        for col in self.columns:
            for tile in col:                
                #set noise values for tiles between [0,1],
                #makes input normalized across disparate map sizes
                nx = tile.pos[0] / self.size[0] - 0.5
                ny = tile.pos[1] / self.size[1] - 0.5
                
                freq = 12.0
                
                moisture = (
                    simplex.noise2d(freq * nx, freq * ny) 
                )

                tile.moisture =  moisture
                    
    def determineTemperature(self):
        #debug
        low_temp = 9999
        high_temp = -9999
    
        for col in self.columns:
            for tile in col:
                latitude_mod = abs( tile.pos[1]/ self.size[1] - 0.5)
                
                tile.base_temperature = 1.5 - 0.5*(tile.elevation + 1) - 4*latitude_mod
                
                if tile.base_temperature < low_temp:
                    low_temp = tile.base_temperature
                elif tile.base_temperature > high_temp:
                    high_temp = tile.base_temperature
         
        #debug
        print("Low Temp: {}  High Temp: {}".format(low_temp, high_temp))
        
    def determineBiomes(self):
        for tile in self.allTiles():
            #Elevation
            if tile.elevation < ELEVATION_SEALEVEL:
                if tile.base_temperature < TEMPERATURE_FROZEN:
                    tile.setTerrain(Terrain.ICE)
                else:
                    tile.setTerrain(Terrain.WATER)
                
            elif tile.elevation < ELEVATION_HILL:
                if tile.base_temperature < TEMPERATURE_COLD:
                    tile.setTerrain(Terrain.SNOW_TUNDRA)
                    
                else:
                    if tile.moisture < MOISTURE_DESERT:
                        tile.setTerrain(Terrain.DESERT)
                    elif tile.moisture < MOISTURE_DRY:
                        tile.setTerrain(Terrain.DRY_GRASS)
                    elif tile.moisture < MOISTURE_SEMIDRY:
                        tile.setTerrain(Terrain.SEMI_DRY_GRASS)
                    else:
                        tile.setTerrain(Terrain.GRASS)
                
            elif tile.elevation < ELEVATION_MOUNTAIN:
                if tile.base_temperature < TEMPERATURE_COLD:
                    tile.setTerrain(Terrain.SNOW_HILLS)
                else:
                    if tile.moisture < MOISTURE_DRY:
                        tile.setTerrain(Terrain.DESERT_HILLS)
                    elif tile.moisture < MOISTURE_NORMAL:
                        tile.setTerrain(Terrain.DRY_HILLS)
                    else:
                        tile.setTerrain(Terrain.HILLS)
            else:
                if tile.moisture < MOISTURE_DRY:
                    tile.setTerrain(Terrain.DRY_MOUNTAIN)
                else:
                    if tile.base_temperature < TEMPERATURE_COLD:
                        tile.setTerrain(Terrain.SNOW_MOUNTAIN)
                    else:
                        if tile.moisture < MOISTURE_NORMAL:
                            tile.setTerrain(Terrain.DRY_MOUNTAIN)
                        else:
                            tile.setTerrain(Terrain.MOUNTAIN)
    
    def generateTerrainBorders(self):
        for tile in self.allTiles():
            nw_neighbor = self.tileAt(self.neighborAt(tile.pos, HexDir.UL))
            n_neighbor = self.tileAt(self.neighborAt(tile.pos, HexDir.U))
            ne_neighbor = self.tileAt(self.neighborAt(tile.pos, HexDir.UR))
            sw_neighbor = self.tileAt(self.neighborAt(tile.pos, HexDir.DL))
            s_neighbor = self.tileAt(self.neighborAt(tile.pos, HexDir.D))
            se_neighbor = self.tileAt(self.neighborAt(tile.pos, HexDir.DR))
            
            neighbors = [nw_neighbor, n_neighbor, ne_neighbor,
                sw_neighbor, s_neighbor, se_neighbor]
            
            dir = HexDir.UL        
            for neighbor in neighbors:
                if neighbor:
                    tile.addBorder(neighbor.terrain, dir)   
                dir += 1
    
    """
    generateLandmassAround:
    Randomly sets a portion of tiles around the given index
    to flatland.
    Larger or smaller areas can be specified by providing a
    gen_chance above or below the default 100.
    """ 
    #TODO: Allow more options for the landmass (shape...)
    #TODO: Generate interesting land with varied terrain. (Mountain, hills, beachers)
    def generateLandmassAround(self, pos, gen_chance= 100.0):
        this_tile = self.tileAt(pos)
        this_tile.visited = True

        gen_list = self.neighborsOf(this_tile)
        temp_list = list()

        while gen_list:
            #set all these tiles to visited
            #and give them a chance to be added to landmass
            for tile in gen_list:
                tile.visited = True

                if random.uniform(0, 99.9) < gen_chance:
                    tile.setTerrain(Terrain.GRASS)
                    temp_list += self.neighborsOf(tile)

            gen_list = gen_list + temp_list
            #prune visited from list
            gen_list = list(filter(self.notVisited, gen_list))

            #TODO: KNOWN BUG -- decreasing the following value may result in an infinite loop
            #where gen_list is growing too fast, and the temp_list is getting nearly
            #every tile on the map (even duplicates due to the world wrapping in neighborAt())
            #FIX OPTIONS: check for duplicates (use visited attribute), remove world wrapping,
            #or just don't change the value (although loop is still possible,
            # however unlikely, with regular values)
            gen_chance -= 5.0

            
    """
    generateForests:
    Meant to be called after landmass is generated. Creates forests randomly on the map.
    """
    def generateForests(self):
        gen_chance = 7.0
        land = list()
        for col in self.columns:
            land += [tile for tile in col if tile.isFlatland()]

        for tile in land:
            if (random.uniform(0, 100.0) < gen_chance) and (not tile.feature):
                if tile.terrain == Terrain.GRASS:
                    tile.setFeature(Feature.FOREST)
                elif tile.terrain == Terrain.DRY_GRASS:
                    tile.setFeature(Feature.SAVANNA)
                elif tile.terrain == Terrain.DESERT:
                    tile.setFeature(Feature.PALM)
                self.spreadForest(tile)
                self.resetAllVisited()

    """
    spreadForest:
    Helper function of generateForests; adds trees in
    an area around the tile.
    """
    def spreadForest(self, tile, gen_chance=100.0):
        tile.visited = True
        
        if (random.uniform(0,99.9) < gen_chance):
            if tile.terrain == Terrain.GRASS:
                tile.setFeature(Feature.FOREST)
            elif tile.terrain == Terrain.DRY_GRASS:
                tile.setFeature(Feature.SAVANNA)
            elif tile.terrain == Terrain.DESERT:
                tile.setFeature(Feature.PALM)
                
            neighbors = self.neighborsOf(tile)
            neighbors = [_tile for _tile in neighbors if _tile.isFlatland()]
            neighbors = filter(self.notVisited, neighbors)
        
            for neighbor_tile in neighbors:
                self.spreadForest(neighbor_tile, gen_chance - 25.0)
            
    """
    neighborsOf:
    Returns a list of all tiles immediately neighboring the given tile           
    """
    def neighborsOf(self, tile):
        return self.neighborsOfPos(tile.pos)

    """
    neighborsOfPos:
    Returns a list of all tiles immediately neighboring the tile at the given index
    """
    def neighborsOfPos(self, pos):
        #print str(pos[0]) + " " + str(pos[1])
        ls = list()
        for dir in range(HexDir.FIRST, HexDir.LENGTH):
            _pos = self.neighborAt(pos, dir)

            if _pos:
                ls.append(self.tileAt(_pos))

        return ls

    """
    neighborAt:
    Given an index on the map and a direction (HexDir), returns
    that neighboring tile. Supports world wrapping.
    """
    def neighborAt(self, pos, dir):
        pos_x, pos_y = self.tileAt(pos).pos

        _x = -1
        _y = -1

        width = self.size[0]
        height = self.size[1]

        if (dir == HexDir.UL):
            _x = (pos_x - 1) % self.size[0]

            if isEven(pos_x):
                _y = pos_y
            else:
                _y = (pos_y - 1) % self.size[1]

        elif (dir == HexDir.U):
            _x = pos_x
            _y = (pos_y - 1) % self.size[1]

        elif (dir == HexDir.UR):
            _x = (pos_x + 1) % self.size[0]

            if isEven(pos_x):
                _y = pos_y
            else:
                _y = (pos_y - 1) % self.size[1]

        elif (dir == HexDir.DL):
            _x = (pos_x - 1) % self.size[0]
            if isEven(pos_x):
                _y = (pos_y + 1) % self.size[1]
            else:
                _y = pos_y

        elif (dir == HexDir.D):
            _x = pos_x
            _y = (pos_y + 1) % self.size[1]

        elif (dir == HexDir.DR):
            _x = (pos_x + 1) % self.size[0]

            if isEven(pos_x):
                _y = (pos_y + 1) % self.size[1]
            else:
                _y = pos_y

        return [_x,_y]

    #Returns a list of HexDir that constitutes a best
    #land path from start to end.
    def determineShortestLandPath(self, start, end):
        path_list = list()
        if not end.isEnterableByLandUnit():
            return path_list
        
        current_tile = start
        start.distance = 0
        
        land = list()
        for col in self.columns:
            land += [tile for tile in col if tile.isEnterableByLandUnit()]
        
        while not current_tile.visited:
            neighbors = self.neighborsOf(current_tile)
            neighbors = [tile for tile in neighbors if tile.isEnterableByLandUnit()]
            
            for tile in neighbors:
                new_distance = tile.move_cost + current_tile.distance
                if new_distance < tile.distance:
                    tile.distance = new_distance
                    tile.prev_tile = current_tile
                    
            current_tile.visited = True
            #has end tile been reached?
            if current_tile == end:
                break
            
            land.remove(current_tile)
            
            
            current_tile = None
            min_distance = MAX_DISTANCE
            for tile in land:
                if tile.distance < min_distance:
                    current_tile = tile
                    min_distance = tile.distance
                    
            #All potential paths have been exhausted
            if not current_tile:
                self.resetAllVisited()
                return []
        
        #path has been found, reconstruct
        curr_path_tile = current_tile

        while curr_path_tile:
            path_list.insert(0, curr_path_tile.pos)
            curr_path_tile = curr_path_tile.prev_tile
    
        self.resetAllVisited()
        return path_list
    
    def moveUnit(self, unit):
        if len(unit.move_list) < 1:
            return [self.tileAt(unit.map_idx),self.tileAt(unit.map_idx)]
        moves = unit.moves_left
        if moves <= 0:
            return [self.tileAt(unit.map_idx),self.tileAt(unit.map_idx)]
        
        start_pos = unit.map_idx
        i=1
        next_tile = None
        for tile_idx in unit.move_list[1:]:
            next_tile = self.tileAt(tile_idx)
            moves -= next_tile.move_cost
            unit.moves_left -= next_tile.move_cost
            i += 1
            if moves <= 0 or tile_idx == unit.move_list[-1]:
                next_tile.addUnit(unit)
                unit.setMapIdx(tile_idx)
                break
        
        remaining_moves = unit.move_list[i-1:]
        unit.setMovePath(remaining_moves)
                
        if not next_tile:
        #The unit did not move
            return [self.tileAt(unit.map_idx), self.tileAt(unit.map_idx)]

        return [self.tileAt(start_pos), self.tileAt(unit.map_idx)]
    
    def allUnits(self):
        units = list()
        for col in self.columns:
            for tile in col:
                units += tile.unit_list
    
        return units
        
    def allTiles(self):
        tiles = list()
        for col in self.columns:
            for tile in col:
                tiles.append(tile)
                
        return tiles
