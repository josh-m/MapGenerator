import random

from tile import Tile
from definitions import HexDir, Terrain, Feature, UiElement
from constants import MAP_X, MAP_Y

def isEven(integer):
    return not (integer % 2)

#TODO: disable world wrapping
#The world is flat! (Add sea monsters at ocean edges)
    
class Map():
    def __init__(self, cols=MAP_X, rows=MAP_Y):
        self.size = (cols, rows)
        self.columns = list()

        for col in range(cols):
            column = list()
            for row in range(rows):
                column.append(Tile([col, row]))

            self.columns.append(column)

        #select starting location for town
        town_loc = [int(random.triangular(0,cols)),
                    int(random.triangular(0,rows))]
        print("rand town idx:" +str(town_loc))
        town_tile = self.tileAt(town_loc)
        print("tile idx:" +str(town_tile.pos) +" tile_px_pos:"+str(town_tile.abs_pixel_pos))
        town_tile.setTerrain(Terrain.GRASS)
        town_tile.feature = Feature.TOWN

        self.start_tile = town_tile

        print("start_tile pix pos: "+str(self.start_tile.abs_pixel_pos))

        self.generateLandmassAround(town_loc)
        self.generateForests()

        self.selected_tile = None

    def selectTile(self, tile):
        if tile:
            if self.selected_tile:
                self.selected_tile.ui_element = None
            tile.ui_element = UiElement.BORDER
            self.selected_tile = tile

    def tileAt(self, pos):
        x = pos[0]
        y = pos[1]

        tile = self.columns[x % (self.size[0])][y % (self.size[1])]

        return tile

    #TODO: investigate potential error in tileAt(col)
    def column(self, col, start_row, end_row):
        ls = list()
        for row in range(start_row, end_row):
            ls.append(self.tileAt([col, row]))

        return ls

    def row(self, row, start_col, end_col):
        ls = list()
        for col in range(start_col, end_col):
            ls.append(self.tileAt([col, row]))

        return ls

    def notVisited(self, tile):
        if (not tile.visited) and tile.depth == -1:
            return True
        else:
            return False

    def isFlat(self, tile):
        return tile.terrain == Terrain.GRASS

    def notVisited(self,tile):
        if (not tile.visited) and tile.depth == -1:
            return True
        else:
            return False

    def resetVisited(self):
        for col in self.columns:
            for tile in col:
                tile.visited = False

    def resetDepth(self):
        for col in self.columns:
            for tile in col:
                tile.depth = -1

    #
    #World building methods
    #

    def generateForests(self):
        gen_chance = 7.0
        land = list()
        for col in self.columns:
            land += filter(self.isFlat, col)

        for tile in land:
            if (random.uniform(0, 100.0) < gen_chance) and (not tile.feature):
                tile.feature = Feature.FOREST
                self.spreadForest(tile)
                self.resetVisited()

    def spreadForest(self, tile, gen_chance=100.0):
        tile.visited = True
        
        if (random.uniform(0,99.9) < gen_chance):
            tile.feature = Feature.FOREST
            neighbors = self.neighborsOf(tile)
            neighbors = filter(self.isFlat, neighbors)
            neighbors = filter(self.notVisited, neighbors)
        
            for neighbor_tile in neighbors:
                self.spreadForest(neighbor_tile, gen_chance - 25.0)

    #def generatePoles(self):

    def neighborsOf(self, tile):
        return self.neighborsOfPos(tile.pos)

    #returns a list of all neighboring tiles
    def neighborsOfPos(self, pos):
        #print str(pos[0]) + " " + str(pos[1])
        ls = list()
        for dir in range(HexDir.FIRST, HexDir.LENGTH):
            _pos = self.neighborAt(pos, dir)

            if _pos:
                ls.append(self.tileAt(_pos))

        return ls


    #returns tile coordinates if neighbor exists, else None
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
            x = (pos_x + 1) % self.size[0]

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

    #iterative iteration that produces more bulky landmasses
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

            #BUG: 
            #decreasing too much increases chance of infinite loop
            #
            gen_chance -= 8.0
