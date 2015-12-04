"""
Map

Map generates and stores the list of tiles and their indexes.
Also keeps track of the currently selected tile.
"""

import random
from queue import Queue

from tile import Tile
from definitions import HexDir, Terrain, Feature, UnitType, UiElement
from constants import MAP_COL_COUNT, MAP_ROW_COUNT, MAX_DISTANCE
from util import isEven

    
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

        #select starting location for town
        start_loc = [   int(random.triangular(0,n_cols)),
                        int(random.triangular(0,n_rows))]
                    
        self.start_tile = self.tileAt(start_loc)
        self.start_tile.setTerrain(Terrain.GRASS)
        self.start_tile.addNewUnit(UnitType.SETTLER)

        self.generateLandmassAround(start_loc)
        self.generateForests()

        self.selected_tile = None

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

        tile = self.columns[x % (self.size[0])][y % (self.size[1])]

        return tile

    """
    Returns the column at the given index (col_idx).
    Supports specifying a subset of the col.
    """
    def column(self, col_idx, start_row=0, end_row=MAP_ROW_COUNT):
        ls = list()
        for row_idx in range(start_row, end_row):
            ls.append(self.tileAt([col_idx, row_idx]))

        return ls
    
    """
    Returns the column at the given index (row_idx).
    Supports specifying a subset of the row.
    """
    def row(self, row_idx, start_col=0, end_col=MAP_COL_COUNT):
        ls = list()
        for col_idx in range(start_col, end_col):
            ls.append(self.tileAt([col_idx, row_idx]))

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
            #or just don't fuck w/ the value (although loop is still possible,
            # however unlikely, with regular values)
            gen_chance -= 8.0

            
    """
    generateForests:
    Meant to be called after landmass is generated. Creates forests randomly on the map.
    """
    def generateForests(self):
        gen_chance = 7.0
        land = list()
        for col in self.columns:
            land += [tile for tile in col if tile.isValidForestLocation()]

        for tile in land:
            if (random.uniform(0, 100.0) < gen_chance) and (not tile.feature):
                tile.setFeature(Feature.FOREST)
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
            tile.setFeature(Feature.FOREST)
            neighbors = self.neighborsOf(tile)
            neighbors = [_tile for _tile in neighbors if _tile.isValidForestLocation()]
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
    neightborAt:
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
        
    def allUnits(self):
        units = list()
        for col in self.columns:
            for tile in col:
                units += tile.unit_list
    
        return units

            
               
            
            
        
        
            
            
            
            
            
            
            
            